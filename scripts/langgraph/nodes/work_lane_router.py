import re
from pathlib import Path

from state import SessionState, LaneStatus

_LANES = ["cici-ai-core", "cici-ai-progress", "cici-ai-telegram"]


def _parse_lane_readme(readme_path: Path) -> LaneStatus:
    lane_name = readme_path.parent.name
    open_blockers: list = []
    next_action = ""

    if not readme_path.exists():
        return {"lane": lane_name, "open_blockers": [], "next_action": "README not found", "last_updated": ""}

    text = readme_path.read_text()
    sections = re.split(r"\n## ", text)

    for section in sections:
        lines = section.splitlines()
        if not lines:
            continue
        header = lines[0].strip().lower()
        body = lines[1:]

        if header == "open loops":
            for line in body:
                stripped = line.strip()
                if stripped.startswith("- [ ]"):
                    open_blockers.append(stripped[5:].strip())

        elif header == "next action":
            para: list = []
            for line in body:
                if line.strip() == "" and para:
                    break
                if line.strip() and not line.strip().startswith(("---", "|", "**Post")):
                    para.append(line.strip())
            next_action = " ".join(para)[:200]

    return {
        "lane": lane_name,
        "open_blockers": open_blockers,
        "next_action": next_action,
        "last_updated": "",
    }


def work_lane_router_node(state: SessionState) -> dict:
    root = Path(state["repo_root"])
    errors = list(state.get("errors", []))
    lane_statuses: list = []

    for lane_name in _LANES:
        readme = root / "docs" / "work-lanes" / lane_name / "README.md"
        try:
            status = _parse_lane_readme(readme)
            lane_statuses.append(status)
        except Exception as e:
            errors.append(f"work_lane_router: {lane_name}: {e}")

    return {"lane_statuses": lane_statuses, "errors": errors}
