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

- [ ] Collect GitHub + country from: Ythak Pat, Y, Diwitty|, Bj Libron (not yet introduced)
- [ ] Verify OB1 fork for Jayr — was shown how but completion unconfirmed
- [ ] Verify OB1 fork for Jonathan K — no confirmation in chat
- [ ] Collect Task 1 proof from each member (screenshot or GitHub update)

## Next Action

Chase Task 1 proof from members who have confirmed their fork. Chase Jayr and Jonathan K to confirm fork so they can join Task 1.

## Task Definitions

### Task 1 — Get OB1 Live (assigned 2026-05-02)

**Goal:** Complete the OB1 setup and store your first real thought.

**Steps:**
1. Follow the setup guide: `docs/setup-guide.md` in the Cici repo (link in pinned message)
2. Store one real thought from your actual life — a client task, school note, personal goal, side project idea, anything
3. Share proof in Telegram: a screenshot showing OB1 working (the `curl` test from Step 7, or OB1 connected in Claude/Cursor)

**Bonus (makes it visible on GitHub):** Add a `proof/` folder to your forked repo with a short `README.md` — just one sentence describing what you stored (no personal data needed, e.g. "stored my first client request").

**Pass criteria:** Screenshot shared in Telegram showing a live OB1 response, OR a `proof/` commit visible on your GitHub fork.

**Notes:**
- Claude, Cursor, or ChatGPT can help you through any step — that's the point
- Ask in the group if you get stuck; don't go silent
- Estimated time: 30–45 minutes following the guide

## Dashboard

_Last updated: 2026-05-02 (fork status revised). Source: Telegram chat history (Tier A). Owner confirmation (Tier A). Executive report signal (Tier B). Unverified fields marked [C]._

### Eligible — GitHub + Country submitted [A]

| Name | Country | GitHub | Self-reported XP | GitHub signal [B] | OB1 fork | First task | Next prompt |
|---|---|---|---|---|---|---|---|
| Jonathan K | US | [JK3303](https://github.com/JK3303) | "little basic experience" | Not in exec report | — | Pending fork | Confirm fork first |
| Jayr (Dismantle) | Philippines | [salajosefinojr-sys](https://github.com/salajosefinojr-sys) | "no experience, willing to learn" | Not in exec report | Unconfirmed [C] | Pending fork | Confirm fork first |
| Pango (Penguin) | Philippines | [PenguinPH739](https://github.com/PenguinPH739) | "little experience" | Automation / tooling — Python, data, bots | Done [A] | Assigned | Follow setup guide → curl test screenshot |
| Troy | Philippines | [Troy2171](https://github.com/Troy2171) | "no knowledge about coding" | Automation / tooling — Python, shell, security | Done [A] | Assigned | Follow setup guide → curl test screenshot |
| Hannah | Philippines | [nana-rpix](https://github.com/nana-rpix) | "don't know coding" | Backend / systems — C++, Java/Spring Boot, PHP/SQL | Done [A] | Assigned | Follow setup guide → curl test screenshot |
| Kekerv (Kekervs) | Philippines | [Adelle-sims](https://github.com/Adelle-sims) | "don't really know how to code" | Automation / tooling — Python, shell, security | Done [A] | Assigned | Follow setup guide → curl test screenshot |
| Ell | Philippines | [jhon-ell16](https://github.com/jhon-ell16) | "no experience, willing to learn" | Backend / systems — Java/Spring Boot, PHP/SQL | Done [A] | Assigned | Follow setup guide → curl test screenshot |
| Kyle (Ka Kyle) | Philippines | [Ka-kyle](https://github.com/Ka-kyle) | Not stated | Frontend / UI — web, HTML/CSS, React-adjacent | Done [A] | Assigned | Follow setup guide → curl test screenshot |
| Jiyah | Philippines | [jiaj259](https://github.com/jiaj259) | Not stated | Backend / systems — C++, Java/Spring Boot, PHP/SQL | Done [A] | Assigned | Follow setup guide → curl test screenshot |
| Val Ortiz | Philippines | [Mia-yana](https://github.com/Mia-yana) | Not stated | Frontend / UI — web, HTML/CSS, React-adjacent | Done [A] | Assigned | Follow setup guide → curl test screenshot |
| Kathy | Philippines | [Chloe05688](https://github.com/Chloe05688) | Not stated | Frontend / UI — web, HTML/CSS, React-adjacent | Done [A] | Assigned | Follow setup guide → curl test screenshot |

### Pending intro — GitHub + Country not yet received

| Name | Country | GitHub | Notes |
|---|---|---|---|
| Ythak Pat | — | — | Invited 24 Apr; no intro posted |
| Y | — | — | Invited 24 Apr; no intro posted |
| Diwitty\| | — | [diWitty00](https://github.com/diWitty00) [C] | Invited 24 Apr; handle in exec report but no chat intro |
| Bj Libron | — | — | Invited 24 Apr; no intro posted |

_diWitty00 (full-stack, JavaScript + Node.js) appears in the executive report — likely Diwitty|, but unconfirmed [C]. Owner to verify._

### Organizers (not applicants)

| Name | Role | GitHub | Notes |
|---|---|---|---|
| Xavier | Admin / owner | [Xavier-x01](https://github.com/Xavier-x01) | Philippines |
| Robert | Founder | — | US; GitHub not shared in group |

## GitHub Signal Summary (from executive report) [B]

| Cluster | Handles | Signal |
|---|---|---|
| Frontend / UI | nana-rpix (Hannah) [C — partial match], Ka-kyle (Kyle), Mia-yana (Val Ortiz), Chloe05688 (Kathy) | Entry to junior; web UI, HTML/CSS, React-adjacent |
| Backend / systems | nana-rpix (Hannah), jhon-ell16 (Ell), jiaj259 (Jiyah) | Intermediate; C++, Java/Spring Boot, PHP/SQL |
| Automation / tooling / data | Adelle-sims (Kekerv), Troy2171 (Troy), PenguinPH739 (Pango) | Junior to intermediate; Python, shell, security/data/bot-oriented |
| Full-stack / general tooling | diWitty00 (Diwitty\| — unconfirmed) | Intermediate; JavaScript + Node.js |

Strongest technical anchors per executive report: **nana-rpix (Hannah), jhon-ell16 (Ell), Adelle-sims (Kekerv), Troy2171 (Troy)**.

_All exec-report handles now matched. Mia-yana = Val Ortiz [A]. Chloe05688 = Kathy [A]._

## Key References

- Telegram intake: [`../cici-ai-telegram/README.md`](../cici-ai-telegram/README.md)
- Evidence tiers: [`docs/companion-agent/brewmind-companion-contract.md`](../../companion-agent/brewmind-companion-contract.md)
- Evidence staging: [`docs/prepared-context-doctrine.md`](../../prepared-context-doctrine.md)
- Upstream OB1 project: [NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1)
