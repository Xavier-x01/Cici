# Research Methodology Surface

**Status: active**

## Purpose

This surface governs how Xavier conducts and tracks research: active questions, citation standards, confidence annotation rules, and how findings graduate from hypothesis to synthesis.

## Canonical Files

- `methodology.json` — Research conventions: citation standards, source trust by domain, confidence annotation, hypothesis lifecycle
- `hypothesis-schema.json` — JSON schema for a research question / hypothesis entry
- `open-questions.json` — Xavier's active research questions, surfaced at every session-start

## How research flows

1. A question is added to `open-questions.json` with `status: open`
2. As evidence accumulates, status moves to `investigating`; `evidence_refs` and `finding_summary` are updated
3. When answered with tier A or B evidence and confidence ≥ 0.7, the finding is eligible for promotion to `prepared-context/synthesis/`
4. Abandoned questions are marked `abandoned` with a reason in `finding_summary`

## Related surfaces

- `knowledge-graph/` — Concepts and relationships arising from research
- `memory-policy/` — Rules governing which research captures go to Supabase
- `source-priority/` — Trust hierarchy for external sources
