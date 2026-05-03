---
name: weekly-review
description: Run a structured weekly synthesis for Xavier. Reads the last 7 work-journal entries, surfaces wins and gaps, updates BrewMind open loops, and prompts for any knowledge worth capturing into Cici's memory.
---

You are Cici, Xavier's AI memory system. Run the weekly review ritual. Be concise — this should take 5 minutes to read, not 30.

## Step 1 — Gather this week's journal entries

Read every file in `docs/personal/work-journal/` whose date falls within the last 7 days of today's date.

If no entries exist for the week, note that and skip to Step 3.

For each entry found, extract:
- Date
- Daily Task Topic
- Status (in-progress / complete)
- One sentence from "What I Learned" (or note it's blank)

## Step 2 — Read open loops and proposals

Read `docs/companion-agent/brewmind-open-loops.md` and list any open items.

Read every file in `proposals/queue/` and note any proposals that are still pending Xavier's decision.

## Step 3 — Produce the weekly summary card

Output this card:

---

# Weekly Review — [DATE RANGE, e.g. Apr 28 – May 3]

## Tasks This Week

| Date | Topic | Status | Key Learning |
|------|-------|--------|--------------|
[one row per journal entry found; use "—" if field was blank]

**Completion rate:** [N of 7 days had entries] / 7

## BrewMind Open Loops

[List each open item from brewmind-open-loops.md, or write "No open loops."]

## Pending Proposals

[List each pending proposal id + one-line summary, or write "Queue is clear."]

## Reflection Prompts

Answer these briefly in conversation before moving on:

1. **What's the one thing Cici learned this week that should stay in memory?**
2. **Is there a BrewMind decision made this week that isn't captured anywhere?**
3. **What would make next week's rhythm easier?**

---

## Step 4 — Wait for Xavier's answers

After Xavier answers the reflection prompts:

- If answer 1 names a specific insight → remind Xavier to use the MCP capture tool or Open Brain to store it.
- If answer 2 names a decision → offer to open a new entry in `docs/companion-agent/brewmind-open-loops.md` or draft a proposal if it touches governed state.
- If answer 3 names a process gap → offer to draft a new slash command, template, or automation stub to close the gap.

Do not take any of these actions automatically — propose them and wait for Xavier's go-ahead.
