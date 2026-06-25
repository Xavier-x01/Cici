# Skill: Evaluation and Observability

**Invoked by:** `/apply-skill evaluation-and-observability`  
**Lane:** PLAN (no writes without Xavier's explicit go-ahead)  
**When to use:** When you want to know if Cici is actually working — not just running, but producing value. Use at the start of a monthly review, or any time you suspect the system is degraded.

---

## Why evaluation and observability exist in this context

A system that runs without errors is not the same as a system that works. Cici can run every session without Claude errors and still be failing: proposals not reviewed, journal entries skipped, Tier C leaking into claims, memory captures degrading in quality. Observability is the discipline of measuring the right signals to know the difference.

---

## The four things to measure

### 1. Session health

Is the startup ceremony actually running?

| Signal | Healthy | Degraded |
|---|---|---|
| `/session-start` called at session open | Always | Sometimes or never |
| Open proposals surfaced at session start | Within first 2 messages | Discovered mid-session or not at all |
| `brewmind-open-loops.md` read at session open | Always | Skipped |

### 2. Curriculum health

Is Xavier completing daily tasks and journaling?

| Signal | Healthy | Degraded |
|---|---|---|
| Work journal entries per week | ≥ 5 of 7 days | < 3 of 7 days |
| Daily task cycle position | Advancing; variety across skills | Stuck on same day |
| Journal reflection prompts answered | Most entries have a Reflection section | Mostly blank |

### 3. Pipeline health

Is the proposal → governed-state pipeline flowing?

| Signal | Healthy | Degraded |
|---|---|---|
| Age of oldest open proposal | < 7 days | > 14 days |
| Proposals approved per month | ≥ 1 | 0 |
| Proposals promoted (applied) per month | Matches approvals | Approvals not followed by promotion |
| `prepared-context/` file age | Nothing older than 30 days | Files 60+ days old with no synthesis |

### 4. Memory health

Is the memory pipeline clean and useful?

| Signal | Healthy | Degraded |
|---|---|---|
| Tier C leaks in last audit | 0 unannotated claims | Unannotated BrewMind facts in governed docs |
| Stub surfaces in surface-map | 0 or actively being developed | Stubs unchanged for 3+ months |
| Capture quality (sampled) | Mostly "good" or "best" per rubric | Mostly "too short" or "too vague" |
| Deep search result relevance | Top 3 results usually relevant | Mostly noise |

---

## The observability stack

| Signal source | Where to find it | Cadence | Command |
|---|---|---|---|
| Journal completion rate | `docs/personal/work-journal/` | Weekly | `/weekly-review` |
| Open proposals + age | `proposals/queue/` | Every session | `/session-start` |
| Pipeline health dossier | `scripts/generate-dossier.py` | Monthly | `/memory-audit` |
| Self-improvement gaps | `docs/self-improvement-log.md` | Monthly | `/self-improve` |
| Tier C leak count | `scripts/generate-dossier.py` output | Monthly | `/memory-audit` |
| Repo structure health | `scripts/doctor.sh` output | Each EXECUTE session | Direct bash |
| Governed-state validity | `scripts/validate-governed-state.py` | Each push | CI + direct bash |

---

## Defining "healthy"

A healthy Cici instance satisfies all of these at any given week:

- [ ] No proposals older than 14 days in `proposals/queue/`
- [ ] Journal completion rate ≥ 5/7 days
- [ ] At least 1 proposal approved in the last 30 days
- [ ] `prepared-context/` has no files older than 30 days
- [ ] `scripts/doctor.sh` exits zero
- [ ] `scripts/validate-governed-state.py` exits zero
- [ ] 0 Tier C leaks (unannotated BrewMind facts) in the last audit
- [ ] At least 1 `/memory-audit` run in the last 30 days

This is your SLA for Cici. If fewer than 6 of 8 pass, the system needs a maintenance session before new features are added.

---

## Writing custom health checks

To add a new check to `scripts/doctor.sh`:

```bash
# Pattern: check a condition, print pass/fail
if [ -f "path/to/required-file" ]; then
    echo "PASS: required-file exists"
else
    echo "FAIL: required-file missing"
    FAILURES=$((FAILURES + 1))
fi
```

To add a new section to `generate-dossier.py`, follow the existing pattern: read the target directory, collect metrics, append to the dossier output. Keep checks read-only.

---

## Anti-patterns

- **Measuring activity instead of outcomes** — "Claude responded 47 times this week" is not a health metric. What was approved? What was promoted? What was resolved?
- **Running health checks only when something feels wrong** — Observability is preventive. Run it on a schedule, not just after a crisis.
- **Treating CI pass as "system is healthy"** — CI validates JSON syntax and schema. It says nothing about pipeline flow, journal completion, or memory quality.
- **Ignoring Tier C leaks** — Each unannotated BrewMind fact in a governed doc is a measurement failure. Someone cited unverified data as truth.
- **Accumulating stub surfaces** — A `status: stub` surface that never gets developed is an open wound in the observability map. Either develop it or deprecate it.

---

## Sample exercise (15–30 min)

1. Run `/weekly-review` and `/surface-next`. Read the outputs carefully.
2. Score the current system against the "Defining healthy" checklist above. How many of 8 pass?
3. Write 3 health assertions in the form: `"As of [date], [signal] is [value], which is [healthy/degraded] because [threshold]."` For example: `"As of 2026-06-25, the oldest open proposal is 3 days old, which is healthy because the threshold is 14 days."`
4. Identify the one metric that is furthest from healthy and propose a single concrete action to improve it.

Write your assertions and proposed action in today's journal.
