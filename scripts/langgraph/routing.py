def route_branches(state: dict) -> str:
    """
    Returns the next node name based on current state.
    Priority: proposals > stub surfaces > synthesize directly.
    Pure function — no LangGraph import needed.
    """
    if state.get("proposals"):
        return "proposal_review"
    dossier = state.get("dossier") or {}
    if dossier.get("stub_surfaces"):
        return "memory_audit"
    return "synthesize"
