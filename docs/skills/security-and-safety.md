# Skill: Security and Safety

**Invoked by:** `/apply-skill security-and-safety`  
**Lane:** PLAN (no writes without Xavier's explicit go-ahead)  
**When to use:** When rotating secrets, auditing agent write-class rules, reviewing what a fork inherits before sharing it, or designing any feature that touches access control or data boundaries.

---

## Why security and safety exist in this context

"Security" in most systems means preventing unauthorized external access. In Cici's system, the risks are different: the main threats are internal — accidentally leaking secrets into the repo, treating unverified Tier C data as fact, or bypassing the proposal gate and writing directly to governed state. Safety is as much epistemic (what we claim to know) as it is technical (what we expose).

---

## The four safety mechanisms

| Mechanism | Protects against | How it works |
|---|---|---|
| Proposal → approval gate | Unauthorized governed-state changes | No write to `users/cici/governed-state/` without a `proposals/queue/` JSON and Xavier's explicit approval |
| Evidence tier annotations [A/B/C] | Tier C promoted as fact | Every BrewMind claim must carry an inline tier tag; absence of a tag is itself an error |
| `.gitignore` + secrets in Supabase | Secrets committed to the repo | `MCP_ACCESS_KEY` and `OPENROUTER_API_KEY` live in Supabase secrets, never in tracked files |
| Write-class rules in agent definitions | Agents overwriting what they shouldn't | Each `.claude/agents/*.md` declares explicit paths it may and may not write to |

If any of these four mechanisms is bypassed, the system is less safe — not just by degree but categorically.

---

## Threat model for a personal AI memory system

| Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Secret key in a tracked file | Medium (easy mistake) | High — anyone with repo access can read it | Supabase secrets; `.gitignore`; check before push |
| Tier C cited as a confirmed decision | High (happens often) | Medium — bad decisions made on wrong info | Mandatory inline tier annotations |
| Governed-state drift | Medium | High — Cici's identity/policy becomes unreliable | Proposal → approval gate |
| Pilot member fork inheriting private data | Low | High — Xavier's memory exposed to strangers | Fork template audit before sharing |
| Agent writing outside its declared class | Low | High — unpredictable side effects | Write-class declaration + review |

---

## Secret rotation protocol

Reference: `CLAUDE.md` → "Common Tasks" → "Rotate the access key"

**When to rotate `MCP_ACCESS_KEY`:**
- Any time a key may have been exposed (logged in a chat, pasted in a public place)
- Every 3–6 months as routine hygiene

**Rotation steps:**
```bash
openssl rand -hex 32          # generate new key
supabase secrets set MCP_ACCESS_KEY=<new-key>
supabase functions deploy open-brain-mcp --no-verify-jwt
# Update the key in your AI client MCP connection URL
```

**When to rotate `OPENROUTER_API_KEY`:**
- Same triggers as above
```bash
supabase secrets set OPENROUTER_API_KEY=<new-key>
```

Never paste these keys into a commit message, a Telegram post, a Claude chat, or any tracked file.

---

## Community pilot isolation

Before sharing a fork template with pilot members:

| Check | What to verify |
|---|---|
| No secrets in tracked files | `git grep -r "MCP_ACCESS_KEY\|OPENROUTER_API_KEY"` returns nothing |
| No personal journal entries | `docs/personal/` is either excluded or cleared |
| No private governed-state content | `users/cici/governed-state/` contains only structural templates, no Xavier's private decisions |
| No Supabase URL or project ref | Neither the URL nor the project ref should be hardcoded anywhere |
| `.env.example` provided | A template file showing which secrets are needed, with placeholder values |

A pilot member's fork should be a clean structural scaffold — no Xavier's memory, no Xavier's keys.

---

## Agent write-class audit

Every agent file should answer these questions explicitly:

1. What paths may this agent write to?
2. What paths is this agent explicitly prohibited from writing to?
3. Does the agent have access to Bash? (If yes, can it bypass write-class limits via shell?)
4. Does the agent have a lane declaration?

Run this audit on any agent before expanding its `tools` list or giving it new permissions.

---

## Anti-patterns

- **"It's just a personal project" exemption** — Personal projects are more vulnerable to lazy security habits, not less. The pilot creates real exposure.
- **Committing a `.env` file** — Even if immediately deleted, it exists in git history.
- **Tier C promoted without verification** — Citing a Supabase capture as a confirmed partner commitment or pricing decision.
- **Agents with `tools: *`** — Wildcard tool access means an agent can write anywhere, push to GitHub, delete files. Only `dev-hygiene` needs broad access, and it's supervised.
- **Silent conflict resolution** — When two sources disagree, picking one without surfacing the tension to Xavier. This is both an epistemic and a safety failure.

---

## Sample exercise (15–30 min)

1. Pick one agent from `.claude/agents/` (not `dev-hygiene`).
2. Read its frontmatter `tools` field. List what each tool can do.
3. Read its body. Does it declare what it may and may NOT write to?
4. Does its actual behavioral instructions honor those limits? (Look for any step that might write outside the declared class.)
5. Rate the agent: fully safe / has a gap / needs a fix.

If you find a gap, draft a one-line fix (don't apply it without Xavier's go-ahead). Write your findings in today's journal.
