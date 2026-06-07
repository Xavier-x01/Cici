import json
import re
from pathlib import Path

from state import SessionState


_PROPOSAL_REQUIRED = {"id", "target_surface", "summary", "status"}


def load_context_node(state: SessionState) -> dict:
    root = Path(state["repo_root"])
    errors = list(state.get("errors", []))
    proposals = []
    open_loops = []

    # --- Load proposals from queue ---
    queue_dir = root / "proposals" / "queue"
    if queue_dir.is_dir():
        for f in sorted(queue_dir.glob("*.json")):
            try:
                data = json.loads(f.read_text())
                proposals.append({
                    "id": data.get("id", f.stem),
                    "target_surface": data.get("target_surface", "?"),
                    "summary": data.get("summary", "")[:120],
                    "status": data.get("status", "?"),
                    "schema_valid": False,
                    "reviewer_notes": "",
                })
            except Exception as e:
                errors.append(f"load_context: failed to parse {f.name}: {e}")

    # --- Parse brewmind-open-loops.md ---
    loops_path = root / "docs" / "companion-agent" / "brewmind-open-loops.md"
    if loops_path.exists():
        try:
            text = loops_path.read_text()
            # Split on ## headers (skip anything before the first ##)
            sections = re.split(r"\n## ", text)
            for section in sections[1:]:  # first element is the preamble
                lines = section.strip().splitlines()
                if not lines:
                    continue
                domain = lines[0].strip()
                body = "\n".join(lines[1:]).strip()
                # Skip meta sections like "How to use this file"
                if domain.lower().startswith("how to"):
                    continue
                has_items = "_(no open items)_" not in body
                open_loops.append({
                    "domain": domain,
                    "has_open_items": has_items,
                    "raw_text": body[:400],
                })
        except Exception as e:
            errors.append(f"load_context: failed to parse open-loops: {e}")
    else:
        errors.append("load_context: brewmind-open-loops.md not found")

    return {
        "proposals": proposals,
        "open_loops": open_loops,
        "lane": "PLAN",
        "errors": errors,
    }
