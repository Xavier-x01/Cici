from typing import TypedDict, Optional


class ProposalSummary(TypedDict):
    id: str
    target_surface: str
    summary: str
    status: str
    schema_valid: bool
    reviewer_notes: str


class OpenLoop(TypedDict):
    domain: str
    has_open_items: bool
    raw_text: str


class DossierData(TypedDict):
    surface_map_present: bool
    active_surfaces: list
    stub_surfaces: list
    proposal_queue_count: int
    evidence_artifact_count: int
    synthesis_count: int
    pending_review_count: int
    seed_phase_status: str
    recommendations: list
    raw: dict


class MemoryAuditResult(TypedDict):
    stub_surfaces_with_evidence: list
    tier_c_leaks: list
    overdue_proposals: list
    recommended_next_steps: list


class ProposalReviewResult(TypedDict):
    evaluated: list
    conflicts: list
    issues_found: bool


class SessionState(TypedDict):
    run_date: str
    repo_root: str
    proposals: list
    open_loops: list
    lane: str
    dossier: Optional[DossierData]
    proposal_review: Optional[ProposalReviewResult]
    memory_audit: Optional[MemoryAuditResult]
    report: str
    branches_taken: list
    errors: list
