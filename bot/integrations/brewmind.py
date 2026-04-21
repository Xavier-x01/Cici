"""
BrewMind metrics and status reader.
Reads governed docs (Tier A) first, falls back to open loops file.
Governed by users/cici/governed-state/realtime-data/policy.json (source: brewmind_governed_docs).
"""
import json
from pathlib import Path
from bot.config.settings import (
    OPEN_LOOPS_PATH,
    PROPOSALS_QUEUE_PATH,
    REPO_ROOT,
)

_BREWMIND_DOC = REPO_ROOT / "docs" / "brewmind.md"


def get_open_loops() -> str:
    """
    Read open loops from docs/companion-agent/brewmind-open-loops.md.
    Source trust: Tier A (governed doc). Returns empty string if no loops found.
    """
    if not OPEN_LOOPS_PATH.exists():
        return ""

    content = OPEN_LOOPS_PATH.read_text(encoding="utf-8").strip()
    if not content or "no open" in content.lower():
        return ""

    return f"🔁 **Open Loops** [A]\n{content[:800]}"


def get_pending_proposals() -> str:
    """
    List proposals in proposals/queue/ that are in 'proposed' status.
    Source trust: Tier A (governed files). Returns empty string if queue is empty.
    """
    if not PROPOSALS_QUEUE_PATH.exists():
        return ""

    proposals = []
    for p in sorted(PROPOSALS_QUEUE_PATH.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if data.get("status") == "proposed":
                proposals.append(f"- `{data['id']}`: {data.get('summary', '')[:100]}")
        except (json.JSONDecodeError, KeyError):
            continue

    if not proposals:
        return ""

    return "📋 **Pending Proposals** [A] — awaiting your review:\n" + "\n".join(proposals)


def get_brewmind_status() -> str:
    """
    Read a brief BrewMind status from docs/brewmind.md (first 600 chars).
    Source trust: Tier A (governed doc).
    """
    if not _BREWMIND_DOC.exists():
        return ""

    content = _BREWMIND_DOC.read_text(encoding="utf-8").strip()
    if not content:
        return ""

    excerpt = content[:600]
    return f"🍺 **BrewMind Status** [A]\n{excerpt}"
