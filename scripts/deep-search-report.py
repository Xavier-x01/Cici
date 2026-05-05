#!/usr/bin/env python3
"""
deep-search-report.py

Generates a structured deep-search synthesis report from MCP search results
and local governed-state artifacts.

USAGE

  python3 scripts/deep-search-report.py --query "<query>" [options]

  Options:
    --query TEXT        The search query to synthesize (required)
    --results FILE      Path to JSON file containing MCP search results
                        (array of {content, created_at, tags, score} objects)
    --recent FILE       Path to JSON file containing recent_thoughts results
    --output FILE       Output path for the synthesis report (default: stdout)
    --format md|json    Output format (default: md)
    --threshold FLOAT   Min similarity score to include (default: 0.5)
    --dry-run           Print what would be analyzed without writing

  Example:
    # First dump MCP results to a file from your MCP client, then:
    python3 scripts/deep-search-report.py \\
      --query "BrewMind pricing strategy" \\
      --results /tmp/search-results.json \\
      --recent /tmp/recent-thoughts.json \\
      --output prepared-context/synthesis/2026-05-05-pricing-deep-search.md

---

MCP RESULTS FORMAT

The --results file should be a JSON array:
[
  {
    "id": "...",
    "content": "...",
    "created_at": "2026-04-15T10:30:00Z",
    "tags": ["brewmind", "pricing"],
    "similarity": 0.87
  },
  ...
]

---

OUTPUT FORMAT

Produces a Markdown synthesis document (or JSON if --format json) with:
  - Direct answer summary
  - Per-result tier annotations ([C: supabase/...])
  - Confidence distribution (high/medium/low by similarity score)
  - Gap list (sub-questions with no results)
  - Recommended action queue

---
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
GOVERNED_STATE_DIR = ROOT / "users" / "cici" / "governed-state"
DOCS_DIR = ROOT / "docs"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a deep-search synthesis report from MCP results."
    )
    parser.add_argument("--query", required=True, help="The search query")
    parser.add_argument("--results", default=None, help="Path to MCP search results JSON")
    parser.add_argument("--recent", default=None, help="Path to recent_thoughts results JSON")
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")
    parser.add_argument("--format", choices=["md", "json"], default="md", help="Output format")
    parser.add_argument("--threshold", type=float, default=0.5, help="Min similarity score")
    parser.add_argument("--dry-run", action="store_true", help="Analyze without writing")
    return parser.parse_args()


def load_json_file(path, label):
    if path is None:
        return []
    try:
        with open(path) as f:
            data = json.load(f)
        if not isinstance(data, list):
            print(f"[warn] {label}: expected JSON array, got {type(data).__name__}", file=sys.stderr)
            return []
        return data
    except (json.JSONDecodeError, OSError) as e:
        print(f"[warn] Cannot read {label} at {path}: {e}", file=sys.stderr)
        return []


def score_confidence(similarity):
    if similarity is None:
        return "unknown"
    if similarity >= 0.80:
        return "high"
    if similarity >= 0.65:
        return "medium"
    return "low"


def format_tier_tag(result):
    hint = result.get("id", "")[:8] or "unknown"
    date_hint = ""
    created = result.get("created_at", "")
    if created:
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            date_hint = dt.strftime("%Y%m%d")
        except (ValueError, AttributeError):
            pass
    tag_hint = f"{date_hint}-{hint}" if date_hint else hint
    return f"[C: supabase/{tag_hint}]"


def scan_governed_state():
    """Scan governed-state for relevant files and return a summary."""
    findings = []
    key_paths = [
        GOVERNED_STATE_DIR / "identity" / "instance.json",
        GOVERNED_STATE_DIR / "voice" / "session-behavior.json",
        GOVERNED_STATE_DIR / "memory-policy" / "policy.json",
        GOVERNED_STATE_DIR / "source-priority" / "policy.json",
        DOCS_DIR / "companion-agent" / "brewmind-companion-contract.md",
        DOCS_DIR / "companion-agent" / "brewmind-open-loops.md",
    ]
    for path in key_paths:
        if path.exists():
            rel = path.relative_to(ROOT)
            findings.append({
                "path": str(rel),
                "exists": True,
                "tier": "A" if "governed-state" in str(path) else "B",
            })
        else:
            findings.append({
                "path": str(path.relative_to(ROOT)),
                "exists": False,
                "tier": None,
            })
    return findings


def build_report_md(query, search_results, recent_results, governed_findings, threshold, today):
    lines = []
    lines.append(f"## Deep Search Synthesis")
    lines.append(f"**Query:** {query}")
    lines.append(f"**Date:** {today}")
    lines.append(f"**Generated by:** scripts/deep-search-report.py")
    lines.append("")

    # Filter by threshold
    filtered = [r for r in search_results if (r.get("similarity") or 0) >= threshold]
    recent_filtered = [r for r in recent_results if (r.get("similarity") or 1) >= threshold]
    all_results = filtered + recent_filtered

    lines.append("### Verified knowledge (Tier A/B — governed-state)")
    active_gs = [f for f in governed_findings if f["exists"]]
    if active_gs:
        for f in active_gs:
            tier_tag = f"[{f['tier']}: {f['path']}]"
            lines.append(f"- `{f['path']}` exists — review manually for query relevance {tier_tag}")
    else:
        lines.append("- No governed-state files found (check path configuration)")
    lines.append("")

    lines.append("### Memory signals (Tier C — Supabase)")
    if all_results:
        by_confidence = {"high": [], "medium": [], "low": [], "unknown": []}
        for r in all_results:
            conf = score_confidence(r.get("similarity"))
            by_confidence[conf].append(r)

        for level in ("high", "medium", "low"):
            group = by_confidence[level]
            if not group:
                continue
            lines.append(f"\n**{level.capitalize()} confidence ({len(group)} results):**")
            for r in group:
                tag = format_tier_tag(r)
                content = r.get("content", "").strip()
                preview = content[:200] + "..." if len(content) > 200 else content
                score = r.get("similarity")
                score_str = f" (score: {score:.3f})" if score is not None else ""
                tags = r.get("tags") or []
                tag_str = f" tags: {', '.join(tags)}" if tags else ""
                lines.append(f"- {preview}{score_str}{tag_str} {tag}")
    else:
        lines.append("- No results above threshold (threshold: {:.2f})".format(threshold))
        lines.append("- **This is a gap** — no Supabase memory found for this query")
    lines.append("")

    lines.append("### Gaps")
    if not all_results:
        lines.append(f"- Full gap: no Supabase results found for \"{query}\"")
        lines.append("  → Recommended: capture relevant context to Supabase for future recall")
    else:
        low_coverage = [r for r in all_results if (r.get("similarity") or 0) < 0.65]
        if len(low_coverage) == len(all_results):
            lines.append("- All results are low-confidence — semantic coverage is sparse")
            lines.append("  → Consider capturing a more detailed summary to improve future recall")
        else:
            lines.append("- Run `/deep-search` for sub-question-level gap analysis")
    lines.append("")

    lines.append("### Recommended actions")
    lines.append("| Action | Type | Priority |")
    lines.append("|--------|------|----------|")
    if not all_results:
        lines.append(f"| Capture notes on \"{query}\" to Supabase | capture | high |")
    else:
        high_conf = [r for r in all_results if score_confidence(r.get("similarity")) == "high"]
        if high_conf:
            lines.append(f"| Review {len(high_conf)} high-confidence result(s) for promotion | review | medium |")
        lines.append(f"| Run /deep-search for full sub-question analysis | search | medium |")
        lines.append(f"| Verify any BrewMind-related C-tier claims | verify | high |")
    lines.append("")

    lines.append("---")
    lines.append("_Report generated by `scripts/deep-search-report.py`. All MCP results are Tier C._")
    lines.append("_Cross-reference governed-state manually before citing any finding as verified fact._")

    return "\n".join(lines)


def build_report_json(query, search_results, recent_results, governed_findings, threshold, today):
    filtered = [r for r in search_results if (r.get("similarity") or 0) >= threshold]
    recent_filtered = [r for r in recent_results if (r.get("similarity") or 1) >= threshold]

    annotated = []
    for r in filtered + recent_filtered:
        annotated.append({
            **r,
            "tier": "C",
            "tier_source": "supabase",
            "confidence": score_confidence(r.get("similarity")),
            "tier_tag": format_tier_tag(r),
        })

    return {
        "query": query,
        "date": today,
        "generator": "scripts/deep-search-report.py",
        "threshold": threshold,
        "governed_state_scan": governed_findings,
        "results": annotated,
        "result_count": len(annotated),
        "gaps": len(annotated) == 0,
    }


def main():
    args = parse_args()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    search_results = load_json_file(args.results, "search results")
    recent_results = load_json_file(args.recent, "recent thoughts")
    governed_findings = scan_governed_state()

    total = len(search_results) + len(recent_results)
    print(f"[deep-search-report] Query: {args.query!r}", file=sys.stderr)
    print(f"[deep-search-report] Loaded {len(search_results)} search + {len(recent_results)} recent = {total} total results", file=sys.stderr)
    print(f"[deep-search-report] Governed-state files found: {sum(1 for f in governed_findings if f['exists'])}/{len(governed_findings)}", file=sys.stderr)

    if args.format == "json":
        report_data = build_report_json(
            args.query, search_results, recent_results, governed_findings, args.threshold, today
        )
        report_str = json.dumps(report_data, indent=2)
    else:
        report_str = build_report_md(
            args.query, search_results, recent_results, governed_findings, args.threshold, today
        )

    if args.dry_run:
        print("[dry-run] Report preview (first 40 lines):", file=sys.stderr)
        for line in report_str.splitlines()[:40]:
            print(f"  {line}", file=sys.stderr)
        return

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            f.write(report_str)
        print(f"[deep-search-report] Written to {out_path}", file=sys.stderr)
        print(f"Next: review the report and run /deep-search for full sub-question analysis.", file=sys.stderr)
    else:
        print(report_str)


if __name__ == "__main__":
    main()
