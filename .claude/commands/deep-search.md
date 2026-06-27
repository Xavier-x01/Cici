---
name: deep-search
description: Multi-pass AI-augmented search across Supabase memory and governed-state. Decomposes the query, runs parallel governed-state workers, cross-references verified facts, surfaces tensions and gaps, and produces a tier-annotated synthesis. Pass the query as the argument.
argument-hint: <query>
---

Run a deep search for: **$ARGUMENTS**

---

## Phase 1 — Orchestrator: Query decomposition

Break `$ARGUMENTS` into 3–5 orthogonal sub-questions. Write them out explicitly before spawning workers. Each sub-question must approach the topic from a distinct angle:

- **What** — current state, facts, decisions
- **Why** — rationale, reasoning, intent
- **When** — timeline, recency, history
- **Who** — people, partners, roles involved
- **How** — process, method, blockers
- **What not** — what was rejected or unknown

Example for "BrewMind pricing strategy":
1. What pricing tiers or numbers have been captured?
2. What rationale or reasoning exists for pricing decisions?
3. What competitors or benchmarks are mentioned?
4. What pricing concerns or blockers have been logged?
5. When was pricing last discussed or decided?

---

## Phase 2 — Parallel workers: Governed-state scan (Tier A/B)

Spawn one Explore agent **per sub-question, all in parallel** (single message, multiple Agent tool calls). Each worker receives:
- Its assigned sub-question
- The governed-state paths listed below to scan
- Instructions to return findings with tier tags and source paths

**Governed-state paths each worker must check:**
```
users/cici/governed-state/identity/instance.json
users/cici/governed-state/voice/session-behavior.json
users/cici/governed-state/memory-policy/policy.json
users/cici/governed-state/source-priority/policy.json
users/cici/governed-state/workflows/
docs/companion-agent/brewmind-companion-contract.md
docs/companion-agent/brewmind-open-loops.md
docs/brewmind.md
prepared-context/synthesis/
```

**Worker prompt template:**
```
You are a search worker for one sub-question of a deep-search task.

Sub-question: <Q>

Scan these governed-state paths for any information relevant to your sub-question:
[paths listed above]

Then use Grep to search any other local files you find relevant.

Return:
- Findings relevant to your sub-question with source paths
- Tier tags: [A: <path>] for Xavier-verified content, [B: <path>] for structured summaries
- Any gaps (sub-question angles with zero local coverage)

Do NOT synthesize across sub-questions. Stay focused on your one sub-question.
Do NOT write any files. Return findings only.
```

Collect all worker results before proceeding to Phase 3.

---

## Phase 3 — MCP semantic search (Tier C)

In the main context, run MCP searches for each sub-question. Aim for 3–5 total calls — vary phrasing to catch different embeddings:

```
search("<phrasing for sub-question 1>")
search("<phrasing for sub-question 2>")
search("<phrasing for sub-question 3>")
recent_thoughts(limit=20, filter="<topic keyword>")
```

Tag every MCP result: `[C: supabase/<source-hint>]`

---

## Phase 4 — Aggregate and synthesize

Pass the aggregated worker findings (Phase 2) and MCP results (Phase 3) to the `deep-searcher` agent. It will produce the final tier-annotated synthesis covering:

- Direct answer to the query
- Sub-question findings
- Verified facts (Tier A/B)
- Memory signals (Tier C)
- Gaps
- Tensions (with resolution suggestions)
- Recommended actions for Xavier

---

## Phase 5 — Wait for Xavier

Present the synthesis and stop. Do not capture, propose, or modify any governed state without Xavier's direction.

If the query relates to BrewMind facts (pricing, partnerships, launch dates), explicitly note which claims are unverified [C] and require promotion before being treated as decisions.
