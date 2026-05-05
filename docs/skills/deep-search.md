# Skill: Deep Search

**Invoked by:** `/deep-search <query>` | `Agent(deep-searcher)`  
**Lane:** PLAN (read-only; no governed-state writes)  
**When to use:** Any question that requires correlating Supabase memory with verified governed-state facts, detecting gaps, or surfacing contradictions between sources.

---

## Why deep search exists

A single MCP `search` call returns raw Supabase results — all Tier C. It does not:
- Check against governed-state for verified facts
- Run multiple phrasings to catch different embeddings
- Identify what is *missing* from the memory system
- Flag when Supabase results contradict verified docs

Deep search adds those layers. It is a **5-phase cycle**: decompose → scan governed → search Supabase → analyze → synthesize.

---

## When to use `/deep-search` vs. the `deep-searcher` agent

| Use case | Tool |
|----------|------|
| Interactive session with Xavier | `/deep-search <query>` — runs inline |
| Complex query, protect main context window | `Agent(deep-searcher)` — spawns isolated agent |
| Broad topic needing very thorough coverage | `Agent(deep-searcher)` with `"very thorough"` breadth |
| Quick one-shot lookup | Neither — just call `search` directly |

---

## The 5-phase cycle

### Phase 1 — Query decomposition

Split the query into 3–5 sub-questions before touching any data source. Good sub-questions are:
- **Orthogonal** — each targets a different aspect
- **Searchable** — each can be run as a standalone MCP query
- **Complete** — together they cover the full scope of the original query

Write them out explicitly. This prevents confirmation bias in search and ensures gaps are visible.

### Phase 2 — Governed-state cross-reference

Scan local governed-state and doctrine docs first. These are Tier A/B — the highest-trust sources.

Key paths to always check:
```
users/cici/governed-state/            ← canonical truth
docs/companion-agent/brewmind-*       ← BrewMind contract + open loops
prepared-context/synthesis/           ← prior synthesis documents
```

Tag every finding: `[A: path]` (Xavier-verified) or `[B: path]` (structured doc).

### Phase 3 — Multi-pass MCP semantic search

Run 3–5 search calls with varied phrasings. The same concept encoded differently will surface different memories. Also run `recent_thoughts` to catch recent captures that may not have strong semantic matches.

Tag all results: `[C: supabase/<hint>]`

Recommended phrasing strategy:
1. Literal / direct phrasing of the sub-question
2. Synonym or conceptual rephrasing
3. Related context (adjacent topic or project name)
4. Negative phrasing ("concerns about X", "blockers for X")

### Phase 4 — Gap and tension analysis

**Gap** = a sub-question with zero relevant results in any source. Gaps are as informative as findings — they tell you what needs to be captured.

**Tension** = two sources that contradict each other. Always name both sources with tier tags and suggest a resolution:
- If [A] contradicts [C]: trust [A], note the C signal as stale or incorrect
- If [B] contradicts [C]: likely trust [B], flag for Xavier to verify
- If [A] contradicts [B]: rare; escalate to Xavier immediately

### Phase 5 — Synthesis

Produce the structured report format (see `/deep-search` command). Always include:
- A direct answer (even if the answer is "not well-documented")
- Per-sub-question findings
- Gaps and tensions
- Action queue (capture / verify / propose)

---

## Evidence tier reference

| Tier | Tag format | Source | Trust |
|------|-----------|--------|-------|
| A | `[A: users/cici/governed-state/...]` | Xavier-verified, directly authored | Fact — use as truth |
| B | `[B: docs/...]` | Structured doc with traceable source | Reliable — check if outdated |
| C | `[C: supabase/<hint>]` | MCP search result, model recall | Signal — never cite as confirmed fact |

**Critical rule for BrewMind claims:** Pricing, partner status, and launch dates are only reliable at Tier A or B. If only C-tier evidence exists, explicitly state: "not verified in governed docs" and recommend a capture or verification step.

---

## Anti-patterns

- **Single-pass search** — One MCP call misses concepts encoded with different words. Always run at least 3 phrasings.
- **Skipping governed-state** — Jumping straight to Supabase ignores the highest-trust source.
- **Citing C as fact** — MCP results reflect what was *captured*, not what is *true*. Captures can be outdated, speculative, or wrong.
- **Ignoring gaps** — "No results" is meaningful data. Document it.
- **Resolving tensions silently** — Always surface contradictions to Xavier; never pick one silently.

---

## Sample output skeleton

```
## Deep Search: <query>
Date: YYYY-MM-DD

### Direct answer
<2–4 sentences with inline tier citations>

### Sub-question findings
1. <sub-q>: <finding> [tier tag]
2. <sub-q>: no results — gap
...

### Verified facts (A/B)
- <fact> [A: path]

### Unverified signals (C)
- <signal> [C: supabase/...] confidence: medium

### Gaps
- <topic with no coverage>

### Tensions
- [B: doc] vs [C: supabase]: <disagreement>
  → Resolution: verify with Xavier

### Actions
| Capture X to Supabase | capture | high |
| Verify Y claim | verify | medium |
```
