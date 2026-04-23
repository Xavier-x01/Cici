# Operation: Janitor Purge

**Status:** ACTIVE  
**Owner:** Cici  
**Target:** Runtime Storage (Supabase — `memories` table)  
**Doctrine:** `users/cici/governed-state/memory-policy/retention-policy.md`

---

## Logic

| Step | Detail |
|------|--------|
| Filter | `metadata->>'durability' == 'transient'` |
| Threshold | `created_at < (NOW() - INTERVAL '7 days')` |
| Default mode | **Dry run** — SELECTs candidates and prints a preview, no deletes |
| Execute mode | Pass `--execute` flag to perform hard DELETE |

## Safety Rules

- Script **never** touches rows where `durability != 'transient'`.
- Governed-state files in Git are not affected — this script only touches Supabase runtime data.
- Always run without `--execute` first to review candidates.

## Invocation

```bash
# Preview (safe — default)
python scripts/janitor/purge_transient.py

# Live delete
python scripts/janitor/purge_transient.py --execute
```

## Required Environment Variables

| Variable | Source |
|----------|--------|
| `SUPABASE_URL` | Supabase project settings |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase project settings → API → service_role key |

Set them locally in a `.env` file (never committed) or export before running:

```bash
export SUPABASE_URL=https://<ref>.supabase.co
export SUPABASE_SERVICE_ROLE_KEY=<key>
```

## Scheduling (optional)

To run automatically, add a cron job or GitHub Actions scheduled workflow targeting this script. Recommended cadence: daily at 03:00 UTC.
