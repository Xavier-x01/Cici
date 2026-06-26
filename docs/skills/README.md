# Operator Skills

This directory contains portable, step-by-step operator protocols for Cici's governed-formation pipeline.

Skills are **human-readable procedures** — not code. They describe what a person (or an agent operating with human oversight) should do to accomplish a specific governed-formation task.

Skills can be invoked interactively in any session using `/apply-skill <skill-name>` (for the 7 advanced skills listed below).

## Pipeline Skills

| Skill | File | Purpose |
|---|---|---|
| Draft a Proposal | `draft-proposal.md` | Create a formal change proposal for governed state |
| Stage Evidence | `stage-evidence.md` | Extract and stage runtime memories for review |
| Review a Governed Change | `review-governed-change.md` | Evaluate and decide on a proposal in the queue |
| Promote to Governed State | `promote-to-governed-state.md` | Apply an approved proposal to governed-state surfaces |
| Memory Hygiene Audit | `memory-hygiene-audit.md` | Identify and process promotion candidates from runtime memory |

## Advanced Skills (invoke with `/apply-skill <name>`)

| Skill | File | What it covers in Cici's context |
|---|---|---|
| System Design | `system-design.md` | Where new capabilities belong: command, agent, governed-state, or Supabase |
| Tool and Contract Design | `tool-and-contract-design.md` | Writing commands and agents that are safe, composable, and predictable |
| Retrieval Engineering | `retrieval-engineering.md` | Improving captures so future MCP searches return relevant results |
| Reliability Engineering | `reliability-engineering.md` | Understanding and recovering from pipeline failures |
| Security and Safety | `security-and-safety.md` | Secrets, governed-state integrity, and epistemic safety |
| Evaluation and Observability | `evaluation-and-observability.md` | Measuring whether Cici is actually working |
| Product Thinking | `product-thinking.md` | Designing for real users: Xavier, pilot members, BrewMind visitors |

## Relationship to Cursor Rules

`.cursor/rules/operators.mdc` contains quick-reference versions of these protocols.
These docs contain the full, annotated versions.

## Relationship to Governed Workflows

When a skill becomes a stable recurring flow, it should be proposed as a canonical workflow artifact in `users/cici/governed-state/workflows/`.

Skills are operator-facing documentation. Workflow surface artifacts are Cici-canonical declarations.
