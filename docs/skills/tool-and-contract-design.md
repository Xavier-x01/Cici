# Skill: Tool and Contract Design

**Invoked by:** `/apply-skill tool-and-contract-design`  
**Lane:** PLAN (no writes without Xavier's explicit go-ahead)  
**When to use:** Before writing or modifying any `.claude/commands/`, `.claude/agents/`, or behavioral contract document. Use it to evaluate an existing tool for quality gaps.

---

## Why tool and contract design exists in this context

A command or agent that lacks clear inputs, outputs, lane rules, and failure modes becomes a liability — it does ambiguous things, writes to places it shouldn't, or leaves Xavier guessing whether the task is done. The companion contract (`users/cici/governed-state/workflows/companion-contract.md`) is the canonical worked example of a well-formed behavioral contract: it has explicit lane rules, enumerated anti-patterns, and named failure modes.

Tool and contract design is the discipline of writing tools that are safe, composable, and predictable.

---

## Anatomy of a well-formed command

Every `.claude/commands/<name>.md` file should have:

```
---
name: <slug>
description: <one sentence — what it does and when to use it>
argument-hint: <arg>     ← include if the command takes an argument
---

## Step 1 — <action>
## Step 2 — <action>
...
## Step N — Wait
Do not act further. Present output and wait for Xavier's decision.
```

| Element | What it must contain |
|---|---|
| `description` | Enough context to appear in `/help` and be useful at a glance |
| Steps | Numbered, sequential, each with a single clear outcome |
| Wait step | Always the last step — commands present; they do not act autonomously |
| Done state | At least one checkable condition that tells Xavier the command succeeded |

---

## Anatomy of a well-formed agent

Every `.claude/agents/<name>.md` file should have:

```
---
name: <slug>
description: <one sentence — what it does, when to spawn it>
tools: <comma-separated list — only what it needs>
model: sonnet
---

## North star / purpose
## Lane declaration (PLAN / EXECUTE / DOCSYNC)
## What the agent may write to
## What the agent must NOT write to
## Behavioral rules
## Anti-patterns
```

| Element | What it must contain |
|---|---|
| `tools` | Minimal — only the tools the agent actually needs |
| Write-class declaration | Explicit paths it may write to; everything else is off-limits |
| Lane default | PLAN unless there is a strong reason for EXECUTE |
| Anti-patterns | At least 2; name the failure modes you've observed or anticipated |

---

## Contract design checklist

Use this before shipping any new command, agent, or behavioral contract:

- [ ] **Clear input** — Is the argument or trigger condition explicit? No ambiguous entry points.
- [ ] **Clear output** — Does the tool produce a specific, describable artifact (task card, report, proposal JSON)?
- [ ] **Lane declared** — Is the default lane stated? Does the tool only change lanes when Xavier says so?
- [ ] **Write-class limited** — Does the tool only write to paths it explicitly claims ownership of?
- [ ] **Done state defined** — Can Xavier check whether the tool succeeded without asking Cici?
- [ ] **Wait step present** — Commands and agents present results and pause; they don't chain autonomously.
- [ ] **Anti-patterns listed** — At least 2 named failure modes the tool designer thought about.
- [ ] **No hardcoded facts** — No business facts (pricing, partner names, dates) embedded in behavior files.

---

## The companion contract as worked example

`users/cici/governed-state/workflows/companion-contract.md` is the gold standard because it has:
- Named lanes (PLAN / EXECUTE / DOCSYNC / EXECUTE_LOCAL) with explicit switching rules
- Enumerated anti-patterns (9 of them)
- Explicit abstention policy ("say not in governed docs" rather than inventing)
- Approval ceremony: echo proposal id + summary, then stop and wait

When designing a new contract, read it first. Ask: does my new tool have equivalents of each of these?

---

## Anti-patterns

- **Vague steps** — "Explore X" or "Handle the output." Every step should have a single, observable outcome.
- **Missing wait step** — A command that takes action after presenting results without waiting. Removes Xavier's control.
- **Overloaded tools** — One agent doing search + analysis + writing + pushing. Split into composable units.
- **Tools writing outside their class** — An agent that "may only write to `evidence/`" but also writes to `proposals/queue/`. The write-class declaration means nothing if not enforced.
- **Description that describes the implementation** — "Reads files and runs search and synthesizes output." Write what it's FOR, not what it does mechanically.

---

## Sample exercise (15–30 min)

Evaluate `daily-task.md` against the contract design checklist above.

For each checklist item, mark pass / fail / partial and write one sentence explaining why. If you find a gap, write a one-line fix for it (don't apply it — just note what the fix would be).

Then do the same for one agent of your choice from `.claude/agents/`.

Write your evaluation in the work journal for today.
