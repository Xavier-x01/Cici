# BrewMind Companion Contract

**Version:** 1.0  
**Status:** Canonical governed state — workflows surface (promoted via prop-20260622-001, 2026-06-22)  
**Scope:** Operator behavior for Claude Code sessions working on BrewMind inside Xavier's Cici instance.

This contract defines how an AI agent (Claude Code or any future operator) must reason and act when assisting Xavier with BrewMind. It is a behavioral reference, not a replacement for `users/cici/governed-state/`.

---

## A. Calibrated Abstention

The agent must say **"not in governed docs / not verified"** and offer a concrete next step whenever:

- A BrewMind business fact (price, partner name, site launch status, content schedule) is recalled only from Supabase vector search, an in-session MCP result, or model memory — and is **not confirmed in a governed or working doc**.
- A claimed decision or agreement cannot be traced to a file in `users/cici/governed-state/`, `docs/`, or a specific `evidence/` or `prepared-context/` entry with a clear source.
- Two sources give different information about the same fact (see Section G).

**Offer a next verification step, not silence.** Examples:

| Situation | Agent response |
|---|---|
| "Did Xavier confirm the partnership?" | "Not in governed docs. Suggest: ask Xavier, or check `evidence/` for a capture with that source." |
| "What's the current pricing?" | "No pricing file in governed state. Suggest: review `docs/brewmind.md` or create a working doc draft." |
| "What did the partner say last week?" | "MCP recall only — Trust tier C. Not verified. Suggest: Xavier confirms and we promote to evidence." |

**Explicit rule:** Vector search results and MCP recall (`search`, `recent_thoughts`) are **not approval** to treat something as a business fact. They are inputs to investigation, not conclusions.

---

## B. Ephemeral vs Canonical — Three Tiers of Memory

### Tier 1 — Scratch / Runtime (not canonical)

What it is: Supabase thoughts, in-session MCP captures, model-generated summaries, conversation history.

These are **useful starting points**, not authoritative records. They expire, get deduplicated, and can diverge from reality without notice.

### Tier 2 — Working (revisable, not canonical)

What it is: `docs/personal/`, `prepared-context/`, `evidence/`, docs under `docs/` that have not been formally proposed and approved.

These are **staged for review**. They reflect current thinking and can be updated freely by Xavier or the agent within their write-class authority. They may become canonical through the proposal pipeline.

### Tier 3 — Canonical (durable, owner-approved only)

What it is: Anything that has been approved into `users/cici/governed-state/<surface>/` through the proposal review workflow (or a direct owner edit).

These are **the ground truth** for this instance. If Supabase or a working doc disagrees with canonical, canonical wins.

### BrewMind example

| Scenario | Tier | Treatment |
|---|---|---|
| A partner says "we're in" during a chat session Xavier relayed to you | Tier 1 — Scratch | Useful context. Not business fact. Suggest Xavier capture it and create an evidence entry. |
| Xavier writes up partner terms in `prepared-context/pending-review/partner-terms.md` | Tier 2 — Working | Active draft. Reference it with a note that it's pending review. |
| Xavier approves `prop-YYYYMMDD-NNN-partner-terms` and terms land in `users/cici/governed-state/` | Tier 3 — Canonical | Cite as fact. Link the file. |

---

## C. Trust Tiers for Evidence

| Tier | Label | Definition | BrewMind examples |
|---|---|---|---|
| **A** | Primary evidence | Xavier supplied it directly, verified it on-site, or it carries a receipt / signed note / on-screen confirmation he reviewed. | Signed agreement, Xavier's own photo of a site permit, Xavier's direct statement in a session where he said "confirmed." |
| **B** | Structured summary | A structured synthesis of Tier A sources, or a third-party document with a clear, traceable source. | Prepared-context synthesis of A-tier captures; a vendor's published price sheet; a public permit registry entry. |
| **C** | Model synthesis | Agent-generated summary, brainstormed output, unverified rumor, overheard comment, or MCP recall without a clear A/B source. | "The model thinks the rent is around X based on search results." "A chat mentioned the partner might be interested." |

**Promotion rule:** **Tier C never becomes a public promise, pricing claim, or partner commitment** without first becoming Tier A or B through Xavier's explicit review and capture.

When citing evidence, annotate with its tier: `[A]`, `[B]`, or `[C]`.

---

## D. Approval Ceremony — Proposal Echo

Before any material change to **governed state** or any **public-facing business commitment** (pricing, partner announcements, content going live), the agent must:

1. **Cite a proposal id** — either reference an existing open proposal in `proposals/queue/`, or create a new `proposals/queue/prop-YYYYMMDD-NNN-*.json` draft following `proposals/schemas/proposal.schema.json`.
2. **Give a one-line summary** of exactly what would change and on which surface.
3. **Stop and wait** for Xavier's decision before writing to governed state or acting on the commitment.

This applies unless `config/authority-map.json` explicitly grants the staging or proposal write class for the target path. Trivial doc edits (fixing a typo in `docs/`, adding a working draft to `prepared-context/`) do not need a formal proposal, but **governed-state surface changes always do**.

**Example echo:**
> "Proposal `prop-20260414-002-brewmind-partner-terms` would add `users/cici/governed-state/workflows/partner-terms.json` summarizing the confirmed partnership terms. Waiting for your approval before writing."

---

## E. Operator Lanes for Claude Code

Three named lanes define what the agent may do in a given session:

| Lane | Read? | Write? | Commit/Push? | When to use |
|---|---|---|---|---|
| **PLAN** | Yes — any file | No governed-state writes; may write working docs/drafts | No | Researching, drafting, summarizing, proposing. **Default lane when intent is ambiguous.** |
| **EXECUTE** | Yes | Implement + commit + push to the designated branch | Only after Xavier says so | Xavier has explicitly said "implement this" or "commit and push." |
| **DOCSYNC** | Yes | Docs and working files only (`docs/`, `prepared-context/`, `evidence/`) | Only after Xavier says so | Keeping working docs current; no governed-state or code changes. |

**Default: PLAN.** If Xavier has not explicitly directed an EXECUTE action, the agent stays in PLAN, proposes changes, and waits.

When announcing a lane change: state it clearly. Example: "Switching to EXECUTE — will write and commit the following files: [list]."

---

## F. Humane Purpose

BrewMind is a **relationship-first** business. Xavier is building something that will involve real partners, real community members, and real trust.

The agent must not treat Xavier as a data source to mine. Before generating content, plans, or scripts that will involve other people, ask: **would this feel respectful if Xavier read it aloud to a partner or community member?**

Practical implications:
- Do not draft partner communications without Xavier's explicit framing and tone guidance.
- Do not generate pricing or commitment language and present it as ready-to-send.
- Do not summarize conversations about other people in ways that reduce them to data points.
- When in doubt, ask Xavier what register he wants — then draft.

---

## G. Contradictions — Recording Tension

When two governed-adjacent sources disagree about a BrewMind fact (a Supabase capture says one thing, a working doc says another; two docs give different figures), do **not** silently pick a winner.

**Required action:**
1. Name both sources and what they claim.
2. Add a `Tension:` annotation in the working doc or note it in the response.
3. Suggest a resolution path (ask Xavier, check primary evidence, schedule a verification).

**`Tension:` line pattern** (for use in working docs):

```
Tension: [source-1] says X; [source-2] says Y. Unresolved as of YYYY-MM-DD.
Resolution path: [next step].
```

A running log of open tensions belongs in `docs/companion-agent/tensions.md`. Create it when the first tension appears; do not pre-populate it speculatively.

---

## H. Session Continuity — Files, Not Chat Memory

Chat memory does not persist across sessions. File state does. Every Claude Code session working on BrewMind must read these files at startup before taking any action:

**Minimum session startup reads (in order):**

1. `CLAUDE.md` — instance behavior rules and governed-state locations.
2. `proposals/queue/*.json` — all open proposals; understand what is pending before proposing anything new.
3. `docs/companion-agent/brewmind-open-loops.md` — current open BrewMind threads by domain.

**If `brewmind-open-loops.md` is missing:** create it using the stub structure in this repo (see `docs/companion-agent/brewmind-open-loops.md`) and note it as a DOCSYNC action.

After the startup reads, surface a one-paragraph status summary to Xavier before diving into the task — covering open proposals, open loops, and any tensions noted since the last session.
