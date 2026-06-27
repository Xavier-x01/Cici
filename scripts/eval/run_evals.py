#!/usr/bin/env python3
"""
Lightweight eval harness for Cici's agents.

Surfaces:
  tier-c    — Tier C leak detection (component eval, no API)
  proposal  — Proposal schema validation (component eval, no API)
  router    — Intent classification (prompt eval, requires ANTHROPIC_API_KEY)

Usage:
  python3 scripts/eval/run_evals.py [--surface all|tier-c|proposal|router] [--output json|md]

Results are written to evals/results/YYYY-MM-DD-HH-MM.json
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATASET_PATH = REPO_ROOT / "evals" / "dataset.jsonl"
RESULTS_DIR = REPO_ROOT / "evals" / "results"

# Haiku pricing (per 1M tokens) as of 2026-06
HAIKU_INPUT_COST_PER_M = 0.80
HAIKU_OUTPUT_COST_PER_M = 4.00

_BUSINESS_PATTERN = re.compile(
    r"\b(pric(e|ing)|revenue|partner(ship)?|launch|cost|fee|charg(e|ing)|commit(ment)?)\b",
    re.IGNORECASE,
)
_TIER_TAG = re.compile(r"\[(A|B)\]")

_REQUIRED_FIELDS = {"id", "target_surface", "summary", "status", "created_at"}
_VALID_STATUSES = {"pending_review", "draft", "approved", "rejected", "deferred", "proposed"}


# ---------------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------------

def load_dataset(surface_filter: str) -> list:
    examples = []
    with open(DATASET_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            ex = json.loads(line)
            if surface_filter == "all" or ex["surface"] == surface_filter:
                examples.append(ex)
    return examples


# ---------------------------------------------------------------------------
# Tier C component eval
# ---------------------------------------------------------------------------

def _check_tier_c(text: str) -> bool:
    """Return True if the text looks like an unannotated business claim."""
    stripped = text.strip()
    if not stripped or stripped.startswith(("#", ">")):
        return False
    return bool(_BUSINESS_PATTERN.search(stripped)) and not bool(_TIER_TAG.search(stripped))


def eval_tier_c(examples: list) -> dict:
    results = []
    correct = 0
    for ex in examples:
        text = ex["input"]
        expected_flagged = ex["expected"]["flagged"]
        actual_flagged = _check_tier_c(text)
        passed = actual_flagged == expected_flagged
        if passed:
            correct += 1
        results.append({
            "id": ex["id"],
            "input": text[:80],
            "expected_flagged": expected_flagged,
            "actual_flagged": actual_flagged,
            "passed": passed,
        })
    return {
        "surface": "tier-c",
        "total": len(examples),
        "correct": correct,
        "accuracy": round(correct / len(examples), 3) if examples else 0,
        "results": results,
    }


# ---------------------------------------------------------------------------
# Proposal component eval
# ---------------------------------------------------------------------------

def _validate_proposal(data: dict) -> tuple[bool, list]:
    """Validate proposal dict. Returns (valid, list_of_issue_keys)."""
    issues = []
    missing = _REQUIRED_FIELDS - set(data.keys())
    if missing:
        issues.append("missing fields")
    status = data.get("status")
    if status and status not in _VALID_STATUSES:
        issues.append("unknown status")
    valid = len(issues) == 0
    return valid, issues


def eval_proposal(examples: list) -> dict:
    results = []
    correct = 0
    for ex in examples:
        data = ex["input"]
        expected_valid = ex["expected"]["valid"]
        expected_issues = ex["expected"].get("issues", [])
        actual_valid, actual_issues = _validate_proposal(data)
        # Pass if validity matches; issue keywords are checked for debugging only
        passed = actual_valid == expected_valid
        # Secondary check: if expected has issue keywords, verify they appear
        if passed and expected_issues:
            for kw in expected_issues:
                if not any(kw in ai for ai in actual_issues):
                    passed = False
                    break
        if passed:
            correct += 1
        results.append({
            "id": ex["id"],
            "expected_valid": expected_valid,
            "actual_valid": actual_valid,
            "expected_issues": expected_issues,
            "actual_issues": actual_issues,
            "passed": passed,
        })
    return {
        "surface": "proposal",
        "total": len(examples),
        "correct": correct,
        "accuracy": round(correct / len(examples), 3) if examples else 0,
        "results": results,
    }


# ---------------------------------------------------------------------------
# Router prompt eval (Claude API)
# ---------------------------------------------------------------------------

ROUTER_SYSTEM_PROMPT = """You are Cici's intent router. Your sole job is to classify one incoming user message and return a routing card. You do not take action, write anything, or follow up — classify and stop.

## Step 1 — Lane classification

Determine which operator lane applies:

| Lane | When to assign |
|------|----------------|
| PLAN | Exploring, reviewing, thinking, asking opinions, planning, learning, anything ambiguous |
| EXECUTE | Explicit request to implement, commit, push, build, create, or apply a change |
| DOCSYNC | Docs-only fixes: stale links, path corrections, header sync, README updates |

Default to PLAN when uncertain. EXECUTE requires an unambiguous "do it" signal. DOCSYNC requires an unambiguous "docs only" signal.

## Step 2 — Command / agent match

| Signal in request | Route to |
|---|---|
| "search", "find", "what do we know", "look up in memory" | /deep-search |
| "propose a change", "draft a proposal", "new proposal" | /draft-proposal |
| "review the proposal", "approve or reject", "evaluate proposal" | /review-governed-change |
| "apply the proposal", "promote to governed state" | /promote-to-governed-state |
| "what should I work on", "what's next", "surface next" | /surface-next |
| "start the session", "startup", "open loops", "status" | /session-start |
| "stage evidence", "import", "export from supabase" | evidence-stager |
| "improve Cici", "behavioral gap", "self-improve" | self-improver |
| "doctor", "health check", "preflight" | dev-hygiene |
| "weekly review", "review the week" | /weekly-review |
| "daily task", "what's today's task" | /daily-task |
| "memory audit", "audit the memory" | /memory-audit |
| "log a tension", "conflict between" | /log-tension |

If no command or agent clearly matches, use none.

## Output format

Return exactly this JSON object and nothing else:
{"lane": "PLAN|EXECUTE|DOCSYNC", "command": "/command-name or none", "agent": "agent-name or none", "confidence": 0.00}"""


def _parse_router_output(text: str) -> dict:
    """Extract JSON routing card from model response."""
    text = text.strip()
    # Try direct JSON parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Try extracting JSON block
    match = re.search(r'\{[^{}]+\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    # Fallback: extract lane at minimum
    lane_match = re.search(r'\b(PLAN|EXECUTE|DOCSYNC)\b', text)
    lane = lane_match.group(1) if lane_match else "PLAN"
    return {"lane": lane, "command": "none", "agent": "none", "confidence": 0.5}


def eval_router(examples: list) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("  ANTHROPIC_API_KEY not set — skipping router evals", file=sys.stderr)
        return {
            "surface": "router",
            "total": len(examples),
            "correct": 0,
            "accuracy": None,
            "skipped": True,
            "reason": "ANTHROPIC_API_KEY not set",
            "results": [],
        }

    try:
        import anthropic
    except ImportError:
        print("  anthropic package not installed — run: pip install anthropic", file=sys.stderr)
        return {
            "surface": "router",
            "total": len(examples),
            "correct": 0,
            "accuracy": None,
            "skipped": True,
            "reason": "anthropic package not installed",
            "results": [],
        }

    client = anthropic.Anthropic(api_key=api_key)
    results = []
    correct = 0
    total_input_tokens = 0
    total_output_tokens = 0
    total_latency_ms = 0

    for ex in examples:
        query = ex["input"]
        expected = ex["expected"]
        t0 = time.monotonic()
        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=256,
                system=ROUTER_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": query}],
            )
            latency_ms = round((time.monotonic() - t0) * 1000)
            actual = _parse_router_output(response.content[0].text)
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
        except Exception as e:
            results.append({"id": ex["id"], "error": str(e), "passed": False})
            continue

        total_input_tokens += input_tokens
        total_output_tokens += output_tokens
        total_latency_ms += latency_ms

        lane_match = actual.get("lane") == expected.get("lane")
        # Command/agent match is checked loosely (strip leading slash for comparison)
        expected_cmd = (expected.get("command") or "none").lstrip("/")
        actual_cmd = (actual.get("command") or "none").lstrip("/")
        expected_agent = expected.get("agent") or "none"
        actual_agent = actual.get("agent") or "none"
        cmd_match = expected_cmd == "none" or expected_cmd in actual_cmd or actual_cmd in expected_cmd
        agent_match = expected_agent == "none" or expected_agent in actual_agent or actual_agent in expected_agent
        passed = lane_match and cmd_match and agent_match

        if passed:
            correct += 1

        results.append({
            "id": ex["id"],
            "input": query,
            "expected": expected,
            "actual": actual,
            "lane_match": lane_match,
            "cmd_match": cmd_match,
            "agent_match": agent_match,
            "passed": passed,
            "latency_ms": latency_ms,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        })

    n = len(results)
    cost_usd = (
        (total_input_tokens / 1_000_000 * HAIKU_INPUT_COST_PER_M)
        + (total_output_tokens / 1_000_000 * HAIKU_OUTPUT_COST_PER_M)
    ) if n > 0 else 0

    return {
        "surface": "router",
        "total": len(examples),
        "correct": correct,
        "accuracy": round(correct / len(examples), 3) if examples else 0,
        "avg_latency_ms": round(total_latency_ms / n) if n > 0 else 0,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "cost_usd": round(cost_usd, 6),
        "results": results,
    }


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_md(surface_results: list, run_ts: str) -> str:
    lines = [f"# Cici Eval Run — {run_ts}\n"]
    for sr in surface_results:
        surface = sr["surface"]
        lines.append(f"## {surface}")
        if sr.get("skipped"):
            lines.append(f"**Skipped:** {sr['reason']}\n")
            continue
        acc = sr.get("accuracy")
        acc_str = f"{acc:.1%}" if acc is not None else "n/a"
        lines.append(f"**Accuracy:** {acc_str}  ({sr['correct']}/{sr['total']})")
        if "avg_latency_ms" in sr:
            lines.append(f"**Avg latency:** {sr['avg_latency_ms']} ms")
        if "cost_usd" in sr:
            lines.append(f"**Cost:** ${sr['cost_usd']:.6f}")
        failures = [r for r in sr.get("results", []) if not r.get("passed")]
        if failures:
            lines.append(f"\n### Failures ({len(failures)})")
            for f in failures:
                lines.append(f"- `{f['id']}`: {json.dumps(f.get('actual', f.get('actual_issues', '')))}")
        else:
            lines.append("\nAll examples passed.")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Cici eval harness")
    parser.add_argument("--surface", default="all", choices=["all", "tier-c", "proposal", "router"])
    parser.add_argument("--output", default="md", choices=["json", "md"])
    args = parser.parse_args()

    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M")
    examples = load_dataset(args.surface)

    all_results = []

    surfaces_to_run = (
        ["tier-c", "proposal", "router"] if args.surface == "all"
        else [args.surface]
    )

    for surface in surfaces_to_run:
        surface_examples = [e for e in examples if e["surface"] == surface]
        if not surface_examples:
            continue
        print(f"Running {surface} ({len(surface_examples)} examples)...")
        if surface == "tier-c":
            result = eval_tier_c(surface_examples)
        elif surface == "proposal":
            result = eval_proposal(surface_examples)
        elif surface == "router":
            result = eval_router(surface_examples)
        else:
            continue
        all_results.append(result)
        acc = result.get("accuracy")
        if acc is not None:
            print(f"  accuracy: {acc:.1%}  ({result['correct']}/{result['total']})")
        else:
            print(f"  skipped: {result.get('reason', '')}")

    # Write results JSON
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    result_path = RESULTS_DIR / f"{run_ts}.json"
    payload = {"run_ts": run_ts, "surfaces": all_results}
    result_path.write_text(json.dumps(payload, indent=2))
    print(f"\nResults written to {result_path.relative_to(REPO_ROOT)}")

    if args.output == "md":
        print("\n" + format_md(all_results, run_ts))


if __name__ == "__main__":
    main()
