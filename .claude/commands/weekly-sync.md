---
name: weekly-sync
description: Run the BrewMind weekly sync. Reads the operator daily log, open loops, proposals, and brand context, then surfaces a structured weekly summary in Cici's voice. Run this at the start of any weekly review session.
---

You are running the BrewMind weekly sync for Xavier. Follow every step exactly. Do not skip steps. Do not take actions beyond what is listed — surface findings and wait for Xavier's direction.

## Files to read (in order)

1. `docs/operator-daily-log.md` — scan the most recent 7 days of entries
2. `docs/companion-agent/brewmind-open-loops.md` — identify any open items
3. `proposals/queue/*.json` — list any pending proposals
4. `docs/brewmind.md` — brand context (skim for tone anchoring)
5. `docs/companion-agent/brewmind-companion-contract.md` — voice and lane rules

## Step 1 — Weekly activity summary

From the daily log, extract entries from the past 7 days. For each day that has an entry, pull out:
- What was shipped or decided
- Any blocker that was open

If no entry exists for a day, skip that day silently.

## Step 2 — Open loops check

From `brewmind-open-loops.md`, list every item with status `open`. If all domains are clear, say so in one line.

## Step 3 — Proposals check

From `proposals/queue/`, list every proposal with:
- `id`
- `target_surface`
- `summary`
- `status`

If the queue is empty, say so in one line.

## Step 4 — Weekly summary output

Write a single structured weekly-sync block for Xavier using this exact format:

---

**BrewMind Weekly Sync — [DATE RANGE, e.g. Apr 14–21 2026]**

**This week:**
- [bullet per meaningful ship or decision from the daily log]

**Still open:**
- [bullet per open loop item, or "Nothing open."]

**Pending proposals:**
- [bullet per proposal, or "Queue is clear."]

**Tension flags:**
- [any tensions noted in open-loops file, or "None."]

**Recommended next step:** [one sentence — the most important thing to do or decide this week]

**Lane:** PLAN — waiting for Xavier's direction.

---

Do not write anything after the sync block. Wait for Xavier to respond.

## Voice notes (read before writing the output)

- Direct and warm. BrewMind is a learning brand built by a real person — the tone is not corporate.
- Short sentences. No filler. No "As we can see..." or "It is worth noting...".
- Surface tensions honestly. If two things disagree, name both and flag it.
- Evidence tiers apply: [A] = verified by Xavier, [B] = structured doc, [C] = model recall. Do not present [C] as fact.
- If a BrewMind claim (partner, pricing, launch date) can't be traced to a governed doc, say "not in governed docs" and offer a next step.
