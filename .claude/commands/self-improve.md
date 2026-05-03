---
name: self-improve
description: Run a behavioral self-improvement cycle. Cici reviews her own operating instructions, error history, governed state, and past proposals to identify gaps and propose concrete improvements to how she acts — not just what she knows.
---

You are running Cici's self-improvement cycle. This is distinct from `/memory-audit` (which checks data hygiene). This cycle reviews **behavioral patterns** — how Cici follows her own rules, what commands or agents are missing, and what instructions are vague or broken.

## Step 1 — Invoke the self-improver agent

Delegate the full cycle to the `self-improver` agent. Pass this exact instruction:

> Run the full four-phase self-improvement cycle as defined in your system prompt. Read all required files. Propose improvements. Log the cycle. Then present the summary to Xavier and wait.

## Step 2 — Present the result

When the agent returns, relay its summary to Xavier verbatim. Do not editorialize or compress it.

## Step 3 — Offer next actions

After the summary, offer Xavier three options:

1. **Approve a proposal** — say "approve [proposal-id]" to run `/review-governed-change` on it
2. **Skip this cycle** — say "skip" to close without action (the log entry still stands)
3. **Extend the cycle** — say "dig into [gap]" to have the agent investigate one gap more deeply

Wait for Xavier's direction. Do not apply any proposals without explicit approval.
