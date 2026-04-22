# Memory Retention Policy: Durability Classification

> **Status:** active — governed by proposal `prop-20260422-001`
> **Machine-readable source:** `memory-policy/policy.json` (canonical, governed by `prop-20260420-001`)
> **Last updated:** 2026-04-22
> **Write class:** `canonical` — changes require Xavier approval or an approved proposal

---

## Purpose

This document explains how Cici classifies and retains memories in plain language. The authoritative machine-readable policy lives in `policy.json` alongside this file. This document is the human-readable companion: it explains the rationale, the rules, and the operational consequences of each durability class for sessions, agents, and future maintainers.

---

## Durability Classes

Every memory written to Supabase runtime must declare a `durability_class` at write time. There are exactly two classes.

---

### Transient

| Property | Value |
|---|---|
| Retention window | 7 days (rolling) |
| Eligible for synthesis | No |
| Auto-archive on expiry | Yes |
| Promotion path | None — expires and archives automatically |

**What belongs here:** One-off, session-scoped data with no recurring relevance. Examples: a debugging question, a quick lookup, a one-time calculation, intermediate planning steps, session scaffolding notes.

**Operational rules:**
- Do not cite transient memories as fact in any Compiled View or governed document.
- `memory-auditor` archives expired transient entries on the weekly hygiene pass.
- No manual review is needed at expiry — auto-archive fires automatically.
- Transient entries are never promoted to synthesis or governed-state; they have no promotion path.
- If a transient entry turns out to be worth retaining, a fresh `persistent` capture must be created from verified source material. There is no in-place reclassification (see Transition Rules below).

---

### Persistent

| Property | Value |
|---|---|
| Retention window | 90 days |
| Eligible for synthesis | Yes |
| Auto-archive on expiry | No |
| Promotion path | `evidence/` → `prepared-context/synthesis/` → proposal → governed-state |

**What belongs here:** Recurring or pattern-based data that should survive across sessions. Examples: twice-daily protein tracking, active project state, personal preferences, verified BrewMind partner context, explicit decisions made by Xavier.

**Operational rules:**
- At 90 days, `memory-auditor` flags the entry for review — it does not auto-archive.
- Review outcomes are: extend retention, promote to governed-state via proposal, or archive.
- Only Tier A or B sources may back persistent entries used in Compiled Views.
- Tier C content (model synthesis, unverified Supabase recall) must not be stored as `persistent` without Xavier's explicit verification.

---

## Transition Rules: Transient → Persistent

Transient data is **never** directly reclassified as persistent. There is no in-place upgrade.

If a transient entry proves worth keeping:
1. Create a new `persistent` capture from verified source material.
2. The original transient entry continues on its 7-day schedule and archives normally.

This rule prevents session noise from accumulating as governed truth through an informal reclassification shortcut.

---

## Promotion Path: Persistent → Governed State

High-signal persistent memories that represent durable conclusions (decisions, verified preferences, canonical project context) may be promoted through the full durable stack:

```
supabase-runtime (persistent class)
  ↓ stage via evidence-stager
evidence/
  ↓ synthesize
prepared-context/synthesis/
  ↓ propose
proposals/queue/
  ↓ approved by Xavier
users/cici/governed-state/
```

No shortcut is permitted. Model-synthesized summaries do not bypass this path. Each step requires a human decision point or an approved agent action.

---

## Archived State

Archived entries — whether transient entries past their 7-day window or persistent entries archived after review — are retained for 365 days before deletion. Archived entries are:
- Read-only
- Not eligible for synthesis
- Not citable as active facts

---

## Agent Obligations

Any agent reading or processing memories (`memory-auditor`, `evidence-stager`, session agents) must:

- Check `durability_class` before using a memory as an input to any output.
- Not use transient entries as inputs to Compiled Views.
- Annotate persistent entries with `[C]` until they have been promoted to a Tier A or B source.
- Flag conflicts (same topic, different durability classes on different entries) as `Tension:` annotations and log them in `docs/companion-agent/brewmind-open-loops.md`.

---

## Related Files

| File | Role |
|---|---|
| `policy.json` | Machine-readable policy source — canonical |
| `../source-priority/policy.json` | How to weight conflicting sources (5-tier hierarchy) |
| `../../../docs/companion-agent/brewmind-companion-contract.md` | Evidence tier definitions (Tier A / B / C) |
| `../../../proposals/approved/prop-20260420-001-activate-memory-policy.json` | Proposal that created policy.json |
