import json
import re
from datetime import datetime, timezone
from pathlib import Path

from state import SessionState, MemoryAuditResult

_BUSINESS_PATTERN = re.compile(
    r"\b(pric(e|ing)|revenue|partner(ship)?|launch|cost|fee|charg(e|ing)|commit(ment)?)\b",
    re.IGNORECASE,
)
_TIER_TAG = re.compile(r"\[(A|B)\]")
_OVERDUE_DAYS = 14


def _scan_tier_c_leaks(paths: list) -> list:
    leaks = []
    for path in paths:
        if not path.exists():
            continue
        try:
            in_html_comment = False
            for i, line in enumerate(path.read_text().splitlines(), 1):
                stripped = line.strip()
                # Track HTML comment blocks
                if "<!--" in stripped:
                    in_html_comment = True
                if "-->" in stripped:
                    in_html_comment = False
                    continue
                if in_html_comment:
                    continue
                if not stripped or stripped.startswith(("#", ">")):
                    continue
                if _BUSINESS_PATTERN.search(stripped) and not _TIER_TAG.search(stripped):
                    leaks.append({"file": str(path.name), "line": i, "text": stripped[:120]})
        except Exception:
            pass
    return leaks


def memory_audit_node(state: SessionState) -> dict:
    errors = list(state.get("errors", []))
    root = Path(state["repo_root"])
    dossier = state.get("dossier") or {}

    stub_surfaces = dossier.get("stub_surfaces", [])

    # Which stubs have at least one evidence file referencing them?
    evidence_dir = root / "evidence"
    stub_surfaces_with_evidence = []
    for stub in stub_surfaces:
        matches = list(evidence_dir.glob(f"*{stub}*"))
        if matches:
            stub_surfaces_with_evidence.append(stub)

    # Tier C leak scan
    scan_targets = [
        root / "docs" / "companion-agent" / "brewmind-open-loops.md",
        *sorted((root / "prepared-context" / "pending-review").glob("*.md")),
        *sorted((root / "prepared-context" / "pending-review").glob("*.json")),
    ]
    tier_c_leaks = _scan_tier_c_leaks(scan_targets)

    # Overdue proposals (created_at > OVERDUE_DAYS ago)
    overdue = []
    now = datetime.now(timezone.utc)
    queue_dir = root / "proposals" / "queue"
    if queue_dir.is_dir():
        for f in queue_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                created_str = data.get("created_at", "")
                if created_str:
                    created = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                    age = (now - created).days
                    if age > _OVERDUE_DAYS:
                        overdue.append(f"{data.get('id', f.stem)} (age: {age}d)")
            except Exception:
                pass

    next_steps = []
    if stub_surfaces:
        next_steps.append(
            f"Draft proposals to populate stub surfaces: {', '.join(stub_surfaces)}"
        )
    if tier_c_leaks:
        next_steps.append(
            f"Review {len(tier_c_leaks)} Tier C claim(s) in pending-review/ or open-loops.md"
        )
    if overdue:
        next_steps.append(f"Resolve {len(overdue)} overdue proposal(s): {', '.join(overdue)}")

    result: MemoryAuditResult = {
        "stub_surfaces_with_evidence": stub_surfaces_with_evidence,
        "tier_c_leaks": tier_c_leaks,
        "overdue_proposals": overdue,
        "recommended_next_steps": next_steps,
    }

    return {
        "memory_audit": result,
        "branches_taken": list(state.get("branches_taken", [])) + ["memory_audit"],
        "errors": errors,
    }
