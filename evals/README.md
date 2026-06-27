# Cici Eval Layer

Lightweight evaluation harness for Cici's agents. Tracks output quality (accuracy, latency, cost) as prompts and tools evolve.

## Surfaces

| Surface | Count | Method | API needed |
|---|---|---|---|
| `tier-c` | 20 | Regex component eval | No |
| `proposal` | 10 | Schema validation component eval | No |
| `router` | 20 | Prompt eval via Claude API | Yes (Haiku) |

## Running Evals

```bash
# All surfaces (router requires ANTHROPIC_API_KEY)
python3 scripts/eval/run_evals.py

# Single surface (no API key needed)
python3 scripts/eval/run_evals.py --surface tier-c
python3 scripts/eval/run_evals.py --surface proposal

# Router only (prompt eval)
ANTHROPIC_API_KEY=sk-... python3 scripts/eval/run_evals.py --surface router

# JSON output
python3 scripts/eval/run_evals.py --output json
```

## Results

Results are written to `evals/results/YYYY-MM-DD-HH-MM.json`. Each file contains per-example pass/fail, plus summary metrics:

- `accuracy` — fraction of examples matching expected output
- `avg_latency_ms` — wall-clock time per API call (router only)
- `cost_usd` — estimated cost at Haiku pricing (router only)

## Dataset

`evals/dataset.jsonl` — 50 labeled examples. Each record has:
- `id` — unique identifier
- `surface` — which eval surface (`tier-c`, `proposal`, `router`)
- `input` — the query or text to evaluate
- `expected` — ground-truth output fields

To extend the dataset, add lines to `dataset.jsonl` following the existing format. Run evals after every prompt change or agent update.

> **Known gap (tier-c):** The regex uses `\blaunch\b` (strict word boundary), so "launches" is not flagged. `tier-c-001` in the dataset deliberately captures this — the 95% baseline reflects a real detection hole, not a dataset error. Fix in `scripts/langgraph/nodes/memory_audit.py` to close it.

## When to Run

- After changing any agent prompt in `.claude/agents/`
- After modifying the Tier C detection regex in `scripts/langgraph/nodes/memory_audit.py`
- After updating proposal schema requirements
- Before merging changes to governed-state surfaces
