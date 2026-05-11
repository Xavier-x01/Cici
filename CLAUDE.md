# CLAUDE.md — Context for Claude Code Sessions

This file gives Claude Code context about this repository so it can assist effectively.

---

## What This Repo Is

`xavier_self` is a personal instance of [Open Brain (OB1)](https://github.com/NateBJones-Projects/OB1) — a self-owned AI memory system. It is primarily a **configuration and documentation repository**. The runtime server code is deployed as a Supabase Edge Function and is not stored here.

## Project Purpose

- Provide a persistent, cross-AI knowledge base (thoughts, notes, context)
- Connect to Claude, ChatGPT, Cursor, and other MCP clients
- All data lives in a personal Supabase project (PostgreSQL + pgvector)

## Key Facts

- **No application code lives in this repo** — the server is deployed upstream from NateBJones-Projects/OB1
- **Database**: Supabase (PostgreSQL with pgvector extension)
- **Server**: Supabase Edge Function (Deno/TypeScript) at `open-brain-mcp`
- **Protocol**: MCP over HTTP (query-param key auth)
- **AI Gateway**: OpenRouter for embeddings and model routing
- **Cost**: ~$0.10/month at personal scale

## Directory Structure

Key directories for AI orientation:

| Directory / File | Purpose |
|---|---|
| `.claude/agents/` | Sub-agents (7); invoked via the Agent tool |
| `.claude/commands/` | Slash commands (10); invoked with `/` |
| `.claude/modes/` | Thin mode checklists for focused passes |
| `config/` | Authority map and surface configuration |
| `docs/` | Architecture docs, companion contract, work lanes, personal journals |
| `docs/work-lanes/` | Active work lanes hub (3 lanes) |
| `evidence/` | Raw imports and captured thoughts (immutable once written) |
| `goals/` | Goal manifesto and alignment targets |
| `prepared-context/` | Normalized context staged for review |
| `proposals/` | Proposal queue (`queue/`) and schemas (`schemas/`) |
| `scripts/` | Utility scripts — CI validator, dossier, search, evidence tools |
| `users/cici/governed-state/` | Canonical durable state (owner-approved changes only) |

## Environment Variables / Secrets (in Supabase)

| Secret name | Description |
|---|---|
| `MCP_ACCESS_KEY` | 64-char hex key securing the MCP endpoint |
| `OPENROUTER_API_KEY` | OpenRouter API key for embeddings |
| `SUPABASE_URL` | Auto-injected by Supabase Edge Functions runtime |
| `SUPABASE_SERVICE_ROLE_KEY` | Auto-injected by Supabase Edge Functions runtime |

## Common Tasks

### Re-deploy the MCP server after upstream updates

```bash
cd <your-project-folder>
curl -o supabase/functions/open-brain-mcp/index.ts \
  https://raw.githubusercontent.com/NateBJones-Projects/OB1/main/server/index.ts
supabase functions deploy open-brain-mcp --no-verify-jwt
```

### Rotate the access key

```bash
openssl rand -hex 32   # generate new key
supabase secrets set MCP_ACCESS_KEY=<new-key>
supabase functions deploy open-brain-mcp --no-verify-jwt
# Update the key in your AI client MCP connection URL
```

### Rotate the OpenRouter key

```bash
supabase secrets set OPENROUTER_API_KEY=<new-key>
```

### Verify the server is alive

```bash
curl "https://YOUR_PROJECT_REF.supabase.co/functions/v1/open-brain-mcp?key=YOUR_ACCESS_KEY"
```

## CI / Validation Gate

A GitHub Actions workflow runs on every push or PR touching `proposals/**`, `users/**`, `config/**`, or `scripts/validate-governed-state.py`.

| Step | Detail |
|---|---|
| Runner | `ubuntu-latest` |
| Python | 3.11 |
| Command | `python3 scripts/validate-governed-state.py` |

The validator checks JSON syntax, required directories, schema conformance, and surface-map integrity. A failing CI run means a governed-state artifact is malformed — do not merge until it passes.

## Utility Scripts

Scripts live in `scripts/`. Run from the repo root.

| Script | Purpose |
|---|---|
| `validate-governed-state.py` | CI validator — JSON, schema, required dirs, surface-map |
| `generate-dossier.py` | Full pipeline health dossier + Tier C leak audit |
| `deep-search-report.py` | Multi-pass search synthesis from MCP results |
| `extract-evidence.py` | Extract + normalize Supabase exports into `evidence/` |
| `ai-goal-check.py` | Check an action against manifesto alignment goals |
| `daily_journal_helper.py` | Scaffold today's daily journal entry from template |
| `doctor.sh` | Bash repo health check |
| `janitor/` | Transient memory purge utilities (dry-run default) |

## Architecture Reference

See [README.md](README.md) for the full architecture diagram.

## Setup Reference

See [docs/setup-guide.md](docs/setup-guide.md) for the complete beginner setup walkthrough.

## Session Bootstrap Prompt

See [docs/session-bootstrap-prompt.md](docs/session-bootstrap-prompt.md) for a copy-paste prompt that gives any AI tool (Claude, ChatGPT, Cursor) instant full context on Cici and BrewMind.

## Governed State (Phase 2 — Formation + Review)

This repo is in **Phase 2 (Formation + Review)** of the governed-state lifecycle. Key locations:

| Path | Purpose |
|---|---|
| `users/cici/governed-state/` | Canonical durable state for this instance |
| `proposals/queue/` | Pending proposals — agents write here, owner approves |
| `proposals/schemas/proposal.schema.json` | Proposal format |
| `config/authority-map.json` | Who may write what |
| `docs/governed-state-doctrine.md` | Architectural doctrine |
| `docs/seed-phase.md` | Instance initialization walkthrough |
| `scripts/validate-governed-state.py` | Run to validate artifacts |

Supabase remains the primary runtime. The governed-state layer is additive — it does not change how Supabase or MCP work.

When proposing material changes to governed state, create a JSON file in `proposals/queue/` following the schema in `proposals/schemas/proposal.schema.json`. Do NOT write directly to `users/cici/governed-state/` unless the change is small and obvious.

### Work Lanes

Active coordination surfaces. Hub: `docs/work-lanes/README.md`.

| Lane | Scope |
|---|---|
| `cici-ai-core` | Repo architecture, governed-state, prompts, technical implementation |
| `cici-ai-progress` | Member progress, applicant table, cohort metrics, proof packets |
| `cici-ai-telegram` | Telegram group operations, posts, norms, applicant intake |

Lane files summarize and route; they must not silently rewrite governed-state or applicant facts.

## Session Behavior

- **Git / fork context:** Assume Xavier may be learning git workflows. Before any git advice, restate the current branch and remote in one line (e.g. "You're on `main`, tracking `origin/main`"). Link to `docs/personal/intentions-and-preferences.md` for fuller context on collaboration style.
- **Disagreement:** Raise at most one concise challenge per decision point, then implement Xavier's chosen direction unless the action is blocked by a policy constraint or would expose secrets.
- **Plan-mode-first:** Begin complex or ambiguous tasks in Plan mode (shift+tab twice in the CLI, or state the plan before acting). Switch to edits only once the approach is confirmed. This enforces the PLAN lane default.

## Available Slash Commands

These commands live in `.claude/commands/` and can be invoked with `/`:

| Command | Purpose |
|---|---|
| `/session-start` | Run the startup ceremony: reads open proposals, open loops, surfaces status paragraph |
| `/deep-search <query>` | Multi-pass AI-augmented search — decomposes query, scans governed-state, runs parallel MCP searches, surfaces gaps and tensions, produces tier-annotated synthesis |
| `/draft-proposal <surface>` | Scaffold a new proposal for a governed-state surface |
| `/review-governed-change <proposal-id>` | Evaluate a queued proposal and wait for Xavier's decision |
| `/promote-to-governed-state <proposal-id>` | Apply an approved proposal to the correct surface |
| `/stage-evidence [tag]` | Stage Supabase export into evidence/ and prepared-context/ |
| `/memory-audit` | Run a full pipeline and Tier C leak audit |
| `/self-improve` | Run a behavioral self-improvement cycle — identifies gaps in how Cici acts and proposes concrete changes |
| `/weekly-review` | Run the weekly synthesis ritual — reads journal entries, surfaces BrewMind open loops, and prompts for knowledge worth capturing into memory |
| `/daily-task` | Generate today's AI skill-building task for Xavier and log it to the work journal |

## Available Agents

These agents live in `.claude/agents/` and can be invoked via the Agent tool:

| Agent | Tools | Purpose |
|---|---|---|
| `proposal-reviewer` | Read-only | Evaluates queued proposals; flags issues |
| `evidence-stager` | Read + Write (evidence/ + prepared-context/ only) | Stages and synthesizes evidence |
| `memory-auditor` | Read-only | Monthly hygiene audit; finds Tier C leaks |
| `dev-hygiene` | Read + Write + Bash | Doctor check, batch workers, mode checklists — one command for repo health |
| `self-improver` | Read + Write + Bash | Behavioral self-improvement cycle — reviews Cici's own instructions and proposes improvements |
| `deep-searcher` | Read-only | Multi-pass deep search — query decomposition, governed-state cross-reference, gap/tension analysis, tier-annotated synthesis |
| `self-directed-learning` | Read, Write, Bash, Glob, Grep | Xavier's learning partner and community pilot co-pilot. Discovers, documents, and ships experiments — teaches in-repo habits, tracks pilot funnel metrics, and drafts outreach copy. Defaults to PLAN lane. |

## Agent Modes

Thin checklists for focused passes. Live in `.claude/modes/`; do not duplicate CLAUDE.md.

| Mode file | When to use |
|---|---|
| `_shared.md` | Always-true context (paths, owner, no-secrets) — referenced by other modes |
| `batch-ingest.md` | Processing multiple `prepared-context/` files in one bounded pass |
| `proposal-review.md` | Focused pass over `proposals/queue/` (evaluate, not apply) |
| `docsync-pass.md` | Docs-only updates: stale links, path refs, header sync |

_Routines inspired by [career-ops](https://github.com/santifer/career-ops) layout (external reference; not a dependency)._

## Common Errors (Do Not Repeat)

_This section is a living log. Add entries when Claude makes a mistake Xavier should not see again._

- **Do not cite Supabase recall as fact.** MCP search results and `recent_thoughts` are Tier C. Always annotate and offer a verification step.
- **Do not write to governed-state surfaces without a proposal.** Even obvious improvements need the proposal → approval flow unless Xavier explicitly says "direct edit is fine."
- **Do not generate pricing, partner commitment, or launch date language** without an explicit Tier A or B source and Xavier's go-ahead.

## BrewMind companion defaults

Full contract: [`docs/companion-agent/brewmind-companion-contract.md`](docs/companion-agent/brewmind-companion-contract.md) _(working reference — not yet canonical governed state)_

- **Startup reads (every session):** `CLAUDE.md` → `proposals/queue/*.json` → `docs/companion-agent/brewmind-open-loops.md`. Surface a one-paragraph status before acting.
- **Default lane: PLAN.** Read and propose freely. Only write to governed state or commit/push when Xavier explicitly says so (EXECUTE lane). Docs-only changes use DOCSYNC.
- **No retrieval-as-truth.** MCP search results (`search`, `recent_thoughts`) and Supabase captures are **Tier C** inputs — useful context, not business facts. Never cite them as confirmed decisions without a Tier A or B source.
- **Three evidence tiers:** `[A]` = Xavier verified / primary source. `[B]` = structured summary of A or third-party doc with traceable source. `[C]` = model synthesis, brainstorm, unverified recall. Tier C never becomes a public promise or pricing claim without promotion to A or B.
- **Abstain when unverified.** If a BrewMind fact (partner status, pricing, launch date) cannot be traced to a governed doc or working file, say "not in governed docs / not verified" and offer a named next step.
- **Proposal echo before governed-state changes.** Cite a proposal id (or create `proposals/queue/prop-YYYYMMDD-NNN-*.json`), give a one-line summary of what changes on which surface, then stop and wait for Xavier's decision.
- **Record tensions, never silently resolve them.** If two sources disagree, name both, add a `Tension:` annotation, and suggest a resolution path. Log in `docs/companion-agent/brewmind-open-loops.md`.
- **Relationship-first.** BrewMind involves real partners and community. Before drafting anything involving other people, ask: would this feel respectful if Xavier read it aloud to a partner?
