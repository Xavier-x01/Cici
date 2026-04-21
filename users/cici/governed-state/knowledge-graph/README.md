# Knowledge Graph Surface

**Status: active**

## Purpose

This surface holds Xavier's canonical concept map: definitions, domain classifications, and relationships between ideas across all projects and research domains. It gives Claude a stable vocabulary to reason from rather than re-deriving definitions each session.

## Canonical Files

- `concept-schema.json` — JSON schema for a concept entry
- `concepts.json` — The concept map, seeded with core governance and research concepts

## How concepts are added

- Any concept referenced across multiple sessions or surfaces is a candidate
- New concepts are added directly to `concepts.json` with `tier: C` initially
- Xavier can promote to `tier: A` or `tier: B` by verifying the definition
- Relationships between concepts are recorded in `related_concepts`

## Related surfaces

- `research-methodology/` — Research questions generate new concepts
- `identity/` — Cici's own identity is a governed concept
- `source-priority/` — Concept definitions inform how sources are weighted
