# Skill: Product Thinking

**Invoked by:** `/apply-skill product-thinking`  
**Lane:** PLAN (no writes without Xavier's explicit go-ahead)  
**When to use:** When designing a new workflow or onboarding experience, when the pilot is losing members mid-funnel, or when Cici feels like it's being built for an ideal user instead of a real one.

---

## Why product thinking exists in this context

Xavier is simultaneously the builder of Cici and its primary user. The community pilot makes Xavier also a product manager for ~10 real people in a different context. Product thinking is the discipline of designing for real users — their actual friction, their actual starting point, their actual goals — rather than for the imagined ideal user who completes every task and reads every doc.

---

## The three user lenses

Every product decision in this system should be tested against all three:

### Lens 1 — Xavier as user

Xavier is the operator and primary user. He experiences Cici through:
- The `/session-start` ceremony (is it fast enough that he doesn't skip it?)
- The daily-task curriculum (does it teach something genuinely useful, or feel like homework?)
- The proposal flow (is it light enough to use regularly, or heavy enough to avoid?)
- The journal habit (does the journal stub make writing easy, or does the blank page create friction?)

Questions to ask: Where does Xavier shortcut? What does he skip? What would he do differently if Cici weren't watching?

### Lens 2 — Pilot member as user

A pilot member is a real person in the Philippines who forked the repo and set up their own OB1 instance. They are NOT Xavier. They:
- May not know what governed state is on Day 1
- May get stuck at the curl health check (Task 1) and never recover
- May not understand why they need to "seed" their instance
- May have a different relationship with English as the documentation language
- May be motivated by community belonging, not technical mastery

Questions to ask: What is the Day 1 experience like for someone who has never used Claude or Supabase? Where is the first point of confusion? What makes them feel like they're succeeding, not just following steps?

### Lens 3 — BrewMind visitor as user

A visitor to brewmind.cafe is encountering the public face of what Xavier and Cici are building together. They:
- Have no context for Cici, OB1, or governed state
- Are evaluating whether BrewMind is interesting / credible / worth following
- Are forming a first impression that may not match the private thinking captured in Supabase

Questions to ask: Is the public brand consistent with the private strategy? Is there a gap between what Cici knows and what BrewMind shows? Does the site reflect the current thinking, or is it 3 months behind?

---

## User story format (for this system)

```
As [Xavier / pilot member / BrewMind visitor],
I want [specific, concrete thing],
so that [named outcome that matters to this user].

Acceptance criteria:
- [ ] [Checkable condition 1]
- [ ] [Checkable condition 2]
```

**What makes an acceptance criterion checkable:**
- It can be verified by reading a file, running a command, or visiting a URL — not by asking Cici "does this work?"
- Bad: "The user understands the proposal flow."
- Good: "The user has submitted at least one proposal JSON to `proposals/queue/`."

---

## The pilot funnel (from `self-directed-learning` agent)

```
Joined → GitHub posted → Fork → Supabase created → First win
```

Each stage transition is a product problem:
- **Joined → GitHub posted:** Does the Telegram welcome message give a concrete first action?
- **GitHub posted → Fork:** Is the fork template clearly labeled? Is there a one-command setup?
- **Fork → Supabase created:** Is the Supabase setup doc clear for a non-developer?
- **Supabase created → First win:** What is "first win"? Is it defined and celebrated?
- **Silent drop-off at any stage:** What is the checkpoint message? Does it blame-frame or normalize being stuck?

To instrument the funnel: track stage transitions in `docs/work-lanes/cici-ai-progress/` using the existing applicant table format.

---

## Anti-patterns

- **Building for the ideal user** — Designing for the pilot member who completes all 5 tasks, reads every doc, and asks great questions. Real users drop off after Task 1 if it's too hard.
- **Features without user stories** — Adding a command or workflow without asking who uses it, when, and what success looks like.
- **Optimizing before measuring** — Rewriting the onboarding doc before knowing where people actually get stuck.
- **Confusing "built" with "shipped"** — A feature that exists in the repo but no pilot member has used is not shipped.
- **Xavier-as-user bias** — Designing the pilot experience based on what Xavier would find intuitive. Xavier has weeks of context; pilot members have none.

---

## Sample exercise (15–30 min)

Write 3 user stories — one for each lens — for a pilot member's first week.

Use the user story format above. For each story:
1. State which lens (Xavier / pilot member / BrewMind visitor)
2. Write the full story with acceptance criteria
3. Check: can each acceptance criterion be verified without asking Cici?

Then identify which of the 3 stories has the weakest acceptance criteria and rewrite those criteria until they're fully checkable.

Write all 3 stories in today's journal.
