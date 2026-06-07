from state import SessionState


def synthesize_report_node(state: SessionState) -> dict:
    lines = []
    run_date = state.get("run_date", "unknown")
    lane = state.get("lane", "PLAN")
    branches = state.get("branches_taken", [])

    lines += [
        f"## Session Status — {run_date}",
        f"",
        f"**Lane:** {lane}  |  **Branches run:** {', '.join(branches) if branches else 'none (clean state)'}",
        f"",
        "---",
        "",
    ]

    # --- Open Proposals ---
    lines += ["### Open Proposals", ""]
    proposals = state.get("proposals", [])
    pr = state.get("proposal_review")
    if not proposals:
        lines.append("Queue is clear.")
    else:
        lines += ["| ID | Surface | Status | Valid | Notes |", "|---|---|---|---|---|"]
        for p in proposals:
            valid_str = "yes" if p.get("schema_valid") else "**NO**"
            lines.append(
                f"| `{p['id']}` | `{p['target_surface']}` | {p['status']} | {valid_str} | {p.get('reviewer_notes', '')} |"
            )
        if pr and pr.get("conflicts"):
            lines += ["", "**Conflicts detected:**"]
            for c in pr["conflicts"]:
                lines.append(f"- {c}")
    lines.append("")

    # --- Open Loops ---
    lines += ["---", "", "### Open Loops (BrewMind)", ""]
    open_loops = state.get("open_loops", [])
    if not open_loops:
        lines.append("Open-loops file not found or empty.")
    else:
        lines += ["| Domain | Status |", "|---|---|"]
        for loop in open_loops:
            status = "Open items present" if loop["has_open_items"] else "No open items"
            lines.append(f"| {loop['domain']} | {status} |")
    lines.append("")

    # --- Pipeline Health (from dossier) ---
    lines += ["---", "", "### Pipeline Health", ""]
    dossier = state.get("dossier")
    if dossier:
        seed_status = dossier.get("seed_phase_status", "unknown")
        active = dossier.get("active_surfaces", [])
        stubs = dossier.get("stub_surfaces", [])
        evidence_count = dossier.get("evidence_artifact_count", 0)
        synthesis_count = dossier.get("synthesis_count", 0)
        pending_count = dossier.get("pending_review_count", 0)
        lines += [
            f"- Seed phase: `{seed_status}`",
            f"- Active surfaces: {len(active)}  |  Stubs: {len(stubs)}"
            + (f" ({', '.join(stubs)})" if stubs else ""),
            f"- Evidence: {evidence_count} artifact(s)  |  Synthesis: {synthesis_count}  |  Pending review: {pending_count}",
            "",
        ]
        if dossier.get("recommendations"):
            lines.append("**Recommendations:**")
            for r in dossier["recommendations"]:
                lines.append(f"- {r}")
    else:
        lines.append("Dossier not available (run_dossier node failed — check errors).")
    lines.append("")

    # --- Memory Audit (if branch ran) ---
    ma = state.get("memory_audit")
    if ma is not None:
        lines += ["---", "", "### Memory Audit", ""]
        stubs_with_ev = ma.get("stub_surfaces_with_evidence", [])
        leaks = ma.get("tier_c_leaks", [])
        overdue = ma.get("overdue_proposals", [])

        lines.append(f"- Stub surfaces with evidence: {', '.join(stubs_with_ev) if stubs_with_ev else 'none'}")
        if leaks:
            lines.append(f"- Tier C leaks found: {len(leaks)}")
            for leak in leaks[:5]:  # show max 5
                lines.append(f"  - `{leak['file']}` line {leak['line']}: {leak['text']}")
        else:
            lines.append("- Tier C leaks: none detected")
        lines.append(f"- Overdue proposals: {', '.join(overdue) if overdue else 'none'}")
        lines.append("")

    # --- Errors ---
    errors = state.get("errors", [])
    if errors:
        lines += ["---", "", "### Warnings", ""]
        for e in errors:
            lines.append(f"- `{e}`")
        lines.append("")

    # --- Recommended Actions (consolidated) ---
    all_actions = list(dossier.get("recommendations", []) if dossier else [])
    existing_lower = {a.lower() for a in all_actions}
    if ma and ma.get("recommended_next_steps"):
        for step in ma["recommended_next_steps"]:
            if step.lower() not in existing_lower:
                all_actions.append(step)
                existing_lower.add(step.lower())

    if all_actions:
        lines += ["---", "", "### Recommended Actions", ""]
        for action in all_actions:
            lines.append(f"- {action}")
        lines.append("")

    report = "\n".join(lines)
    return {"report": report}
