# Python reference

Reference implementation of the exact layout: `assets/template.py` (runnable; read it first and mirror its structure, banners and harness).

## Toolchain and style

- Target Python 3.10+; start files with `from __future__ import annotations`.
- Standard library first (`heapq`, `bisect`, `collections`, `itertools`, `functools`, `dataclasses`, `concurrent.futures`, `asyncio`). Add a third-party package only when it is clearly the professional choice (e.g. `numpy` for numeric kernels) and say so in the header.
- Full type hints, `dataclass(slots=True, frozen=True)` for value objects, `Protocol`/`ABC` for seams, `logging` (not `print`) inside library code; `print` only in the comparison/main section.
- Raise specific exceptions with clear messages; never bare `except`.
- Concurrency: threads for I/O, processes for CPU (GIL), `asyncio` for many sockets. State which one and why. If shared state exists, protect it (`threading.Lock`) and mention it.

## Benchmark harness pattern

- Wall time: `time.perf_counter()`, best-of-N (min is the least noisy), fewer repeats for big inputs.
- Peak memory: `tracemalloc` (start, run, `get_traced_memory()[1]`, stop). Measure separately from timing because tracing slows execution.
- Sizes grow geometrically (1e3 ... 1e6). A per-approach time budget skips approaches that are too slow at larger sizes and prints "skipped (too slow)".
- Deterministic inputs: `random.Random(seed)`; realistic distributions (Zipf, sorted, adversarial) rather than uniform noise when the scenario suggests it.
- Correctness first: compare all approaches against a trusted brute-force reference on small data, and run edge cases (empty, single item, duplicates, invalid arguments).

## Quality bar for the optimal approach

Validated inputs, documented complexity, deterministic output, bounded memory, no hidden global state, clear trade-offs note. Prefer algorithms with a named idea (heap selection, two pointers, sliding window, union-find, trie, monotonic deque, bitset, LRU via `OrderedDict`, token bucket, consistent hashing, ...) and say which one.

## Run

`python file.py [max_size]`
