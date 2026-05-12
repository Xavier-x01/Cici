# Task 3 — Capture Your Context

**Phase:** 1 — Personal OB1  
**Prerequisite:** Task 2 complete (OB1 connected in your AI client)  
**Estimated time:** 20–40 minutes

---

## Goal

Build a meaningful personal knowledge base by storing at least 10 thoughts about yourself. This is your OB1 instance learning who you are. After this task, your AI client can search your own context and give you more relevant responses.

---

## What to Capture

Store at least 10 thoughts covering these categories. One thought per bullet is enough — be honest, be brief.

**About you (pick 2–3):**
- Your name and where you're from
- Your technical background — what you know, what you're learning
- The tool or language you're most comfortable with
- Something you're working on right now (job, project, school, side hustle)

**Your goals (pick 2–3):**
- What you want to be able to do with AI in 3 months
- One skill you're actively building
- One problem you want to solve for yourself or others

**Your current project or learning focus (pick 2–3):**
- What you're building or studying
- The hardest part you're facing
- A resource or approach that's helping

**Anything else (1–2):**
- A principle you work by
- A question you can't stop thinking about

---

## How to Capture

In your AI client, ask Claude (or Cursor) to capture each thought:

> "Capture this into my OB1: I am a backend developer based in Manila. My strongest language is Java and I'm learning Python."

OB1 will auto-generate an embedding and store it. No JSON needed — just ask.

You can capture all 10 in one session, or spread it out. Consistency matters more than perfection.

---

## Verify

After capturing, ask your AI client:

> "Search my OB1 for thoughts about my skills."

You should see your entries come back in the search results. If they don't appear, check that the `capture` tool ran successfully (look for a confirmation from OB1 in the chat).

---

## Proof

Screenshot of `recent_thoughts` or a `search` result showing at least 10 entries.

**Option A — Telegram:** Post the screenshot with your name + "Task 3 done — 10+ thoughts captured."

**Option B — GitHub:** Create `proof/task-03/README.md` in your fork:
```
10+ personal context thoughts captured on YYYY-MM-DD. Covers: [brief list, e.g. skills, goals, current project].
```

---

## Why This Matters

Everything you capture here will be available in Phase 2 when we build the shared cici-ai instance. The habit of capturing your thinking is the core skill this whole system is built on.
