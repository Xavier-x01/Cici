---
name: log-tension
description: Capture a named two-source conflict into brewmind-open-loops.md. Pass the two sources and their conflicting claims as the argument.
argument-hint: "<source-1> vs <source-2>: <claim-1> / <claim-2> [domain: Partners|Site|Content|Budget|Blockers]"
---

You are Cici. A two-source tension has been surfaced and must be recorded — do not resolve it silently.

## Input

Parse the user's argument as:
- **source-1:** the first source name (e.g. "Supabase capture", "brewmind-open-loops.md", "Xavier verbal")
- **source-2:** the second source name
- **claim-1:** what source-1 says
- **claim-2:** what source-2 says
- **domain:** one of Partners, Site, Content, Budget, Blockers (default: Blockers if unclear)

If the argument is missing or ambiguous, ask Xavier for the two source names and their conflicting claims before proceeding.

## Step 1 — Read brewmind-open-loops.md

Read `docs/companion-agent/brewmind-open-loops.md` in full.

## Step 2 — Draft the tension entry

Format the entry exactly as:

```
- [YYYY-MM-DD] Tension: [source-1] says "[claim-1]"; [source-2] says "[claim-2]". Unresolved as of YYYY-MM-DD.
  Resolution path: [ask Xavier to verify against a Tier A source, or note which source should take precedence per source-priority policy].
  Evidence tier: [C] until resolved.
```

Use today's date for YYYY-MM-DD.

## Step 3 — Append to the correct domain section

Insert the formatted entry under the matching domain section heading (## Partners, ## Site, ## Content, ## Budget, or ## Blockers). Place it after any existing open items, before the closing `_(no open items)_` line (remove that placeholder if it's the only item).

Update the `**Last updated:**` and `**Session:**` fields at the top of the file with today's date and the current session context.

## Step 4 — Echo the result

Show Xavier exactly what was written:

```
Tension logged to brewmind-open-loops.md → [Domain] section:

[paste the formatted entry]

This is a DOCSYNC action. No proposal needed.
To resolve: verify one source against a Tier A artifact, then update the entry with the resolution and remove it when closed.
```

Do not automatically resolve the tension, propose a winner, or edit any other section of the file.
