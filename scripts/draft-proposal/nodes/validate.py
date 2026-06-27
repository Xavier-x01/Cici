import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from state import ProposalDraftState

_REQUIRED = {"id", "created_at", "status", "change_type", "target_surface", "summary", "rationale", "proposer"}
_VALID_STATUSES = {"proposed", "under_review", "approved", "rejected", "deferred", "superseded"}
_VALID_CHANGE_TYPES = {"add", "update", "remove", "restructure", "policy"}
_ID_RE = re.compile(r"^prop-\d{8}-\d{3,}$")
_MAX_RETRIES = 2


def validate_node(state: ProposalDraftState) -> dict:
    draft = state.get("draft", {})
    known_surfaces = state.get("known_surfaces", [])
    retry_count = state.get("retry_count", 0)
    errors = list(state.get("errors", []))

    issues = []

    missing = _REQUIRED - set(draft.keys())
    if missing:
        issues.append(f"missing required fields: {sorted(missing)}")

    pid = draft.get("id", "")
    if pid and not _ID_RE.match(pid):
        issues.append(f"id format invalid (expected prop-YYYYMMDD-NNN): {pid!r}")

    status = draft.get("status")
    if status and status not in _VALID_STATUSES:
        issues.append(f"invalid status {status!r}; must be one of {sorted(_VALID_STATUSES)}")

    if status != "proposed":
        issues.append(f"proposals in queue/ must have status 'proposed', got {status!r}")

    change_type = draft.get("change_type")
    if change_type and change_type not in _VALID_CHANGE_TYPES:
        issues.append(f"invalid change_type {change_type!r}; must be one of {sorted(_VALID_CHANGE_TYPES)}")

    surface = draft.get("target_surface", "")
    if known_surfaces and surface not in known_surfaces:
        issues.append(f"unknown target_surface {surface!r}; known: {known_surfaces}")

    summary = draft.get("summary", "")
    if len(summary) > 200:
        issues.append(f"summary too long ({len(summary)} chars, max 200)")

    if not draft.get("rationale", "").strip():
        issues.append("rationale is empty")

    return {
        "validation_errors": issues,
        "retry_count": retry_count + (1 if issues else 0),
        "errors": errors,
    }
