# Mode: proposal-review

Use when doing a focused pass over `proposals/queue/` — reading, evaluating, and surfacing decisions.

Shared context: [_shared.md](./_shared.md)
Full skill doc: [docs/skills/review-governed-change.md](../../docs/skills/review-governed-change.md)

## Checklist

1. List all `*.json` files in `proposals/queue/`; note count.
2. For each proposal:
   - Read `id`, `surface`, `status`, `summary`, `rationale`, `confidence`.
   - Check schema compliance (`proposals/schemas/proposal.schema.json`).
   - Flag: surface valid? rationale present? evidence refs traceable? conflicts?
3. Present structured evaluation per proposal (see skill doc for format).
4. **Stop** — do not approve, merge, or apply. Xavier decides.
5. If a proposal needs revision, note it as `needs-work`; do not edit the JSON without Xavier's go-ahead.

## Output format (per proposal)

```
[prop-id] <surface> — <one-line summary>
Recommendation: approve / reject / defer / needs-work
Reason: <one sentence>
Blocker (if any): <specific field or missing info>
```
