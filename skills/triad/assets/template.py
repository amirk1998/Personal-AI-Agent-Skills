#!/usr/bin/env python3
"""
==============================================================================
SECTION 1: SCENARIO
==============================================================================
Top-K most frequent words in a large text stream.

Context
-------
A log-analytics service receives millions of tokens and must report the K most
frequent ones (K is small, e.g. 10) on demand.

Requirements
------------
- Input : a list of string tokens (n up to a few million), and an integer k.
- Output: a list of (token, count) tuples, sorted by count descending.
- Ties  : broken deterministically by token ascending, so results are stable
          across runs and Python versions.
- Errors: k must be a positive integer, otherwise ValueError.

Assumptions
-----------
- The number of unique tokens u can be large (u ~ n in the worst case).
- Memory is limited: avoid materialising more than O(u) extra data.

Goal
----
O(n) counting plus O(u log k) selection, never a full O(u log u) sort.

Run:  python template.py [max_size]
==============================================================================
"""

from __future__ import annotations

import heapq
import random
import string
import sys
import time
import tracemalloc
from collections import Counter
from typing import Callable, Sequence

Result = list[tuple[str, int]]


# =============================================================================
# SECTION 2: APPROACH 1 - THE WRONG WAY
# =============================================================================
# What the author was thinking:
#   "Take the unique words, then sort them by how often each appears.
#    list.count() already does the counting for me."
#
# Why it is wrong:
#   1. PERFORMANCE: list.count() scans the whole list for every unique word,
#      so total work is O(n * u). With u ~ n this is O(n^2).
#   2. CORRECTNESS: iterating a set() gives an arbitrary order, so ties are
#      resolved differently between runs (PYTHONHASHSEED), violating the
#      deterministic tie-break requirement.
#   3. It silently accepts k <= 0 and returns garbage instead of failing.
#
# Complexity: time O(n * u), space O(u).
# =============================================================================
def top_k_wrong(tokens: Sequence[str], k: int) -> Result:
    unique = set(tokens)  # arbitrary order -> non-deterministic ties
    ranked = sorted(unique, key=tokens.count, reverse=True)  # O(n) per word!
    return [(w, tokens.count(w)) for w in ranked[:k]]  # counts again


# =============================================================================
# SECTION 3: APPROACH 2 - THE COMMON WAY
# =============================================================================
# Why most developers write this:
#   collections.Counter is the well-known idiom, and Counter.most_common()
#   looks like exactly what the problem asks for.
#
# What is good: linear counting pass, short, readable, correct counts.
# What is missing:
#   - most_common(k) with a k that is small still fine internally (it uses a
#     heap), but the explicit version below reflects what people typically
#     write by hand: sort EVERYTHING, then slice. That costs O(u log u) even
#     though only k items are needed.
#   - No input validation.
#   - Ties depend on insertion order unless a tie-break key is added.
#
# Complexity: time O(n + u log u), space O(u) (plus a sorted copy of u items).
# =============================================================================
def top_k_common(tokens: Sequence[str], k: int) -> Result:
    counts = Counter(tokens)
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ordered[:k]


# =============================================================================
# SECTION 4: APPROACH 3 - THE OPTIMAL, PRODUCTION-GRADE WAY
# =============================================================================
# Key insight:
#   We only need the best k of u candidates. A bounded selection with a heap
#   of size k does that in O(u log k) instead of O(u log u), and never builds
#   a fully sorted copy of the frequency table.
#
# Design choices:
#   - Counter          : C-accelerated hash counting, one pass, O(n).
#   - heapq.nsmallest  : internally maintains a size-k heap; we feed it a
#                        key that makes "smallest" mean "most frequent, then
#                        lexicographically first", giving a deterministic
#                        tie-break for free.
#   - Validation       : fail fast and loudly on bad k.
#   - Fast paths       : k >= u degenerates to a plain sort (heap is pointless).
#
# Complexity: time O(n + u log k), space O(u + k).
#
# Trade-offs / when NOT to use:
#   - If the stream is unbounded and u does not fit in memory, use a
#     Count-Min Sketch + heap (approximate) or Misra-Gries instead.
#   - If k is close to u, a plain sort is equally good and simpler.
# =============================================================================
def top_k_optimal(tokens: Sequence[str], k: int) -> Result:
    if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
        raise ValueError(f"k must be a positive integer, got {k!r}")

    counts = Counter(tokens)  # O(n)

    if k >= len(counts):  # fast path: selection buys nothing
        return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))

    # Negating the count turns "largest count" into "smallest key".
    return heapq.nsmallest(k, counts.items(), key=lambda kv: (-kv[1], kv[0]))


# =============================================================================
# SECTION 5: COMPARISON HARNESS
# =============================================================================
APPROACHES: dict[str, Callable[[Sequence[str], int], Result]] = {
    "1. wrong": top_k_wrong,
    "2. common": top_k_common,
    "3. optimal": top_k_optimal,
}
TIME_BUDGET_S = 5.0  # skip an approach at larger sizes once it exceeds this


def make_tokens(n: int, seed: int = 42) -> list[str]:
    """Build a Zipf-like token list so a few words dominate, as in real text."""
    rng = random.Random(seed)
    vocab = [
        "".join(rng.choices(string.ascii_lowercase, k=6))
        for _ in range(max(10, n // 4))
    ]
    weights = [1 / (i + 1) for i in range(len(vocab))]
    return rng.choices(vocab, weights=weights, k=n)


def best_time(
    fn: Callable[..., Result], tokens: Sequence[str], k: int, repeats: int = 3
) -> float:
    """Best-of-N wall time; the minimum is the least noisy estimator."""
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        fn(tokens, k)
        best = min(best, time.perf_counter() - start)
    return best


def peak_memory_kib(fn: Callable[..., Result], tokens: Sequence[str], k: int) -> float:
    tracemalloc.start()
    fn(tokens, k)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / 1024


def check_correctness() -> None:
    """Compare every approach against a brute-force reference on small data."""
    tokens = make_tokens(2_000)
    k = 5
    reference = sorted(Counter(tokens).items(), key=lambda kv: (-kv[1], kv[0]))[:k]
    print("Correctness check (k=5, n=2000):")
    for name, fn in APPROACHES.items():
        ok = fn(tokens, k) == reference
        print(f"  {name:<12} {'PASS' if ok else 'FAIL (differs from reference)'}")
    print("Input validation check (k=0 must raise ValueError):")
    for name, fn in APPROACHES.items():
        try:
            fn(tokens, 0)
            print(f"  {name:<12} FAIL (silently accepted k=0)")
        except ValueError:
            print(f"  {name:<12} PASS (rejected k=0)")
    print()


def run_benchmark(max_size: int) -> None:
    sizes = [s for s in (1_000, 10_000, 50_000, 200_000, 1_000_000) if s <= max_size]
    k = 10
    skipped: set[str] = set()
    print(
        f"{'size':>10} | {'approach':<12} | {'time (ms)':>10} | {'peak mem (KiB)':>14} | {'vs common':>9}"
    )
    print("-" * 68)
    for n in sizes:
        tokens = make_tokens(n)
        timings: dict[str, float] = {}
        for name, fn in APPROACHES.items():
            if name in skipped:
                continue
            timings[name] = best_time(fn, tokens, k, repeats=1 if n >= 200_000 else 3)
            if timings[name] > TIME_BUDGET_S:
                skipped.add(name)  # do not attempt larger sizes
        base = timings.get("2. common")
        for name in APPROACHES:
            if name in timings:
                mem = (
                    peak_memory_kib(APPROACHES[name], tokens, k)
                    if n <= 200_000
                    else float("nan")
                )
                ratio = f"{base / timings[name]:.2f}x" if base else "n/a"
                print(
                    f"{n:>10} | {name:<12} | {timings[name] * 1000:>10.2f} | {mem:>14.0f} | {ratio:>9}"
                )
            else:
                print(f"{n:>10} | {name:<12} | {'skipped (too slow)':>10}")
        print("-" * 68)


def print_summary() -> None:
    print(
        "\nComplexity summary\n"
        "  wrong   : O(n*u)        - collapses quadratically, non-deterministic ties\n"
        "  common  : O(n+u log u)  - fine, but sorts everything to keep only k\n"
        "  optimal : O(n+u log k)  - bounded selection, validated, deterministic\n"
    )


# =============================================================================
# SECTION 6: ENTRY POINT
# =============================================================================
def main() -> None:
    max_size = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
    check_correctness()
    run_benchmark(max_size)
    print_summary()


if __name__ == "__main__":
    main()
