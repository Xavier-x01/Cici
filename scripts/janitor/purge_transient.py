#!/usr/bin/env python3
"""
Janitor: purge transient memories older than 7 days.

DOCTRINE: users/cici/governed-state/memory-policy/retention-policy.md

Usage:
  python purge_transient.py            # dry run (default — safe)
  python purge_transient.py --execute  # live delete

Requires env vars: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
"""

import os
import sys
import datetime

try:
    from supabase import create_client, Client
except ImportError:
    print("[!] Missing dependency: pip install supabase")
    sys.exit(1)

TABLE = "memories"
RETENTION_DAYS = 7
DRY_RUN_FLAG = "--execute"


def run(dry_run: bool = True) -> None:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

    if not url or not key:
        print("[!] SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set.")
        sys.exit(1)

    supabase: Client = create_client(url, key)

    cutoff = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=RETENTION_DAYS)).isoformat()
    mode_label = "DRY RUN" if dry_run else "LIVE DELETE"

    print(f"[*] Janitor — {mode_label}")
    print(f"[*] Target table : {TABLE}")
    print(f"[*] Filter       : durability == 'transient'  AND  governed != 'true'")
    print(f"[*] Cutoff       : created_at < {cutoff}")
    print()

    # SELECT to preview what would be deleted (always safe).
    # Both conditions must be true to be eligible:
    #   1. durability == 'transient'  (explicit opt-in to deletion)
    #   2. governed  != 'true'        (secondary shield — governed rows are untouchable)
    preview = (
        supabase.table(TABLE)
        .select("id, created_at, metadata")
        .eq("metadata->>durability", "transient")
        .neq("metadata->>governed", "true")
        .lt("created_at", cutoff)
        .execute()
    )

    candidates = preview.data or []
    print(f"[*] Candidate rows: {len(candidates)}")

    if not candidates:
        print("[+] Nothing to purge. Exiting.")
        return

    for row in candidates[:10]:
        meta = row.get("metadata") or {}
        durability = meta.get("durability", "<missing>")
        governed = meta.get("governed", "<missing>")
        print(
            f"    id={row.get('id')}  "
            f"created_at={row.get('created_at')}  "
            f"durability={durability}  governed={governed}"
        )
    if len(candidates) > 10:
        print(f"    ... and {len(candidates) - 10} more.")

    print()

    if dry_run:
        print("[~] DRY RUN complete. No rows deleted.")
        print(f"[~] Re-run with  `python {sys.argv[0]} --execute`  to delete.")
        return

    # LIVE DELETE — only reached with --execute.
    # Mirrors the SELECT filters exactly so the two can never diverge.
    response = (
        supabase.table(TABLE)
        .delete()
        .eq("metadata->>durability", "transient")
        .neq("metadata->>governed", "true")
        .lt("created_at", cutoff)
        .execute()
    )

    deleted = len(response.data) if response.data else 0
    print(f"[+] Deleted {deleted} rows.")


if __name__ == "__main__":
    execute = DRY_RUN_FLAG in sys.argv
    run(dry_run=not execute)
