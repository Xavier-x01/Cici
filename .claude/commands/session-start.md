---
name: session-start
description: Run the required startup ceremony for every Cici/BrewMind session. Reads open proposals, open loops, and surfaces a one-paragraph status before acting.
---

You are starting a Cici session. Follow the startup ceremony defined in the companion contract exactly.

## Step 1 — Read open proposals

Read every file in `proposals/queue/` and list each proposal with:
- `id`
- `target_surface`
- `summary`
- `status`

If the queue is empty, note that explicitly.

## Step 2 — Read open loops

Read `docs/companion-agent/brewmind-open-loops.md`. If the file does not exist, create it as a stub:

```markdown
# BrewMind Open Loops

_No loops recorded yet. Add entries as threads open._

## Format

Each entry:
- **Domain**: e.g. Partnership, Pricing, Content, Site, Operations
- **Thread**: Short description
- **Last updated**: YYYY-MM-DD
- **Status**: open | resolved | deferred
```

Then note the file was created as a DOCSYNC action.

## Step 3 — Read open research questions

Read `users/cici/governed-state/research-methodology/open-questions.json`. List each question where `status` is `"open"` or `"investigating"` with its `id`, `question`, and `status`. If no questions are active, note that explicitly.

## Step 4 — Read CLAUDE.md

Confirm you have read `CLAUDE.md` and note the current default lane (PLAN).

## Step 5 — Surface status paragraph

Write a single paragraph to Xavier that covers:
1. Number of open proposals and their target surfaces (or "queue is clear")
2. Active open loops (or "no open loops")
3. Open research questions (ids + one-line summary of each, or "no open questions")
4. Any tensions noted in `docs/companion-agent/brewmind-open-loops.md`
5. Current lane: PLAN (unless Xavier has already said otherwise)

Do not take any action after this — wait for Xavier's direction.
