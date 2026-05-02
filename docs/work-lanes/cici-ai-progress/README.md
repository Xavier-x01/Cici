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

- [ ] Collect GitHub + country from: Jiyah, Ythak Pat, Y, Diwitty|, Bj Libron, Val Ortiz (not yet introduced)
- [ ] Verify OB1 fork for Jayr — was shown how but completion unconfirmed
- [ ] Verify OB1 fork for Ell and Kekerv — no confirmation in chat
- [ ] Define "first-task" criteria so readiness can be assessed consistently
- [ ] Confirm which GitHub handles from executive report map to: Jiyah, Ythak Pat, Y, Bj Libron, Val Ortiz

## Next Action

Follow up in Telegram with members who have not yet introduced themselves (see table below — "pending intro" rows). Ping Jayr, Ell, and Kekerv to confirm their OB1 fork is done.

## Dashboard

_Last updated: 2026-05-02. Source: Telegram chat history (Tier A). Executive report signal (Tier B). Unverified fields marked [C]._

### Eligible — GitHub + Country submitted [A]

| Name | Country | GitHub | Self-reported XP | GitHub signal [B] | OB1 fork | First task | Next prompt |
|---|---|---|---|---|---|---|---|
| Jonathan K | US | [JK3303](https://github.com/JK3303) | "little basic experience" | Not in exec report | — | — | Confirm OB1 fork; share first use-case |
| Jayr (Dismantle) | Philippines | [salajosefinojr-sys](https://github.com/salajosefinojr-sys) | "no experience, willing to learn" | Not in exec report | Shown how — unconfirmed [C] | — | Confirm fork; pick one daily use-case for OB1 |
| Pango (Penguin) | Philippines | [PenguinPH739](https://github.com/PenguinPH739) | "little experience" | Automation / tooling — Python, data, bots | Done [A] | — | Setup OB1; share first stored thought |
| Troy | Philippines | [Troy2171](https://github.com/Troy2171) | "no knowledge about coding" | Automation / tooling — Python, shell, security | Likely done [C] | — | Confirm fork; pick a daily tracking use-case |
| Hannah | Philippines | [nana-rpix](https://github.com/nana-rpix) | "don't know coding" | Backend / systems — C++, Java/Spring Boot, PHP/SQL | Done [A] | — | Setup OB1; pick a freelance or school use-case |
| Kekerv (Kekervs) | Philippines | [Adelle-sims](https://github.com/Adelle-sims) | "don't really know how to code" | Automation / tooling — Python, shell, security | — | — | Confirm fork; share first use-case |
| Ell | Philippines | [jhon-ell16](https://github.com/jhon-ell16) | "no experience, willing to learn" | Backend / systems — Java/Spring Boot, PHP/SQL | — | — | Confirm fork; share first use-case |
| Kyle (Ka Kyle) | Philippines | [Ka-kyle](https://github.com/Ka-kyle) | Not stated | Frontend / UI — web, HTML/CSS, React-adjacent | Done [A] | — | Setup OB1; pick a small business / freelance use-case |

### Pending intro — GitHub + Country not yet received

| Name | Country | GitHub | Notes |
|---|---|---|---|
| Jiyah | — | — | Invited 24 Apr; no intro posted |
| Ythak Pat | — | — | Invited 24 Apr; no intro posted |
| Y | — | — | Invited 24 Apr; no intro posted |
| Diwitty\| | — | [diWitty00](https://github.com/diWitty00) [C] | Invited 24 Apr; handle in exec report but no chat intro |
| Bj Libron | — | — | Invited 24 Apr; no intro posted |
| Val Ortiz | — | — | Invited 24 Apr; no intro posted |

_diWitty00 (full-stack, JavaScript + Node.js) appears in the executive report — likely Diwitty|, but unconfirmed [C]. Owner to verify._

### Organizers (not applicants)

| Name | Role | GitHub | Notes |
|---|---|---|---|
| Xavier | Admin / owner | [Xavier-x01](https://github.com/Xavier-x01) | Philippines |
| Robert | Founder | — | US; GitHub not shared in group |

## GitHub Signal Summary (from executive report) [B]

| Cluster | Handles | Signal |
|---|---|---|
| Frontend / UI | nana-rpix (Hannah) [C — partial match], Ka-kyle (Kyle), Mia-yana [unmatched], Chloe05688 [unmatched] | Entry to junior; web UI, HTML/CSS, React-adjacent |
| Backend / systems | nana-rpix (Hannah), jhon-ell16 (Ell), jiaj259 [unmatched] | Intermediate; C++, Java/Spring Boot, PHP/SQL |
| Automation / tooling / data | Adelle-sims (Kekerv), Troy2171 (Troy), PenguinPH739 (Pango) | Junior to intermediate; Python, shell, security/data/bot-oriented |
| Full-stack / general tooling | diWitty00 (Diwitty\| — unconfirmed) | Intermediate; JavaScript + Node.js |

Strongest technical anchors per executive report: **nana-rpix (Hannah), jhon-ell16 (Ell), Adelle-sims (Kekerv), Troy2171 (Troy)**.

_Mia-yana, Chloe05688, jiaj259 are in the executive report but not yet matched to a Telegram member. Likely among the unintroduced members (Jiyah, Ythak Pat, Y, Bj Libron, Val Ortiz)._

## Key References

- Telegram intake: [`../cici-ai-telegram/README.md`](../cici-ai-telegram/README.md)
- Evidence tiers: [`docs/companion-agent/brewmind-companion-contract.md`](../../companion-agent/brewmind-companion-contract.md)
- Evidence staging: [`docs/prepared-context-doctrine.md`](../../prepared-context-doctrine.md)
- Upstream OB1 project: [NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1)
