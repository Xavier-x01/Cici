#!/usr/bin/env python3
"""
validate-governed-state.py

Validates governed-state artifacts in this repository.

Run locally:  python3 scripts/validate-governed-state.py
Run in CI:    same command (called by .github/workflows/validate-governed-state.yml)

Checks:
  1. Required directories exist
  2. Proposal JSON files in queue/approved/rejected/ are valid JSON
  3. Proposals have required fields and valid status/change_type values
  4. Proposal status matches expected values for its directory
  5. seed_intent.json files under users/ have required fields
  6. seed_intent.json instance_id matches the parent directory name
  7. governed-state/surface-map.json is present and valid for live instances
  8. governed-state/identity/instance.json is present for live instances
  9. proposals/events/event-log.json is valid JSON if present
 10. seed-phase/status.json and readiness-criteria.json are valid JSON if present
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

REQUIRED_DIRS = [
    "evidence",
    "prepared-context",
    "prepared-context/synthesis",
    "prepared-context/session",
    "prepared-context/pending-review",
    "prepared-context/archived",
    "users",
    "users/_template",
    "proposals",
    "proposals/queue",
    "proposals/approved",
    "proposals/rejected",
    "proposals/events",
    "proposals/schemas",
    "config",
    "bridges/supabase",
]

VALID_STATUSES = {"proposed", "under_review", "approved", "rejected", "deferred", "superseded"}
VALID_CHANGE_TYPES = {"add", "update", "remove", "restructure", "policy"}
REQUIRED_PROPOSAL_FIELDS = [
    "id", "created_at", "status", "change_type",
    "target_surface", "summary", "rationale", "proposer",
]
REQUIRED_SEED_FIELDS = ["instance_id", "owner", "purpose", "seed_phase_status"]
REQUIRED_INSTANCE_FIELDS = ["instance_id", "owner", "purpose", "established_at",
                             "governed_state_version", "capabilities"]
VALID_SURFACE_IDS = {
    "identity", "voice", "memory-policy", "workflows",
    "tools", "source-priority", "runtime-bridges"
}

PROPOSAL_DIRS = {
    "proposals/queue":    {"proposed", "under_review"},
    "proposals/approved": {"approved"},
    "proposals/rejected": {"rejected", "deferred", "superseded"},
}

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def check_required_dirs():
    for rel in REQUIRED_DIRS:
        if not (ROOT / rel).is_dir():
            err(f"Required directory missing: {rel}/")


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        err(f"Invalid JSON in {path.relative_to(ROOT)}: {e}")
        return None
    except OSError as e:
        err(f"Cannot read {path.relative_to(ROOT)}: {e}")
        return None


def validate_proposal(path, expected_statuses=None):
    data = load_json(path)
    if data is None:
        return

    rel = str(path.relative_to(ROOT))

    for field in REQUIRED_PROPOSAL_FIELDS:
        if field not in data:
            err(f"{rel}: missing required field '{field}'")

    status = data.get("status")
    if status is not None:
        if status not in VALID_STATUSES:
            err(f"{rel}: invalid status '{status}' — must be one of {sorted(VALID_STATUSES)}")
        elif expected_statuses and status not in expected_statuses:
            warn(f"{rel}: status '{status}' unexpected in this directory (expected: {sorted(expected_statuses)})")

    change_type = data.get("change_type")
    if change_type is not None and change_type not in VALID_CHANGE_TYPES:
        err(f"{rel}: invalid change_type '{change_type}' — must be one of {sorted(VALID_CHANGE_TYPES)}")

    confidence = data.get("confidence")
    if confidence is not None:
        if not isinstance(confidence, (int, float)) or not (0 <= confidence <= 1):
            err(f"{rel}: 'confidence' must be a number between 0.0 and 1.0")

    proposal_id = data.get("id", "")
    if proposal_id and not _valid_proposal_id(proposal_id):
        warn(f"{rel}: id '{proposal_id}' does not match recommended format prop-YYYYMMDD-NNN")

    # Validate target_surface is a known surface (warn, not error — surface list may expand)
    target_surface = data.get("target_surface", "")
    if target_surface:
        surface_key = target_surface.rstrip("/").rsplit("/", 1)[-1]
        if surface_key not in VALID_SURFACE_IDS:
            warn(f"{rel}: target_surface '{target_surface}' resolves to unknown surface '{surface_key}' — "
                 f"known: {sorted(VALID_SURFACE_IDS)}")


def _valid_proposal_id(proposal_id):
    import re
    return bool(re.match(r'^prop-\d{8}-\d{3,}', proposal_id))


def validate_proposals():
    for rel_dir, expected_statuses in PROPOSAL_DIRS.items():
        directory = ROOT / rel_dir
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.json")):
            validate_proposal(path, expected_statuses)


def validate_seed_intents():
    for path in sorted(ROOT.glob("users/*/seed_intent.json")):
        # skip the template
        if path.parent.name == "_template":
            continue

        data = load_json(path)
        if data is None:
            continue

        rel = str(path.relative_to(ROOT))
        for field in REQUIRED_SEED_FIELDS:
            if field not in data:
                err(f"{rel}: missing required field '{field}'")

        # Check no placeholder values remain
        for key, value in data.items():
            if key == "_instructions":
                err(f"{rel}: '_instructions' field must be removed before committing")
            if isinstance(value, str) and value.startswith("<") and value.endswith(">"):
                err(f"{rel}: field '{key}' still contains placeholder value '{value}'")

        instance_id = data.get("instance_id", "")
        dir_name = path.parent.name
        if instance_id and instance_id != dir_name:
            err(f"{rel}: instance_id '{instance_id}' does not match directory name '{dir_name}'")

        status = data.get("seed_phase_status")
        if status and status not in {"pending", "active", "archived"}:
            warn(f"{rel}: unexpected seed_phase_status '{status}'")


def validate_instance_governed_state():
    """Validate structure of live instance governed-state directories."""
    for instance_dir in sorted(ROOT.glob("users/*")):
        if not instance_dir.is_dir():
            continue
        if instance_dir.name == "_template":
            continue

        instance_id = instance_dir.name
        gs_dir = instance_dir / "governed-state"

        if not gs_dir.is_dir():
            err(f"users/{instance_id}/: missing governed-state/ directory")
            continue

        # Check surface-map.json
        surface_map_path = gs_dir / "surface-map.json"
        if not surface_map_path.exists():
            warn(f"users/{instance_id}/governed-state/: surface-map.json missing — "
                 f"add to enable surface validation")
        else:
            surface_map = load_json(surface_map_path)
            if surface_map:
                # Check for placeholder values
                map_instance_id = surface_map.get("instance_id", "")
                if map_instance_id.startswith("<") and map_instance_id.endswith(">"):
                    err(f"users/{instance_id}/governed-state/surface-map.json: "
                        f"instance_id still contains placeholder '{map_instance_id}'")
                elif map_instance_id and map_instance_id != instance_id:
                    err(f"users/{instance_id}/governed-state/surface-map.json: "
                        f"instance_id '{map_instance_id}' does not match directory '{instance_id}'")

                # Check _instructions not present
                if "_instructions" in surface_map:
                    err(f"users/{instance_id}/governed-state/surface-map.json: "
                        f"'_instructions' field must be removed before committing")

        # Check identity surface exists
        identity_dir = gs_dir / "identity"
        if not identity_dir.is_dir():
            warn(f"users/{instance_id}/governed-state/: identity/ surface directory missing")
        else:
            instance_json_path = identity_dir / "instance.json"
            if not instance_json_path.exists():
                warn(f"users/{instance_id}/governed-state/identity/: instance.json missing — "
                     f"create during Seed Phase initialization")
            else:
                data = load_json(instance_json_path)
                if data:
                    rel = str(instance_json_path.relative_to(ROOT))
                    for field in REQUIRED_INSTANCE_FIELDS:
                        if field not in data:
                            err(f"{rel}: missing required field '{field}'")
                    iid = data.get("instance_id", "")
                    if iid and iid != instance_id:
                        err(f"{rel}: instance_id '{iid}' does not match directory '{instance_id}'")


def validate_event_log():
    """Validate event log JSON structure if present."""
    event_log_path = ROOT / "proposals" / "events" / "event-log.json"
    if not event_log_path.exists():
        warn("proposals/events/event-log.json missing — create with empty events array")
        return

    data = load_json(event_log_path)
    if data is None:
        return

    rel = str(event_log_path.relative_to(ROOT))
    if "events" not in data:
        err(f"{rel}: missing required 'events' array")
        return

    if not isinstance(data["events"], list):
        err(f"{rel}: 'events' must be an array")
        return

    for i, event in enumerate(data["events"]):
        for field in ["event_id", "timestamp", "proposal_id", "action"]:
            if field not in event:
                warn(f"{rel}: event[{i}] missing field '{field}'")


def validate_seed_phase_artifacts():
    """Validate seed-phase/ artifacts for live instances if present."""
    for instance_dir in sorted(ROOT.glob("users/*")):
        if not instance_dir.is_dir() or instance_dir.name == "_template":
            continue

        instance_id = instance_dir.name
        seed_phase_dir = instance_dir / "seed-phase"

        if not seed_phase_dir.is_dir():
            # Not required — just a warning for live instances
            warn(f"users/{instance_id}/: seed-phase/ directory missing — "
                 f"consider adding for readiness tracking")
            continue

        # Validate status.json if present
        status_path = seed_phase_dir / "status.json"
        if status_path.exists():
            data = load_json(status_path)
            if data:
                rel = str(status_path.relative_to(ROOT))
                if "_instructions" in data:
                    err(f"{rel}: '_instructions' field must be removed before committing")
                iid = data.get("instance_id", "")
                if iid.startswith("<"):
                    err(f"{rel}: instance_id still contains placeholder '{iid}'")
                elif iid and iid != instance_id:
                    err(f"{rel}: instance_id '{iid}' does not match directory '{instance_id}'")

        # Validate readiness-criteria.json if present
        criteria_path = seed_phase_dir / "readiness-criteria.json"
        if criteria_path.exists():
            data = load_json(criteria_path)
            if data:
                rel = str(criteria_path.relative_to(ROOT))
                if "_instructions" in data:
                    err(f"{rel}: '_instructions' field must be removed before committing")


def main():
    check_required_dirs()
    validate_proposals()
    validate_seed_intents()
    validate_instance_governed_state()
    validate_event_log()
    validate_seed_phase_artifacts()

    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  [warn] {w}")

    if errors:
        print("Errors:")
        for e in errors:
            print(f"  [fail] {e}")
        print(f"\n{len(errors)} error(s) found. Fix them before merging.")
        sys.exit(1)
    else:
        total_warnings = len(warnings)
        print(f"All governed-state artifacts are valid." +
              (f" ({total_warnings} warning(s))" if total_warnings else ""))


if __name__ == "__main__":
    main()
