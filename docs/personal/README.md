# Xavier's Personal Goals & Workflow

This document describes how Xavier uses Open Brain alongside BrewMind and what this stack is meant to support long-term.

---

## Who This Is For

This is a private working document for Xavier (@Xavier-x01). It is committed to version control so context is never lost between AI sessions, but it contains **no secrets** — all keys and credentials live in Supabase secrets or a local password manager, never in git.

---

## Goals

### 1. BrewMind Growth
[BrewMind](https://brewmind.cafe) is Xavier's café / learning-brand business. Open Brain serves as the persistent memory layer for:
- Capturing ideas, decisions, and lessons learned as BrewMind evolves
- Storing brand voice notes, content drafts, and research that any connected AI can retrieve
- Building a searchable history of what has been tried, decided, and why

### 2. Consistent Capture into Open Brain
The habit goal: any insight worth keeping — from a conversation, a session with an AI, or real-world experience — gets captured into Open Brain via the `capture` MCP tool. This keeps the knowledge base growing and makes future AI sessions more contextually aware.

### 3. Safe Key Handling
All secrets (Supabase keys, MCP access key, OpenRouter key) are stored **only** in:
- Supabase project secrets (for the deployed Edge Function)
- A local password manager or `.env` file that is **excluded by `.gitignore`**

Nothing sensitive is ever committed to `xavier_self` or `open-brain-xavier`. If a key needs rotation, follow the steps in [`docs/setup-guide.md`](../setup-guide.md).

---

## Work Lanes

Active coordination surfaces for Cici's work areas: Telegram, core governance, and progress tracking. See [`docs/work-lanes/README.md`](../work-lanes/README.md).

---

## Repository Map

| Repo | Purpose |
|---|---|
| [`xavier-x01/xavier_self`](https://github.com/Xavier-x01/xavier_self) | This repo — instance docs, configuration notes, personal context |
| [`xavier-x01/open-brain-xavier`](https://github.com/Xavier-x01/open-brain-xavier) | Fork of OB1 server code — deploy from here, pull upstream updates here |
| [`xavier-x01/brew_mind`](https://github.com/Xavier-x01/brew_mind) | BrewMind public site (HTML / GitHub Pages) at [brewmind.cafe](https://brewmind.cafe) |
| [`NateBJones-Projects/OB1`](https://github.com/NateBJones-Projects/OB1) | Upstream Open Brain — never commit personal changes here |

---

## Branch Convention (open-brain-xavier)

| Branch | Purpose |
|---|---|
| `main` | Stays clean and in sync with upstream (`NateBJones-Projects/OB1`) |
| `xavier/experiments` | Scratch branch for local experiments — never merged to main without review |
| `xavier/<feature-name>` | Named branches for specific personal changes (e.g. `xavier/brewmind-metadata`) |

**Rule:** Before pulling upstream updates, check out `main`, run `git pull upstream main`, then rebase any `xavier/*` branch on top of the updated `main`. This keeps the fork mergeable and avoids conflicts accumulating silently.

```bash
# Staying in sync with upstream
git checkout main
git pull upstream main
git push origin main

# Rebase a personal branch on updated main
git checkout xavier/my-feature
git rebase main
```

---

## BrewMind ↔ Open Brain Integration (Today's Scope)

For now the two systems are **linked by documentation and habit, not code**:
- BrewMind ideas and decisions get captured via `capture` MCP tool during AI sessions
- The BrewMind public site (`brew_mind` repo / `brewmind.cafe`) remains fully separate from the Open Brain server stack
- No BrewMind files live inside `open-brain-xavier` — upstream compatibility is preserved

Future (tracked here when decided, not built speculatively):
- BrewMind-specific metadata tags on captured thoughts (e.g. `{"source": "brewmind"}`)
- Scheduled capture prompts for weekly BrewMind review sessions

---

## Definition of Done (Session: Rename + Personalize)

- [x] OB1 fork renamed to `open-brain-xavier` on GitHub
- [x] Local remote `origin` updated to new fork URL
- [x] `upstream` remote confirmed pointing at `NateBJones-Projects/OB1`
- [x] `xavier_self/README.md` updated with Xavier's instance header + BrewMind link
- [x] `docs/personal/README.md` created (this file)
- [x] `.gitignore` added — covers `.env`, Supabase secrets, key files
- [ ] `open-brain-xavier` fork README updated with "Xavier's fork" overlay (see instructions below)
- [x] No secrets committed to any repo

### Adding the fork README overlay (open-brain-xavier)

Since `open-brain-xavier` is not in this workspace, run these commands inside that repo:

```bash
cd ~/path/to/open-brain-xavier

# Create or edit README.md — prepend the Xavier's Fork section
# (See the draft content below, or copy from xavier_self docs)

git add README.md
git commit -m "docs: add Xavier's fork overlay to README"
git push origin main
```

Fork README top section to prepend:

```markdown
# open-brain-xavier — Xavier's Fork of Open Brain

> **Personal fork** of [NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1).
> Instance docs: [xavier-x01/xavier_self](https://github.com/Xavier-x01/xavier_self) ·
> Business brand: [BrewMind](https://brewmind.cafe)

This fork is maintained by [@Xavier-x01](https://github.com/Xavier-x01).
`main` stays in sync with upstream. Personal changes live on `xavier/*` branches.
See [xavier_self/docs/personal/README.md](https://github.com/Xavier-x01/xavier_self/blob/main/docs/personal/README.md) for workflow notes.

---
```
