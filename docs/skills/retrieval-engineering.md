# Skill: Retrieval Engineering

**Invoked by:** `/apply-skill retrieval-engineering`  
**Lane:** PLAN (no writes without Xavier's explicit go-ahead)  
**When to use:** When MCP searches are returning weak results, when you want to improve the quality of what gets captured, or when planning a search strategy for a `/deep-search` run.

---

## Why retrieval engineering exists in this context

The MCP server runs semantic (vector) search over Supabase. The quality of search results is determined almost entirely by the quality of what was captured — not by the search query. Garbage in, garbage out. Retrieval engineering is the discipline of improving what goes INTO the system so that future searches work.

The deep-search skill (`docs/skills/deep-search.md`) covers how to search well. This skill covers the upstream problem: how to capture well so that deep searches find what you stored.

---

## How semantic search works (conceptually)

When you store a thought, Supabase generates an embedding — a vector that represents the meaning of the text. When you search, your query is embedded and compared to all stored vectors by similarity.

**Consequence:** Two captures about the same topic but written with different words may not match. A search for "BrewMind pricing" might miss a thought you titled "monthly fee decision" because the embeddings are not similar enough.

---

## Capture quality rubric

| Quality level | Example | Problem |
|---|---|---|
| Too short | `"BrewMind pricing"` | No context for the embedding; will match too many things or nothing |
| Too vague | `"Thinking about the café setup"` | Matches anything about cafés; no specificity |
| Jargon-only | `"OB1 pgvector ext cfg done"` | Abbreviations break embedding similarity |
| Good | `"[BrewMind] Monthly membership set at $X — covers hosting + Supabase costs based on Apr 2026 model. Decision by Xavier."` | Specific, context-tagged, dated, stated as a decision |
| Best | Same as above + tags: `#brewmind #pricing #decision` | Tags enable filtering; natural language enables semantic match |

**Rules of thumb:**
- Minimum 15 words for a meaningful embedding
- Include the project name (BrewMind, OB1, Cici, pilot) so context is explicit
- State decisions as decisions: "Decided X" not "Maybe X" or "X?"
- Include the date or time context when it matters
- Use natural language, not abbreviations

---

## Tag taxonomy

Tags enable MCP's filter-based search (faster, more precise than pure semantic). Use these consistently:

| Tag | When to use |
|---|---|
| `#brewmind` | Any BrewMind business decision, partner note, or site content |
| `#cici` | Cici architecture, behavior changes, governed-state notes |
| `#pilot` | Community pilot: member status, funnel, onboarding notes |
| `#pricing` | Any thought about fees, costs, or revenue |
| `#decision` | A finalized choice (not exploration) |
| `#blocker` | Something preventing progress |
| `#question` | Open question needing Xavier's input |
| `#reflection` | Personal or retrospective observation |

Add new tags consistently — inconsistent tags are worse than no tags because they create false negatives.

---

## When semantic search will fail

| Failure mode | Cause | Fix |
|---|---|---|
| No results | Topic was never captured, or captured with very different language | Capture more; use multi-pass phrasings in search |
| Wrong results | Query matches unrelated memories | Add context words to query; use tag filter |
| Stale results | Correct topic captured, but decision changed later | Capture the update explicitly; reference the old capture |
| Duplicates | Same thought captured multiple times with slight variations | Deduplicate during evidence staging |
| Recency bias | `recent_thoughts` returns new captures that aren't relevant | Use semantic search first; `recent_thoughts` as a supplement |

---

## Multi-pass search strategy

(Summary of the pattern in `docs/skills/deep-search.md` — use that doc for the full protocol.)

For any topic, run at least 3 phrasings:
1. Direct / literal: exactly what you're looking for
2. Synonym / rephrasing: same concept, different words
3. Adjacent context: related project name or situation
4. Negative framing: "concerns about X," "blockers for X"

Compare results across passes. Unique hits in pass 2 or 3 that you'd have missed in pass 1 are evidence that your capture library has embedding variance for this topic.

---

## Anti-patterns

- **One-word captures** — `"Pricing"` as a capture. Useless for retrieval.
- **Storing decisions as questions** — `"Should we charge $X?"` stored after the decision was made. Future searches find uncertainty, not fact.
- **Over-capturing** — Every stray thought, every draft, every half-formed idea. Dilutes the signal; increases noise on every query.
- **Inconsistent tags** — Using `#BrewMind` sometimes and `#brewmind` other times. Case variance breaks filter-based search.
- **Capturing only final states** — Not capturing the reasoning behind a decision. Six months later, the decision exists but the "why" is lost.

---

## Sample exercise (15–30 min)

1. Open `evidence/` and find 3 recent captures (or pull 3 from `recent_thoughts` via MCP).
2. Evaluate each against the capture quality rubric. Score: good / needs-improvement / poor.
3. Rewrite the "needs-improvement" or "poor" ones using the rubric.
4. Run a semantic search for the topic of each rewritten capture. Does the original come up? Would your rewrite rank higher?
5. Write one sentence about what you'll do differently when capturing going forward.

Log your findings in today's work journal.
