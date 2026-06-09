def route_branches(state: dict) -> str:
    """Priority: proposals > stub surfaces > synthesize directly."""
    if state.get("proposals"):
        return "proposal_review"
    dossier = state.get("dossier") or {}
    if dossier.get("stub_surfaces"):
        return "memory_audit"
    return "synthesize"


def route_after_synthesize(state: dict) -> str:
    """Gate the LLM node behind the --llm flag."""
    if state.get("use_llm"):
        return "llm_synthesis"
    return "__end__"
