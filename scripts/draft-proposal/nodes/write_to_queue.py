import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from state import ProposalDraftState


def _slug(surface: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", surface.lower()).strip("-")


def write_to_queue_node(state: ProposalDraftState) -> dict:
    errors = list(state.get("errors", []))
    draft = state.get("draft", {})
    dry_run = state.get("dry_run", False)

    surface = draft.get("target_surface", "unknown")
    proposal_id = draft.get("id", "prop-00000000-001")
    filename = f"{proposal_id}-{_slug(surface)}.json"
    output_path = ""

    if dry_run:
        print("\n--- DRY RUN: proposal not written ---")
        print(json.dumps(draft, indent=2))
        output_path = f"(dry-run) proposals/queue/{filename}"
    else:
        root = Path(state["repo_root"])
        queue_dir = root / "proposals" / "queue"
        queue_dir.mkdir(parents=True, exist_ok=True)
        dest = queue_dir / filename
        dest.write_text(json.dumps(draft, indent=2) + "\n")
        output_path = str(dest.relative_to(root))
        print(f"\nProposal written: {output_path}")

    print(f"ID:      {draft.get('id')}")
    print(f"Surface: {surface}")
    print(f"Type:    {draft.get('change_type')}")
    print(f"Summary: {draft.get('summary')}")

    return {"output_path": output_path, "errors": errors}
