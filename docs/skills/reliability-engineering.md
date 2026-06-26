# Skill: Reliability Engineering

**Invoked by:** `/apply-skill reliability-engineering`  
**Lane:** PLAN (no writes without Xavier's explicit go-ahead)  
**When to use:** When something in Cici's pipeline is broken or degraded, when running a health check, or when designing a workflow that needs to survive failure.

---

## Why reliability engineering exists in this context

Cici is a system, not just a chat tool. It has a CI gate, a proposal pipeline, a memory pipeline, a journal system, and a governed-state layer — each of which can fail in distinct ways. Reliability engineering is the discipline of understanding those failure modes and having a recovery plan before they happen.

The tools already exist. This skill teaches you to read them.

---

## The three failure modes

### 1. Pipeline failures (technical)

The artifact is malformed or the script crashes.

| Example | Symptom | Detection |
|---|---|---|
| Proposal JSON has a syntax error | CI gate fails on push | `scripts/validate-governed-state.py` |
| `evidence/` file has wrong encoding | `extract-evidence.py` crashes | Manual check after running script |
| `surface-map.json` has a missing surface | Validator error: surface not in map | CI output |
| `scripts/doctor.sh` exits non-zero | Repo structure is broken | Run `doctor.sh` manually |

### 2. Process failures (human/behavioral)

The artifact is technically valid but the workflow broke down.

| Example | Symptom | Detection |
|---|---|---|
| Session ran without calling `/session-start` | Open loops not surfaced; proposals missed | Check `docs/personal/work-journal/` for note |
| Proposal sat unreviewed for 14+ days | Governed-state is stale | `/session-start` surfaces age of oldest proposal |
| Journal has gaps (no entry for 3+ days) | Curriculum continuity broken | `/weekly-review` reports completion rate |
| `prepared-context/` grew without synthesis | Evidence backlog | `/memory-audit` flags overflow |

### 3. Trust failures (epistemic)

The data is there but it's wrong or misclassified.

| Example | Symptom | Detection |
|---|---|---|
| Tier C cited as fact in a response | User acts on unverified info | Inline annotation audit |
| Governed-state stub surface blocking real work | Can't promote because surface has no schema | `surface-map.json` status = `stub` |
| `recent_thoughts` returns stale outdated captures | Search results contradict current state | Tension analysis in deep search |

---

## The reliability toolbox

| Tool | What it checks | When to run |
|---|---|---|
| `bash scripts/doctor.sh` | Required directories, symlinks, CI config, basic repo structure | Start of any EXECUTE session |
| `python3 scripts/validate-governed-state.py` | JSON syntax, required fields, schema conformance, surface-map integrity | Before every push touching `proposals/`, `users/`, `config/` |
| GitHub Actions CI | Same as validate-governed-state.py, runs automatically | On every push or PR to watched paths |
| `/session-start` | Open proposals (with age), open loops, CLAUDE.md freshness | Every session |
| `/weekly-review` | Journal completion rate, pending proposals, open loops summary | Weekly |
| `/memory-audit` | Pipeline health dossier, Tier C leak audit, stub surface status | Monthly |
| `python3 scripts/generate-dossier.py` | Full pipeline health + Tier C leak report | Monthly or on demand |

---

## Failure recovery playbook

**CI gate fails on push:**
1. Read the CI output — it will name the exact file and rule that failed.
2. Run `python3 scripts/validate-governed-state.py` locally to reproduce.
3. Fix the malformed artifact (JSON syntax error, missing required field, etc.).
4. Re-run the validator until it passes locally.
5. Commit the fix and push. Do NOT use `--no-verify` to skip the check.

**MCP server is unreachable:**
1. Run the curl health check from CLAUDE.md to confirm the server is down.
2. Do not attempt to query or capture — work from governed-state and local docs only (Tier A/B sources remain available).
3. Note the outage in today's journal. Do not cite Tier C evidence from memory.
4. Retry after a few minutes; if persistent, check Supabase Edge Function logs.

**Proposal queue is stale (proposals older than 14 days):**
1. Run `/session-start` — it surfaces open proposals with age.
2. For each stale proposal, run `/review-governed-change <id>` to evaluate and decide.
3. Approve (then `/promote-to-governed-state <id>`), reject (delete the file), or defer (add a `deferred_until` note).
4. The queue should be empty or actively moving at all times.

**Evidence backlog in `prepared-context/`:**
1. Run `/memory-audit` to get a full dossier.
2. Process each file: promote Tier A/B findings to governed-state via proposal, or archive stale ones.
3. Target: `prepared-context/` should not have files older than 30 days.

---

## Anti-patterns

- **Skipping `/session-start`** — Open loops and stale proposals accumulate invisibly.
- **Merging a failing CI** — Never merge a PR with a failing governed-state validator. The validator exists for a reason.
- **Letting stubs stay stubs indefinitely** — Stub surfaces in `surface-map.json` block legitimate use. Either populate them or deprecate them.
- **Using `--no-verify`** — Bypassing pre-commit hooks hides problems until they become bigger problems.
- **Treating chat memory as reliable** — Claude's in-session context does not survive between sessions. Use journals, governed-state, and Supabase for persistence.

---

## Sample exercise (15–30 min)

1. Run `bash scripts/doctor.sh` from the repo root. Read every line of output. Note any warnings or failures.
2. Run `python3 scripts/validate-governed-state.py`. Read the output. Note any warnings or failures.
3. Open `proposals/queue/`. Check the age of each proposal. Are any older than 14 days?
4. Open `docs/personal/work-journal/`. Count how many entries exist for the last 7 calendar days. Is the completion rate ≥ 5/7?

Write a 4-line health report in today's journal: one line per check above, with a pass/warn/fail status.
