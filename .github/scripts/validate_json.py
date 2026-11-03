#!/usr/bin/env python3
"""Parse every JSON file and reject duplicate keys."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP = {".git", "node_modules"}


def reject_duplicates(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate key {key!r}")
        seen[key] = value
    return seen


def main():
    files = sorted(
        path
        for path in ROOT.rglob("*.json")
        if not any(part in SKIP for part in path.parts)
    )
    if not files:
        print("no JSON files found", file=sys.stderr)
        return 1
    for path in files:
        text = path.read_text(encoding="utf-8")
        try:
            value = json.loads(text, object_pairs_hook=reject_duplicates)
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"{path.relative_to(ROOT)}: {exc}", file=sys.stderr)
            return 1
        if not isinstance(value, dict):
            print(f"{path.relative_to(ROOT)}: expected a JSON object", file=sys.stderr)
            return 1
        print(f"ok {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
