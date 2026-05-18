#!/usr/bin/env python3
"""
museum-export.py — Generate a flat CSV from all artifact metadata.yaml files.

Usage:
  python3 scripts/museum-export.py
  python3 scripts/museum-export.py --out path/to/output.csv

Reads every metadata.yaml under "Predictive History Museum/" (excluding _templates/)
and writes one row per artifact to the CSV. Run from repo root.
"""

import csv
import sys
import os
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

COLUMNS = [
    "artifact_id",
    "chapter_id",
    "museum_part",
    "room",
    "title",
    "item_type",
    "local_original_path",
    "cloud_original_path",
    "source_url",
    "source_name",
    "rights_status",
    "storage_status",
    "checksum_sha256",
    "what_to_notice",
    "what_this_cannot_prove",
    "lecture_connection",
    "curator_note",
    "metadata_file",
]


def load_metadata(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        return {}
    row = {col: "" for col in COLUMNS}
    for col in COLUMNS:
        val = data.get(col, "")
        if val is None:
            val = ""
        row[col] = str(val).strip()
    row["metadata_file"] = str(path)
    return row


def main():
    parser = argparse.ArgumentParser(description="Export museum metadata to CSV")
    parser.add_argument(
        "--out",
        default="Predictive History Museum/artifact-inventory.csv",
        help="Output CSV path (default: Predictive History Museum/artifact-inventory.csv)",
    )
    parser.add_argument(
        "--museum-dir",
        default="Predictive History Museum",
        help="Museum root directory",
    )
    args = parser.parse_args()

    museum_root = Path(args.museum_dir)
    if not museum_root.exists():
        print(f"ERROR: Museum directory not found: {museum_root}", file=sys.stderr)
        sys.exit(1)

    files = sorted(
        p for p in museum_root.rglob("metadata.yaml")
        if "_templates" not in p.parts
    )

    if not files:
        print("No metadata.yaml files found (outside _templates/).", file=sys.stderr)
        sys.exit(1)

    rows = [load_metadata(f) for f in files]
    rows = [r for r in rows if r]

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} artifacts to {out_path}")
    for r in rows:
        print(f"  {r['artifact_id']:20s}  {r['chapter_id']:10s}  {r['room']:35s}  {r['title'][:50]}")


if __name__ == "__main__":
    main()
