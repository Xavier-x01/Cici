# Daily Journal

One file per day. Commit it to GitHub. That's the shared memory layer.

Every entry answers five questions: what you worked on, what changed, what's blocked, what's next, and what evidence exists. The commit history becomes the team's visible progress log — no separate app or login required.

---

## Where to put journal entries

```
docs/personal/daily-journal/YYYY-MM-DD.md
```

Name the file with today's date. Example: `2026-05-09.md`.

Each team member keeps their own journal in their own fork of the repo. The pattern is the same for everyone.

---

## How to fill it out

Five sections — answer each one briefly:

| Section | What to write |
|---|---|
| **What I Worked On** | The main things you touched today |
| **What Changed** | What actually moved — shipped, merged, completed |
| **What Is Blocked** | Anything stuck or waiting on someone. Write "None" if clear. |
| **What I Plan To Do Next** | Your top 1–3 priorities for the next session |
| **Evidence / Notes** | Links, commit hashes, PR numbers, screenshots, raw notes |

Aim for 3–10 bullets total across all sections. Short is fine.

---

## How to use the helper script

The helper creates today's draft file from the template — you just fill it in:

```bash
# Step 1: create today's draft
python3 scripts/daily_journal_helper.py

# Step 2: open the file and fill in your notes
# (The file path is printed when the script runs)
```

If you have rough notes in a text file, pass it as an argument and the script appends them at the bottom of the draft for easy reference:

```bash
python3 scripts/daily_journal_helper.py my_notes.txt
```

The script never commits or pushes anything — that step is always yours.

---

## How to review before saving

Before committing, do a quick check:

1. Read the file top to bottom — does it accurately reflect your day?
2. Fix anything wrong, vague, or missing.
3. Make sure there are no passwords, API keys, or private links in the file.

---

## How to commit and push to GitHub

```bash
git add docs/personal/daily-journal/YYYY-MM-DD.md
git commit -m "journal: daily entry YYYY-MM-DD"
git push origin <your-branch>
```

Replace `YYYY-MM-DD` with today's date. Replace `<your-branch>` with your branch name (ask your team lead if unsure).

Once pushed, anyone with repo access can see your progress in the commit history — no extra tool needed.

---

## Using an AI to draft the entry

See `daily-journal-prompt.md` in this folder. It has a copy-paste prompt you can use with Claude, ChatGPT, Cursor, or any other AI tool to turn rough notes into a formatted draft in seconds.

---

## Standard daily workflow

1. Run `python3 scripts/daily_journal_helper.py` to create today's draft.
2. Fill in the five sections (or use the AI prompt from `daily-journal-prompt.md`).
3. Review the file — fix anything off, check for secrets.
4. `git add` → `git commit` → `git push`.
5. Done. Your progress is visible on GitHub.

---

## Files in this folder

| File | Purpose |
|---|---|
| `README.md` | This guide |
| `daily-journal-template.md` | Blank template the helper uses |
| `daily-journal-prompt.md` | AI prompt for turning rough notes into a draft |
| `YYYY-MM-DD.md` | Your daily entries (one per day) |

---

## Connection to the work journal

If you use `/daily-task` for AI skill-building practice, those entries live in `docs/personal/work-journal/`. You can cross-reference them here under **Evidence / Notes** — they serve different purposes and both are worth keeping.
