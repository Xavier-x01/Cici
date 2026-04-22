# Mode: batch-ingest

Use when processing multiple `prepared-context/` files or evidence artifacts in one pass.

Shared context: [_shared.md](./_shared.md)

## Checklist

1. **Doctor first** — run `bash scripts/doctor.sh`; stop if it exits non-zero.
2. **List inputs** — enumerate files to process; confirm count with Xavier before starting.
3. **Worker file** — load the relevant worker prompt from `prepared-context/` or `docs/`; do not invent the workflow inline.
4. **Bounded loop** — process one file at a time; log results to `evidence/batch-YYYY-MM-DD.md`.
5. **Stop condition** — halt on first failure or unexpected structure; do not auto-skip silently.
6. **End-of-run report** — print: processed count, failures, next human step. Xavier sees this before commit.

## Anti-patterns

- Unbounded fan-out (processing all files without count confirmation).
- Writing to `users/cici/governed-state/**` mid-batch — queue a proposal instead.
- Logging to a path not under `evidence/` (no temp files left in repo root).
