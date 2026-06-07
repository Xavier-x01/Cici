import json
from pathlib import Path

from state import SessionState, ProposalReviewResult

_REQUIRED_FIELDS = {"id", "target_surface", "summary", "status", "created_at"}
_VALID_STATUSES = {"pending_review", "draft", "approved", "rejected", "deferred"}


def proposal_review_node(state: SessionState) -> dict:
    errors = list(state.get("errors", []))
    proposals = list(state.get("proposals", []))
    root = Path(state["repo_root"])

    # Load known surfaces from surface-map.json
    surface_map_path = root / "users" / "cici" / "governed-state" / "surface-map.json"
    known_surfaces: set = set()
    try:
        data = json.loads(surface_map_path.read_text())
        known_surfaces = {s["id"] for s in data.get("surfaces", [])}
    except Exception:
        pass

    evaluated = []
    seen_surfaces: dict = {}
    conflicts: list = []

    for p in proposals:
        pid = p["id"]
        surface = p["target_surface"]
        notes = []
        valid = True

        # Re-read from disk to get all fields for schema check
        queue_path = root / "proposals" / "queue" / f"{pid}.json"
        raw: dict = {}
        if queue_path.exists():
            try:
                raw = json.loads(queue_path.read_text())
            except Exception as e:
                notes.append(f"parse error: {e}")
                valid = False

        missing = _REQUIRED_FIELDS - set(raw.keys())
        if missing:
            notes.append(f"missing fields: {sorted(missing)}")
            valid = False

        if raw.get("status") not in _VALID_STATUSES and raw.get("status"):
            notes.append(f"unknown status: {raw['status']}")
            valid = False

        if known_surfaces and surface not in known_surfaces:
            notes.append(f"unknown surface: {surface}")
            valid = False

        if surface in seen_surfaces:
            conflict_pair = f"{seen_surfaces[surface]} ↔ {pid}"
            if conflict_pair not in conflicts:
                conflicts.append(conflict_pair)
        else:
            seen_surfaces[surface] = pid

        evaluated.append({
            **p,
            "schema_valid": valid,
            "reviewer_notes": "; ".join(notes) if notes else "ok",
        })

    result: ProposalReviewResult = {
        "evaluated": evaluated,
        "conflicts": conflicts,
        "issues_found": any(not e["schema_valid"] for e in evaluated) or bool(conflicts),
    }

    return {
        "proposals": evaluated,
        "proposal_review": result,
        "branches_taken": list(state.get("branches_taken", [])) + ["proposal_review"],
        "errors": errors,
    }
