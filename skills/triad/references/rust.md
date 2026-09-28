# Rust reference

Mirror the section layout and harness ideas of `assets/template.py`, translated to idiomatic Rust. Single file `main.rs`, std only unless justified, built with optimizations: `rustc -O main.rs && ./main [max_size]` (or `cargo run --release`). Unoptimized builds give meaningless timings, so say this in the header comment.

## Toolchain and style

- Edition 2021+. No `unsafe` unless it is the point of the scenario; if used, document the safety invariant on every block.
- Errors: a small `enum` implementing `std::fmt::Display` and `std::error::Error`; return `Result<T, E>`; no `unwrap()` on fallible paths in the optimal approach (`expect` with a reason only for true invariants).
- Prefer iterators and borrowing over cloning; pick the right collection (`Vec`, `VecDeque`, `HashMap`, `BTreeMap`, `BinaryHeap`) and justify it. Use `with_capacity` when the size is known.
- Concurrency: `std::thread::scope`, `Arc<Mutex<_>>`/`RwLock`, `mpsc` channels, atomics; explain why the design is data-race free.
- Make the wrong approach wrong in a Rust-realistic way: needless `clone()` in a loop, O(n^2) `Vec::remove(0)`/`contains`, holding a lock across slow work, quadratic string concatenation, etc.

## Benchmark harness pattern

- `std::time::Instant`, best-of-N, and `std::hint::black_box` around inputs and outputs so the optimizer cannot delete the work.
- Memory: without external crates, either count allocations with a small custom `#[global_allocator]` wrapper around `System` that tracks current/peak bytes (preferred, document it), or report only time and say memory was analytically derived.
- Deterministic input generation with a tiny xorshift/LCG PRNG written inline (no `rand` crate).
- Correctness check against a brute-force reference first; `assert_eq!` for the passes and a printed FAIL line for the deliberately wrong approach.
- Growing sizes, per-approach time budget, "skipped (too slow)" lines, formatted table via `println!("{:>10} | {:<12} | {:>10.2} | ...")`.

## Sandbox note

Check `which rustc cargo`. If missing and not installable, deliver the file untested, say so, and report no fabricated numbers.
