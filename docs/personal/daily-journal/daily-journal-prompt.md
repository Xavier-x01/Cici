# Daily Journal Prompt

Use this prompt with any AI tool (Claude, ChatGPT, Cursor) to turn rough notes into a clean journal draft.

No API key or account needed beyond whatever AI tool you already use.

---

## The Prompt

Copy everything between the lines, paste it into your AI chat, and replace the two placeholders:

---

I'm writing a daily journal entry for [TODAY'S DATE, e.g. 2026-05-09].

Here are my rough notes:

[PASTE YOUR ROUGH NOTES HERE]

Please format them into exactly this structure — no extra sections, no added content:

## What I Worked On
## What Changed
## What Is Blocked
## What I Plan To Do Next
## Evidence / Notes

Rules:
- Use bullet points inside each section.
- Keep each bullet to one or two sentences.
- Only include things I mentioned. Do not invent details.
- If there is nothing for a section, write a single bullet: "- None."
- Output only the formatted journal entry, starting with "## What I Worked On".

---

## After Getting the Draft

1. Copy the AI's output into `docs/personal/daily-journal/YYYY-MM-DD.md` (replace with today's date).
2. Read it once — fix anything that's wrong, missing, or mis-attributed.
3. Make sure there are no passwords, API keys, or private links in the file.
4. Commit and push:

```bash
git add docs/personal/daily-journal/YYYY-MM-DD.md
git commit -m "journal: daily entry YYYY-MM-DD"
git push origin <your-branch>
```

Replace `YYYY-MM-DD` with today's date and `<your-branch>` with your branch name.

---

## Tip: Using the Helper Script Instead

If you prefer to skip the AI step, the helper script creates the template scaffold for you:

```bash
python3 scripts/daily_journal_helper.py
```

See `README.md` in this folder for full instructions.
