# Mode: docsync-pass

Use for docs-only updates: fixing stale links, updating path references, syncing section headers.

Shared context: [_shared.md](./_shared.md)

## Checklist

1. **Scope confirmation** — state which docs will be touched; Xavier confirms before edits.
2. **Read before edit** — always read the full file before editing; never overwrite blindly.
3. **Minimal diffs** — fix only what's stale; do not reformat unrelated sections.
4. **No governed-state edits** — docs under `docs/` are fine; `users/cici/governed-state/**` requires a proposal.
5. **Commit message** — prefix `docs:` (e.g. `docs: fix stale path refs in setup-guide`).
6. **Push gate** — commit locally (EXECUTE_LOCAL) unless Xavier says "ship remote."

## Common docsync tasks

- Update `CLAUDE.md` table when a new agent or command is added.
- Fix broken links after a file rename.
- Sync skill doc path references after a `docs/skills/` reorganization.
- Update `docs/operator-daily-log.md` date headers.

## Anti-patterns

- Rewriting docs content (voice, strategy) during a docsync — that needs a PLAN pass first.
- Touching `proposals/` files (schema, examples) without a separate proposal.
