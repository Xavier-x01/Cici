# Skill: System Design

**Invoked by:** `/apply-skill system-design`  
**Lane:** PLAN (no writes without Xavier's explicit go-ahead)  
**When to use:** Before adding any new capability to Cici — whenever you are deciding where something belongs, not just how to build it.

---

## Why system design exists in this context

Cici's architecture has four distinct layers. Placing a capability in the wrong layer creates drift (the layer says one thing, reality is another), duplication (the same logic encoded in two places), or unresolvable conflicts (two layers own the same fact and disagree).

System design is the discipline of asking "where does this belong?" before asking "how do I build this?"

---

## The four-layer architecture

```
┌─────────────────────────────────────────────────────────┐
│  Layer 4 — Runtime memory (Supabase / pgvector)         │
│  Ephemeral, searchable, Tier C. Captured thoughts,      │
│  session context, unverified observations.               │
├─────────────────────────────────────────────────────────┤
│  Layer 3 — Governed state (users/cici/governed-state/)  │
│  Durable, owner-approved, Tier A. Identity, voice,      │
│  memory policy, workflows, source-priority.              │
├─────────────────────────────────────────────────────────┤
│  Layer 2 — Working docs (docs/, evidence/, proposals/)  │
│  Tier B. Structured summaries, proposals, protocols,    │
│  staged evidence awaiting promotion.                     │
├─────────────────────────────────────────────────────────┤
│  Layer 1 — Commands and agents (.claude/)               │
│  Behavioral: how Cici acts in a session. Slash commands, │
│  sub-agents, mode checklists. Not data — behavior.       │
└─────────────────────────────────────────────────────────┘
```

Breaking the layer order (e.g., storing a durable policy in Supabase, or treating a Supabase capture as governed truth) is the most common system design error.

---

## Capability placement decision table

| What you're adding | Right home | Why |
|---|---|---|
| A ritual Xavier runs interactively in a session | `.claude/commands/<name>.md` | Interactive behavior, not data |
| A reasoning task that needs an isolated context window | `.claude/agents/<name>.md` | Agent isolation protects main context |
| A durable policy, identity fact, or behavioral contract | `users/cici/governed-state/<surface>/` | Owner-approved truth, requires proposal |
| Runtime operational memory or session captures | Supabase (via MCP `store`) | Ephemeral, searchable, Tier C |
| A human-readable protocol or how-to reference | `docs/skills/<name>.md` or `docs/` | Working doc, Tier B |
| A staged observation or evidence unit | `evidence/` or `prepared-context/` | Pre-promotion layer |
| A queued change to governed state | `proposals/queue/prop-YYYYMMDD-NNN-*.json` | Proposal → approval flow |
| Per-project recurring data or metrics | `docs/personal/work-journal/` or `evidence/` | Structured working doc |

---

## Anti-patterns

- **Building before placing** — Writing the command/agent first, then figuring out where facts go. Decide the layer map first.
- **Governed state as a dumping ground** — Treating `users/cici/governed-state/` as a place to store anything important. Only durable, owner-approved facts belong there.
- **Commands that hold data** — Embedding business facts (pricing, partner names, dates) inside a `.claude/commands/` file. Commands hold behavior; facts belong in governed state or evidence.
- **Supabase as source of truth** — Querying `recent_thoughts` and citing the result as a confirmed decision. Supabase is Tier C — always verify against governed-state.
- **Skipping the proposal for "small" governed-state changes** — Every change to `users/cici/governed-state/` needs a proposal, even obvious ones.

---

## Sample exercise (15–30 min)

Xavier wants to track which community pilot members have completed each of the 5 Phase 1 tasks.

**Your task:** Before building anything, produce a one-page design brief that answers:
1. Which layer does this data belong in? (Use the decision table.)
2. What is the data schema? (A markdown table is fine.)
3. What command or agent, if any, reads or writes this data?
4. What is the update flow — how does a new completion get recorded?
5. What breaks if this data is stored in the wrong layer?

Write the brief in `evidence/` as a raw design note. Do not implement anything yet.
