#!/usr/bin/env python3
"""Scaffold today's daily journal entry from the template.

Usage:
    python3 scripts/daily_journal_helper.py              # bare scaffold
    python3 scripts/daily_journal_helper.py notes.txt    # scaffold + append rough notes

The script writes a draft file and prints next steps. It never commits or pushes.
"""

import datetime
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOURNAL_DIR = os.path.join(REPO_ROOT, "docs", "personal", "daily-journal")
TEMPLATE_PATH = os.path.join(JOURNAL_DIR, "daily-journal-template.md")


def main():
    today = datetime.date.today().isoformat()
    output_path = os.path.join(JOURNAL_DIR, f"{today}.md")

    if not os.path.isfile(TEMPLATE_PATH):
        print(f"Error: template not found at {TEMPLATE_PATH}")
        sys.exit(1)

    if os.path.exists(output_path):
        print(f"Draft already exists: {output_path}")
        print("Open it and continue filling it in.")
        sys.exit(0)

    with open(TEMPLATE_PATH) as f:
        draft = f.read().replace("YYYY-MM-DD", today)

    rough_notes = ""
    if len(sys.argv) > 1:
        notes_path = sys.argv[1]
        if not os.path.isfile(notes_path):
            print(f"Error: notes file not found: {notes_path}")
            sys.exit(1)
        with open(notes_path) as f:
            rough_notes = f.read().strip()

    if rough_notes:
        draft += f"\n\n---\n\n## Raw Notes (edit the sections above using these)\n\n{rough_notes}\n"

    os.makedirs(JOURNAL_DIR, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(draft)

    rel_path = os.path.relpath(output_path, REPO_ROOT)

    print(f"Draft created: {rel_path}")
    print()
    print("Next steps:")
    print(f"  1. Open {rel_path} and fill in your notes")
    print("  2. Read it once — fix anything wrong or missing")
    print("  3. Check that no secrets or private keys are in the file")
    print(f"  4. git add {rel_path}")
    print(f'  5. git commit -m "journal: daily entry {today}"')
    print("  6. git push origin <your-branch>")


if __name__ == "__main__":
    main()
