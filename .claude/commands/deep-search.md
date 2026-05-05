---
name: deep-search
description: Multi-pass AI-augmented search across Supabase memory and governed-state. Decomposes the query, runs parallel semantic passes, cross-references verified facts, surfaces tensions and gaps, and produces a tier-annotated synthesis. Pass the query as the argument.
argument-hint: <query>
---

Run a deep search for: **$ARGUMENTS**

Follow `docs/skills/deep-search.md`.

---

## Phase 1 — Query decomposition

Break `$ARGUMENTS` into 3–5 orthogonal sub-questions. Write them out before searching. Each sub-question should approach the topic from a different angle (e.g., what/why/when/who/how, or: current state / history / blockers / next steps).

Example for "BrewMind pricing strategy":
1. What pricing tiers or numbers have been captured?
2. What rationale or reasoning exists for pricing decisions?
3. What competitors or benchmarks are mentioned?
4. What pricing concerns or blockers have been logged?
5. When was pricing last discussed or decided?

---

## Phase 2 — Multi-pass MCP semantic search

For each sub-question, call the MCP `search` tool with a distinct phrasing. Aim for 3–5 search calls total — vary the wording to catch different embeddings.

Also call `recent_thoughts` once to surface any recent captures on the topic that semantic search might miss.

**Labeling rule:** All MCP results are Tier C. Tag every finding: `[C: supabase/<thought-id-or-date>]`

---

## Phase 3 — Governed-state cross-reference

Scan these paths for any verified facts related to the query:

- `users/cici/governed-state/identity/instance.json`
- `users/cici/governed-state/voice/session-behavior.json`
- `users/cici/governed-state/memory-policy/policy.json`
- `users/cici/governed-state/source-priority/policy.json`
- `users/cici/governed-state/workflows/`
- `docs/companion-agent/brewmind-companion-contract.md`
- `docs/companion-agent/brewmind-open-loops.md`

Any finding from these files is Tier B (structured doc) or Tier A if it was directly authored by Xavier. Tag each: `[A: <path>]` or `[B: <path>]`

---

## Phase 4 — Synthesis

Produce a structured report:

```
## Deep Search: <query>
Date: YYYY-MM-DD

### Answer summary
[2–4 sentences answering the query as directly as possible, citing tiers]

### What the memory system knows (by sub-question)
1. [sub-question]: [finding] [tier tag]
2. [sub-question]: [finding] [tier tag]
...

### Verified facts (Tier A/B)
- [fact] [A/B: source]

### Unverified signals (Tier C)
- [signal] [C: source] — confidence: high/medium/low

### Gaps — what is NOT in the memory system
- [topic or angle with no results]

### Tensions
- [description of contradiction between sources, with both cited]
  → Suggested resolution: [one sentence]

### Recommended actions
| Action | Type | Priority |
|--------|------|----------|
| Capture [X] to Supabase | capture | high/med/low |
| Verify [claim] against primary source | verify | high/med/low |
| Draft proposal for [surface] | propose | high/med/low |
```

---

## Phase 5 — Wait for Xavier

Present the report and stop. Do not capture, propose, or modify any governed state without Xavier's direction.

If the query relates to BrewMind facts (pricing, partnerships, launch dates), explicitly note which claims are unverified [C] and require promotion before being treated as decisions.
