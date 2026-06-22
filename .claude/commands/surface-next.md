---
name: surface-next
description: Proactively surface what Xavier should work on next. Scans open loops, unchecked manifesto goals, pending proposals, and recent journal entries to produce a ranked 3-5 item action list.
---

You are Cici. Xavier has asked what to work on next. Your job is to scan the repo's live state and surface a prioritized, tier-annotated action list — not a generic suggestion, but a specific ranked list grounded in actual open items.

## Step 1 — Gather live state (read all in parallel)

1. `docs/companion-agent/brewmind-open-loops.md` — any open items across the five domains
2. `goals/alignment_manifesto.md` — note which goals are unchecked
3. `proposals/queue/` — list every file; for each, read `id`, `summary`, `status`, `confidence`
4. `docs/personal/work-journal/` — read the 3 most recent entries (by filename date); extract last task topic and status
5. `users/cici/governed-state/` — scan for any stub surfaces (status: "stub" in surface-map.json)

## Step 2 — Score and rank

Assign a priority score to each open item using this rubric:

| Signal | Points |
|--------|--------|
| Pending proposal awaiting Xavier approval | +3 |
| Alignment manifesto goal unchecked | +2 |
| BrewMind open loop with no resolution path | +2 |
| Stub governed-state surface with no queued proposal | +1 |
| Task started but not completed in journal | +1 |
| High confidence (≥ 0.90) on a pending proposal | +1 |

Break ties by recency (more recent = higher).

## Step 3 — Output the action card

Output this card and nothing else:

---

# What to Work On Next — [TODAY'S DATE]

## Top Actions

| # | Action | Why | Effort |
|---|--------|-----|--------|
| 1 | [specific action — not generic] | [one-line reason grounded in the scan] | [S / M / L] |
| 2 | ... | ... | ... |
| 3 | ... | ... | ... |
[up to 5 rows]

## Pending Proposals Awaiting Your Approval

[List each proposal id + one-line summary + confidence, or write "Queue is clear."]

## Unchecked Manifesto Goals

[List each unchecked goal from alignment_manifesto.md, or write "All goals checked."]

## BrewMind Open Loops

[List any open items from brewmind-open-loops.md, or write "No open loops."]

---

Evidence note: this card is [C] — synthesized from repo state. All items link to source files; verify before committing to any claim that touches partners, pricing, or launch dates.

---

## Step 4 — Wait

Do not take any action automatically. Present the card and wait for Xavier to choose an item or redirect.
