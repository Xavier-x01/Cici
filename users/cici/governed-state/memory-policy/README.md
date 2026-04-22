# Memory Policy Surface

**Status: active** — governed artifacts present. Changes require an approved proposal or direct owner edit.

## Purpose

This surface holds canonical truth about how Cici manages its memory: what to capture, what to retain, when to archive, and how to deduplicate.

## Canonical Files

| File | Description | Governed by |
|---|---|---|
| `policy.json` | Machine-readable policy: capture rules, durability classes, retention thresholds, deduplication, hygiene schedule, tag taxonomy, source weighting | `prop-20260420-001-activate-memory-policy` |
| `retention-policy.md` | Human-readable companion: explains transient/persistent classes, transition rules, promotion path, and agent obligations in plain language | `prop-20260422-001` (pending) |

## How to change this surface

1. Create a proposal in `proposals/queue/` citing the target file and describing the change.
2. Xavier reviews and approves.
3. Apply the change and move the proposal to `proposals/approved/`.
4. Log the event in `proposals/events/event-log.json`.

## Related surfaces

- `source-priority/` — how to weight sources when they conflict
- `workflows/` — recurring hygiene and maintenance flows
- `runtime-bridges/` — Supabase-specific memory policy implementation details
