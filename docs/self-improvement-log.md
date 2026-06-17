# Cici Self-Improvement Log

**Purpose:** Running record of every `/self-improve` cycle — what behavioral gaps were identified, what was proposed, and what was actually approved and applied.

**Format:** Newest entry at the top. Each entry written by the `self-improver` agent at the end of its cycle.

---

## How to read this log

- **Observed gaps** — behavioral patterns, missing commands, vague rules, or agent gaps identified during the cycle
- **Proposed** — proposals written to `proposals/queue/` or DOCSYNC actions taken directly
- **Carry-forward** — gaps noted but not addressed this cycle; reviewed next time

Each proposal listed here links to its `proposals/queue/` JSON file by id. Track approval status there.

---

<!-- entries added by self-improver agent below this line -->

## 2026-06-17 — Cycle 1

### Observed gaps
- CLAUDE.md prohibits citing Supabase recall as fact (negative rule) but does not mandate inline evidence-tier annotation ([A], [B], [C]) as a positive requirement. The canonical source-priority/policy.json requires this annotation; CLAUDE.md does not echo it as a positive rule, creating a gap between governed policy and front-loaded operator instructions.
- No slash command exists for recording a source tension (the two-source conflict pattern required by companion contract Section G). The manual edit workflow creates friction that likely causes tensions to go unrecorded.
- The plan-mode-first session behavior rule is described in CLAUDE.md but was never promoted to users/cici/governed-state/voice/session-behavior.json, leaving it as a working doc rule rather than canonical governed state. The other two session behavior rules were promoted in prop-20260413-001.
- The self-directed-learning agent combines learning partner, pilot funnel, and outreach copy roles — potentially overloaded for a single agent prompt, though no active failure observed this cycle.
- Two governed surfaces remain stubs (tools, runtime-bridges); tools in particular covers MCP client settings that are referenced in regular session use.

### Proposed
- prop-20260617-001: Add mandatory inline evidence-tier annotation rule to CLAUDE.md (both Common Errors and Session Behavior sections)
- prop-20260617-002: Add /log-tension slash command to .claude/commands/ for capturing two-source conflicts into brewmind-open-loops.md
- prop-20260617-003: Promote plan-mode-first rule to users/cici/governed-state/voice/session-behavior.json

### Not yet addressed (carry forward)
- self-directed-learning agent scope: potentially overloaded with three distinct responsibilities; consider splitting into separate learning-partner and community-pilot agents in a future cycle
- tools stub surface: no canonical artifact for MCP client settings, AI gateway preferences; blocking clean governed reference for tooling decisions
