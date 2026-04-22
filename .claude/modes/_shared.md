# Shared context — always true in every mode

**Repo:** Xavier-x01/Cici (personal Open Brain instance; no application code)
**Owner:** Xavier
**Runtime:** Supabase Edge Function — not in this repo
**Canonical docs:** [CLAUDE.md](../../CLAUDE.md) | [governed-state-doctrine](../../docs/governed-state-doctrine.md)

## Non-negotiables (any mode)

- No secrets in tracked files. Keys live in Supabase secrets / CI env only.
- No direct writes to `users/cici/governed-state/**` without an approved proposal.
- Echo `prop-id + one-line summary` before applying any governed change.
- Default lane: PLAN. Switch to EXECUTE only when Xavier explicitly says so.

## Key paths

| Path | Purpose |
|------|---------|
| `evidence/` | Raw captured artifacts (Tier B/C) |
| `prepared-context/` | Staged synthesis awaiting proposal |
| `proposals/queue/` | Pending proposals — agent drafts, Xavier approves |
| `users/cici/governed-state/` | Canonical durable state (proposal-gated) |
| `docs/` | Architecture, doctrine, skills |
| `scripts/` | Utility scripts (validate, extract, doctor) |
