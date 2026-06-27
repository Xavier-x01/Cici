from typing import TypedDict


class ProposalDraftState(TypedDict):
    natural_language_input: str
    repo_root: str
    known_surfaces: list        # surface IDs from surface-map.json
    next_sequence: int          # next available NNN for prop-YYYYMMDD-NNN
    parsed: dict                # {surface, change_type, summary} from parse_intent
    draft: dict                 # full proposal dict from draft_proposal
    validation_errors: list     # list of error strings from validate
    retry_count: int
    output_path: str            # written by write_to_queue
    dry_run: bool
    errors: list
