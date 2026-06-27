import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from state import ProposalDraftState

_ID_PATTERN = re.compile(r"^prop-(\d{8})-(\d+)")


def enrich_context_node(state: ProposalDraftState) -> dict:
    errors = list(state.get("errors", []))
    root = Path(state["repo_root"])

    # Load known surface IDs from surface-map.json
    surface_map_path = root / "users" / "cici" / "governed-state" / "surface-map.json"
    known_surfaces = []
    try:
        data = json.loads(surface_map_path.read_text())
        known_surfaces = [s["id"] for s in data.get("surfaces", [])]
    except Exception as e:
        errors.append(f"enrich_context: could not read surface-map: {e}")

    # Compute next available sequence number for today's date
    from datetime import date
    today = date.today().strftime("%Y%m%d")

    search_dirs = [
        root / "proposals" / "queue",
        root / "proposals" / "approved",
        root / "proposals" / "rejected",
    ]
    max_seq = 0
    for d in search_dirs:
        if not d.is_dir():
            continue
        for f in d.glob("*.json"):
            m = _ID_PATTERN.match(f.stem)
            if m and m.group(1) == today:
                seq = int(m.group(2))
                if seq > max_seq:
                    max_seq = seq

    next_sequence = max_seq + 1

    return {
        "known_surfaces": known_surfaces,
        "next_sequence": next_sequence,
        "errors": errors,
    }
