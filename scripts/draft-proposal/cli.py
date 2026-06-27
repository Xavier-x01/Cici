#!/usr/bin/env python3
"""
Proposal Draft Micro-Agent

Takes a natural language description of a governed-state change and produces
a valid, queue-ready proposal JSON file in proposals/queue/.

Usage:
  python3 scripts/draft-proposal/cli.py --input "Add a retention rule to memory-policy"
  python3 scripts/draft-proposal/cli.py --input "..." --dry-run
  echo "Update the companion contract" | python3 scripts/draft-proposal/cli.py
"""

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from graph import build_graph


def detect_repo_root() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        )
        return result.stdout.strip()
    except Exception:
        return str(Path(__file__).resolve().parent.parent.parent)


def main():
    parser = argparse.ArgumentParser(description="Draft a governed-state proposal from natural language")
    parser.add_argument("--input", "-i", help="Natural language description of the change")
    parser.add_argument("--dry-run", action="store_true", help="Print proposal JSON without writing to disk")
    parser.add_argument("--repo-root", default=None, help="Path to repo root (auto-detected if omitted)")
    args = parser.parse_args()

    # Accept input from --input flag or stdin
    if args.input:
        nl_input = args.input.strip()
    elif not sys.stdin.isatty():
        nl_input = sys.stdin.read().strip()
    else:
        parser.error("Provide --input or pipe text via stdin")

    if not nl_input:
        parser.error("Input is empty")

    repo_root = args.repo_root or detect_repo_root()

    graph = build_graph()
    initial_state = {
        "natural_language_input": nl_input,
        "repo_root": repo_root,
        "known_surfaces": [],
        "next_sequence": 1,
        "parsed": {},
        "draft": {},
        "validation_errors": [],
        "retry_count": 0,
        "output_path": "",
        "dry_run": args.dry_run,
        "errors": [],
    }

    final_state = graph.invoke(initial_state)

    validation_errors = final_state.get("validation_errors", [])
    errors = final_state.get("errors", [])

    if validation_errors:
        print(f"\nValidation failed after {final_state.get('retry_count', 0)} attempt(s):", file=sys.stderr)
        for e in validation_errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    if errors:
        for e in errors:
            print(f"Warning: {e}", file=sys.stderr)

    if not final_state.get("output_path"):
        sys.exit(1)


if __name__ == "__main__":
    main()
