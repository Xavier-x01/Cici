#!/usr/bin/env python3
"""
Cici session ritual orchestrator.

Usage:
  python3 scripts/langgraph/cli.py [--repo-root PATH] [--dry-run] [--format md|json]
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def detect_repo_root() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return str(Path(__file__).parents[2])  # scripts/langgraph/../../ = repo root


def main():
    parser = argparse.ArgumentParser(description="Cici session ritual orchestrator")
    parser.add_argument("--repo-root", default=None, help="Path to repo root")
    parser.add_argument("--dry-run", action="store_true", help="Dump state JSON instead of report")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    parser.add_argument("--llm", action="store_true", help="Call Claude to generate Today's Focus (requires ANTHROPIC_API_KEY)")
    args = parser.parse_args()

    try:
        from graph import build_graph
    except ImportError as e:
        print(
            f"[error] langgraph not installed: {e}\n"
            "Run: pip install -r scripts/langgraph/requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    repo_root = args.repo_root or detect_repo_root()

    checkpointer = None
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        try:
            from langgraph.checkpoint.postgres import PostgresSaver
            checkpointer = PostgresSaver.from_conn_string(db_url)
            checkpointer.setup()
        except Exception as e:
            print(f"[warn] PostgreSQL checkpointer unavailable ({e}), falling back to MemorySaver", file=sys.stderr)
            checkpointer = None

    graph = build_graph(checkpointer=checkpointer)
    initial_state = {
        "run_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "repo_root": repo_root,
        "proposals": [],
        "open_loops": [],
        "lane": "PLAN",
        "dossier": None,
        "proposal_review": None,
        "memory_audit": None,
        "lane_statuses": [],
        "use_llm": args.llm,
        "llm_summary": "",
        "report": "",
        "branches_taken": [],
        "errors": [],
    }

    config = {"configurable": {"thread_id": "session-start"}}
    final_state = graph.invoke(initial_state, config=config)

    if args.dry_run or args.format == "json":
        printable = {k: v for k, v in final_state.items() if k != "dossier"}
        if final_state.get("dossier"):
            printable["dossier"] = {
                k: v for k, v in final_state["dossier"].items() if k != "raw"
            }
        print(json.dumps(printable, indent=2, default=str))
    else:
        print(final_state.get("report", "[no report generated]"))

    if final_state.get("errors"):
        print("\n--- Warnings ---", file=sys.stderr)
        for err in final_state["errors"]:
            print(f"  [warn] {err}", file=sys.stderr)


if __name__ == "__main__":
    main()
