import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from state import ProposalDraftState

_SYSTEM = """You are a governed-state proposal writer for an AI memory system called Cici. Given context about a proposed change, produce a JSON object with exactly these fields:

- "rationale": 2–4 sentences explaining why this change is needed and what problem it solves.
- "proposed_diff_summary": 1–2 sentences describing concretely what would be added, changed, or removed.
- "confidence": A float 0.0–1.0 representing how confident you are that this change is correct and well-scoped. Be conservative (0.6–0.8 is typical).

Return exactly: {"rationale": "...", "proposed_diff_summary": "...", "confidence": 0.00}"""


def draft_proposal_node(state: ProposalDraftState) -> dict:
    errors = list(state.get("errors", []))
    parsed = state.get("parsed", {})
    validation_errors = state.get("validation_errors", [])
    retry_count = state.get("retry_count", 0)

    today_str = date.today().strftime("%Y%m%d")
    seq = state.get("next_sequence", 1)
    proposal_id = f"prop-{today_str}-{seq:03d}"

    user_parts = [
        f"Natural language input: {state['natural_language_input']}",
        f"Target surface: {parsed.get('target_surface', 'unknown')}",
        f"Change type: {parsed.get('change_type', 'unknown')}",
        f"Summary: {parsed.get('summary', '')}",
    ]
    if validation_errors and retry_count > 0:
        user_parts.append(f"\nPrevious validation failed with: {'; '.join(validation_errors)}. Adjust accordingly.")

    try:
        llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=512)
        response = llm.invoke([
            SystemMessage(content=_SYSTEM),
            HumanMessage(content="\n".join(user_parts)),
        ])
        raw = response.content.strip()
        enrichment = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
        if match:
            try:
                enrichment = json.loads(match.group())
            except Exception as e:
                errors.append(f"draft_proposal: JSON parse failed: {e}")
                enrichment = {}
        else:
            errors.append(f"draft_proposal: no JSON in response: {raw[:200]}")
            enrichment = {}
    except Exception as e:
        errors.append(f"draft_proposal: {e}")
        enrichment = {}

    now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    draft = {
        "id": proposal_id,
        "created_at": now_iso,
        "status": "proposed",
        "change_type": parsed.get("change_type", "update"),
        "target_surface": parsed.get("target_surface", ""),
        "summary": parsed.get("summary", "")[:200],
        "rationale": enrichment.get("rationale", ""),
        "proposed_diff_summary": enrichment.get("proposed_diff_summary", ""),
        "confidence": enrichment.get("confidence", 0.7),
        "proposer": "draft-proposal-agent",
        "reviewer": None,
        "decided_at": None,
        "decision_notes": None,
    }

    return {"draft": draft, "errors": errors}
