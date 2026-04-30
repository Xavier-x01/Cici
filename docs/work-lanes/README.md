# Work Lanes

Lightweight coordination surfaces for Cici's active areas of work. Each lane owns a focused scope, tracks open loops, and surfaces the next action.

## Lane Hub

| Lane | Purpose | Primary questions |
|---|---|---|
| [`cici-ai-telegram`](cici-ai-telegram/README.md) | Telegram group operations, posts, norms, applicant intake, and communication. | What should be posted? Who needs a reply? What needs recording from chat? |
| [`cici-ai-core`](cici-ai-core/README.md) | Cici/OB1 architecture, prompts, governed-state, repo migration, safety, and technical implementation. | What should change in the repo? What needs proposal/approval? What is safe to automate? |
| [`cici-ai-progress`](cici-ai-progress/README.md) | Member progress, applicant table, task completion, proof packets, scholarships, and cohort metrics. | Who has done what? What is the next task? What evidence supports the status? |

## Boundary Rule

Lane files may summarize, stage, and route. They must not silently rewrite governed-state, applicant claims, payment commitments, or identity facts.

Material changes to governed-state must follow the proposal → approval flow documented in [`docs/governed-state-doctrine.md`](../governed-state-doctrine.md).
