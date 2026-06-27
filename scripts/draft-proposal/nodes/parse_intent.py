import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from state import ProposalDraftState

_SYSTEM = """You are a governed-state proposal classifier. Given a natural language description of a change, extract three fields and return them as a JSON object — nothing else.

Fields to extract:
- "target_surface": One of the known surface IDs listed below. Pick the closest match. If none fits, use the closest one anyway and note it in the summary.
- "change_type": One of: "add", "update", "remove", "restructure", "policy"
  - add: creating a new artifact or rule
  - update: modifying an existing artifact or rule
  - remove: deleting something
  - restructure: reorganizing without changing content
  - policy: changing how something is governed or evaluated
- "summary": A single sentence (max 180 chars) describing the change in plain English.

Return exactly: {"target_surface": "...", "change_type": "...", "summary": "..."}"""


def parse_intent_node(state: ProposalDraftState) -> dict:
    errors = list(state.get("errors", []))
    surfaces = state.get("known_surfaces", [])
    surface_list = ", ".join(surfaces) if surfaces else "identity, voice, memory-policy, workflows, tools, source-priority, runtime-bridges"

    user_msg = f"Known surface IDs: {surface_list}\n\nChange description: {state['natural_language_input']}"

    try:
        llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=256)
        response = llm.invoke([
            SystemMessage(content=_SYSTEM),
            HumanMessage(content=user_msg),
        ])
        raw = response.content.strip()
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        # Attempt to extract JSON from surrounding text
        import re
        match = re.search(r'\{[^{}]+\}', raw, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
            except Exception as e:
                errors.append(f"parse_intent: could not parse JSON: {e}")
                parsed = {}
        else:
            errors.append(f"parse_intent: no JSON in response: {raw[:200]}")
            parsed = {}
    except Exception as e:
        errors.append(f"parse_intent: {e}")
        parsed = {}

    return {"parsed": parsed, "errors": errors}
