# Lane: cici-ai-core

## Purpose

Coordinate the technical and governance core of Cici. This lane owns the governed-state doctrine, repo identity, prompts, memory policy, source-priority rules, and safety checks. Supabase and the runtime server are operational dependencies — Git-governed state is canonical truth.

## Current Scope

- Governed-state doctrine and proposal workflow
- System prompts, session bootstrap, and companion contract
- Source-priority and evidence-tier enforcement
- Repo identity: current-state docs should use Cici/operator wording; historical Xavier references in proposals and evidence are provenance and must be preserved
- Safety checks: no secrets in repo, no unapproved governed-state writes, no fabricated applicant facts
- Tracking proposal-required changes (see `proposals/queue/`)

## Open Loops

- [ ] Audit active files for stale identity references — classify as current-state (update) vs. provenance (preserve)
- [ ] Review `proposals/queue/` for any pending items needing owner decision
- [ ] Confirm `scripts/validate-governed-state.py` passes clean after any batch of changes

## Next Action

Audit active files (non-proposal, non-evidence) for stale Xavier/current-owner identity mismatches. Classify each reference:
- **Current-state**: update to Cici/operator wording
- **Provenance**: preserve as-is in proposal logs or evidence files

Produce a short classification report before making any edits.

## Key References

- Governed-state doctrine: [`docs/governed-state-doctrine.md`](../../governed-state-doctrine.md)
- Authority map: [`config/authority-map.json`](../../../config/authority-map.json)
- Proposal schema: [`proposals/schemas/proposal.schema.json`](../../../proposals/schemas/proposal.schema.json)
- Validation script: [`scripts/validate-governed-state.py`](../../../scripts/validate-governed-state.py)
- Seed phase: [`docs/seed-phase.md`](../../seed-phase.md)
