# Go reference

Mirror the section layout and harness ideas of `assets/template.py`, translated to idiomatic Go. Single file, `package main`, runnable with `go run file.go [max_size]`.

## Toolchain and style

- Go 1.21+; standard library only unless a dependency is clearly justified (generics are available: `slices`, `maps`, `cmp`).
- Idiomatic Go: small interfaces, errors as values (`fmt.Errorf("...: %w", err)`, sentinel errors with `errors.Is`), `context.Context` as first parameter for anything cancellable, no panics for expected failures.
- Concurrency: goroutines + channels or `sync.WaitGroup`/`errgroup`-style patterns written with the stdlib; guard shared state with `sync.Mutex`/`sync.RWMutex` or `sync/atomic`. Always state who owns each goroutine's lifetime (no leaks) and how it stops.
- Preallocate slices/maps with `make(..., 0, n)` when size is known; avoid needless allocation in hot paths; mention `sync.Pool` only when it truly applies.
- The code must pass `go vet`; run it if `go` is available.

## Benchmark harness pattern

- A `testing.B` benchmark needs a separate `_test.go` file, so inside the single file use `time.Now()`/`time.Since()` with best-of-N, and `runtime.ReadMemStats` (compare `TotalAlloc` before/after, run `runtime.GC()` first) for allocation volume.
- Prevent dead-code elimination by storing results in a package-level `sink` variable.
- Growing sizes, per-approach time budget with a "skipped (too slow)" line, deterministic inputs via `rand.New(rand.NewSource(42))`.
- Correctness check against a brute-force reference before timing; use `reflect.DeepEqual` or `slices.Equal`. If concurrency is involved, mention `go run -race` in the header comment as the recommended verification.
- Print the table with `fmt.Printf("%10d | %-12s | %10.2f | ...")`.

## Sandbox note

Check `which go`. If missing and not installable, deliver the file untested, say so, and report no fabricated numbers.
