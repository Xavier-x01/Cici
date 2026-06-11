import sys
from pathlib import Path

# Ensure this package dir is on sys.path so node imports resolve
sys.path.insert(0, str(Path(__file__).parent))

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from state import SessionState
from routing import route_branches, route_after_synthesize
from nodes.load_context import load_context_node
from nodes.run_dossier import run_dossier_node
from nodes.work_lane_router import work_lane_router_node
from nodes.proposal_review import proposal_review_node
from nodes.memory_audit import memory_audit_node
from nodes.synthesize_report import synthesize_report_node
from nodes.llm_synthesis import llm_synthesis_node


def build_graph(checkpointer=None):
    builder = StateGraph(SessionState)

    builder.add_node("load_context", load_context_node)
    builder.add_node("run_dossier", run_dossier_node)
    builder.add_node("work_lane_router", work_lane_router_node)
    builder.add_node("proposal_review", proposal_review_node)
    builder.add_node("memory_audit", memory_audit_node)
    builder.add_node("synthesize", synthesize_report_node)
    builder.add_node("llm_synthesis", llm_synthesis_node)

    builder.set_entry_point("load_context")
    builder.add_edge("load_context", "run_dossier")
    builder.add_edge("run_dossier", "work_lane_router")

    builder.add_conditional_edges(
        "work_lane_router",
        route_branches,
        {
            "proposal_review": "proposal_review",
            "memory_audit": "memory_audit",
            "synthesize": "synthesize",
        },
    )

    builder.add_edge("proposal_review", "synthesize")
    builder.add_edge("memory_audit", "synthesize")

    builder.add_conditional_edges(
        "synthesize",
        route_after_synthesize,
        {"llm_synthesis": "llm_synthesis", "__end__": END},
    )

    builder.add_edge("llm_synthesis", END)

    return builder.compile(checkpointer=checkpointer or MemorySaver())
