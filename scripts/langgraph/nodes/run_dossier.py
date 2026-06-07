import importlib.util
from pathlib import Path

from state import SessionState, DossierData


def _load_generate_dossier():
    scripts_dir = Path(__file__).parents[2]  # scripts/langgraph/nodes/../../ = scripts/
    spec = importlib.util.spec_from_file_location(
        "generate_dossier",
        scripts_dir / "generate-dossier.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_dossier_node(state: SessionState) -> dict:
    errors = list(state.get("errors", []))
    root = Path(state["repo_root"])
    instance_dir = root / "users" / "cici"

    try:
        dossier_mod = _load_generate_dossier()
        gs = dossier_mod.audit_governed_state(instance_dir)
        seed = dossier_mod.audit_seed_phase(instance_dir)
        proposals = dossier_mod.audit_proposals()
        events = dossier_mod.audit_events()
        evidence = dossier_mod.audit_evidence()
        pc = dossier_mod.audit_prepared_context()
        recs = dossier_mod.generate_recommendations(gs, seed, proposals, evidence, pc)

        dossier: DossierData = {
            "surface_map_present": gs["surface_map_present"],
            "active_surfaces": gs["active_surfaces"],
            "stub_surfaces": gs["stub_surfaces"],
            "proposal_queue_count": proposals["queue"],
            "evidence_artifact_count": evidence["artifact_count"],
            "synthesis_count": pc.get("synthesis", 0),
            "pending_review_count": pc.get("pending-review", 0),
            "seed_phase_status": seed.get("seed_phase_status", "unknown"),
            "recommendations": recs,
            "raw": {
                "gs": gs,
                "seed": seed,
                "proposals": proposals,
                "events": events,
                "evidence": evidence,
                "pc": pc,
            },
        }
    except Exception as e:
        errors.append(f"run_dossier: {e}")
        dossier = None  # type: ignore

    return {"dossier": dossier, "errors": errors}
