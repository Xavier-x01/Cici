# Lane: cici-ai-progress

## Purpose

Track member and applicant progress and cohort health. This lane owns the applicant/member table, task completion records, proof packets, and scholarship-readiness signals. Evidence labels govern all status claims — do not overstate eligibility, employment, equity, or payment commitments.

## Current Scope

- Applicant/member table (see dashboard below)
- Fields tracked: name, country, GitHub account, OB1 fork status, first-task proof, self-reported experience, visible GitHub signal, scholarship readiness
- Routing inbound Telegram signals (fork URLs, screenshots) into this lane
- Flagging members ready for next-prompt or next-task assignment

**Safety boundary:** Scholarship readiness, employment eligibility, equity, and payment status are high-stakes claims. Always use evidence labels `[A]`/`[B]`/`[C]` and do not publish or act on `[C]` claims without owner verification.

## Open Loops

- [ ] Populate dashboard table with current known applicants
- [ ] Confirm OB1 fork status for each applicant (awaiting Telegram response or GitHub verification)
- [ ] Define "first-task" criteria so readiness can be assessed consistently

## Next Action

Create or update the dashboard table below with all known applicants. Columns: name, country, GitHub, self-reported experience, visible GitHub signal, OB1 fork status, first-task status, next prompt. Source all entries from verified signals (Telegram posts, GitHub links shared by applicants); mark unverified fields `[C]`.

## Dashboard

| Name | Country | GitHub | Self-reported XP | GitHub signal | OB1 fork | First task | Next prompt |
|---|---|---|---|---|---|---|---|
| _(no entries yet)_ | | | | | | | |

_Table is Tier C until each row is verified against a primary source (applicant's own post or GitHub link). Owner must approve before any scholarship or employment claim is made._

## Key References

- Telegram intake: [`../cici-ai-telegram/README.md`](../cici-ai-telegram/README.md)
- Evidence tiers: [`docs/companion-agent/brewmind-companion-contract.md`](../../companion-agent/brewmind-companion-contract.md)
- Evidence staging: [`docs/prepared-context-doctrine.md`](../../prepared-context-doctrine.md)
- Upstream OB1 project: [NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1)
