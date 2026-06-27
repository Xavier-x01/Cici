import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from langgraph.graph import StateGraph, END

from state import ProposalDraftState
from nodes.parse_intent import parse_intent_node
from nodes.enrich_context import enrich_context_node
from nodes.draft_proposal import draft_proposal_node
from nodes.validate import validate_node, _MAX_RETRIES
from nodes.write_to_queue import write_to_queue_node


def _route_after_validate(state: dict) -> str:
    if not state.get("validation_errors"):
        return "write_to_queue"
    if state.get("retry_count", 0) >= _MAX_RETRIES:
        return "__end__"
    return "draft_proposal"


def build_graph():
    builder = StateGraph(ProposalDraftState)

    builder.add_node("parse_intent", parse_intent_node)
    builder.add_node("enrich_context", enrich_context_node)
    builder.add_node("draft_proposal", draft_proposal_node)
    builder.add_node("validate", validate_node)
    builder.add_node("write_to_queue", write_to_queue_node)

    builder.set_entry_point("parse_intent")
    builder.add_edge("parse_intent", "enrich_context")
    builder.add_edge("enrich_context", "draft_proposal")
    builder.add_edge("draft_proposal", "validate")

    builder.add_conditional_edges(
        "validate",
        _route_after_validate,
        {
            "write_to_queue": "write_to_queue",
            "draft_proposal": "draft_proposal",
            "__end__": END,
        },
    )

    builder.add_edge("write_to_queue", END)

    return builder.compile()
