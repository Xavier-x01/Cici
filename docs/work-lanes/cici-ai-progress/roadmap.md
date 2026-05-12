# cici-ai OB1 Roadmap

## Three Phases

The team's path from personal AI memory to a public-use system for the Philippines and beyond.

---

## Phase 1 — Personal OB1 (Month 1)

**Goal:** Every member owns and operates their own OB1 instance. Progress is visible on GitHub.

**Why it matters:** You cannot contribute to a shared system you don't understand. Month 1 is about building the skill and the habit — your own memory, your own data, your own AI.

### Task Pipeline

| # | Task | Focus | Proof |
|---|---|---|---|
| 1 | Get OB1 Live | Deploy Supabase + Edge Function | curl test / `stats` screenshot |
| 2 | Connect Your AI Client | MCP endpoint live in Claude/Cursor/ChatGPT | AI client screenshot with OB1 tools |
| 3 | Capture Your Context | 10+ thoughts stored about yourself | `recent_thoughts` screenshot |
| 4 | Seed Your Instance | Initialize governed-state in your fork | GitHub commit to `users/your-instance/` |
| 5 | First Weekly Reflection | Structured journal + 3 learnings captured | Committed journal entry |

See [`task-cards/`](task-cards/) for full instructions on each task.

### Checkpoints

| Checkpoint | Target date | What should be done |
|---|---|---|
| Week 1 | 2026-05-09 | Tasks 1–2 complete |
| Week 2 | 2026-05-16 | Tasks 3–4 complete |
| Week 3–4 | 2026-05-30 | Task 5 complete, all proof committed |

### How to Submit Proof

**Option A (Telegram):** Screenshot in the group chat — your name + task number + what's on screen.

**Option B (GitHub):** Commit to your fork under `proof/` with a short `README.md` (one sentence is fine — no personal data needed). Example: `proof/task-02/README.md` → "OB1 tools confirmed active in Claude on 2026-05-08."

Both count. GitHub makes it permanently visible to the group.

---

## Phase 2 — Shared cici-ai OB1 (After Month 1)

**Goal:** One shared Supabase project that the whole team connects to and contributes to together.

**Why it matters:** Phase 1 gives you the skills. Phase 2 gives the team collective memory — knowledge that everyone can search and build on.

### What this looks like

- Xavier sets up a shared Supabase project (`cici-ai` instance)
- Each member connects their AI client to the shared endpoint alongside their personal instance
- Contribution norms established: what to capture, how to tag, what not to store
- Each member contributes 5+ thoughts to shared memory
- Each member reviews and validates 3 other members' contributions

Task cards for Phase 2 will be published when Phase 1 closes.

---

## Phase 3 — Public Version (Philippines First)

**Goal:** A version of cici-ai that anyone can use, calibrated for the Philippines and designed to be adapted for anywhere.

**Why it matters:** Everything learned in Phases 1 and 2 gets packaged so others can benefit — not just our cohort.

### What this looks like

- Simplified setup flow for non-technical users
- Documentation and prompts in Filipino and English
- Pilot with 10+ users outside the current cohort
- Architecture that's portable to other regions

Task cards for Phase 3 will be published when Phase 2 closes.

---

## Key References

| Resource | Location |
|---|---|
| OB1 setup guide | [`docs/setup-guide.md`](../../setup-guide.md) |
| Seed phase walkthrough | [`docs/seed-phase.md`](../../seed-phase.md) |
| Instance template | [`users/_template/`](../../../users/_template/) |
| Member dashboard + proof tracking | [`cici-ai-progress/README.md`](README.md) |
| Upstream OB1 project | [NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1) |
