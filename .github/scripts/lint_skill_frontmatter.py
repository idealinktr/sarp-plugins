#!/usr/bin/env python3
"""Lint SKILL.md frontmatter for the organizational-memory plugin."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "plugins" / "sarp-organizational-memory" / "skills"
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED = {
    "name",
    "description",
    "when_to_use",
    "argument-hint",
    "arguments",
    "disable-model-invocation",
    "user-invocable",
    "allowed-tools",
    "disallowed-tools",
    "model",
    "effort",
    "context",
    "agent",
    "background",
    "hooks",
    "paths",
    "shell",
    "metadata",
    "license",
    "compatibility",
}


def fail(path, message):
    print(f"{path}: {message}", file=sys.stderr)
    return 1


def parse(text, label):
    if not text.startswith("---\n"):
        return None, fail(label, "frontmatter must start at the first line")
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, fail(label, "frontmatter must close with ---")
    raw = text[4:end]
    body = text[end + 5 :]
    if not body.strip():
        return None, fail(label, "skill body is empty")
    fields = {}
    status = 0
    for number, line in enumerate(raw.splitlines(), start=2):
        if not line.strip():
            continue
        if line.startswith(" ") or line.startswith("\t") or ":" not in line:
            status |= fail(label, f"line {number} is not a flat key")
            continue
        key, value = line.split(":", 1)
        if key in fields:
            status |= fail(label, f"duplicate field {key}")
        fields[key] = value.strip()
    return (fields, body), status


def lint(path):
    label = path.relative_to(ROOT)
    parsed, status = parse(path.read_text(encoding="utf-8"), label)
    if parsed is None:
        return status
    fields, _body = parsed
    unknown = sorted(set(fields) - ALLOWED)
    if unknown:
        status |= fail(label, f"unknown frontmatter fields {unknown}")
    name = fields.get("name", "")
    if NAME.fullmatch(name) is None or len(name) > 64:
        status |= fail(label, "name must be kebab-case, 1-64 characters")
    elif name != path.parent.name:
        status |= fail(label, f"name {name!r} does not match directory {path.parent.name!r}")
    description = fields.get("description", "")
    if not description:
        status |= fail(label, "description is required")
    elif len(description) > 1024:
        status |= fail(label, "description is longer than 1024 characters")
    return status


def main():
    files = sorted(SKILLS.glob("*/SKILL.md"))
    if len(files) < 4:
        print(f"expected at least 4 skills, found {len(files)}", file=sys.stderr)
        return 1
    status = 0
    for path in files:
        status |= lint(path)
        if status == 0:
            print(f"ok {path.relative_to(ROOT)}")
    return 1 if status else 0


if __name__ == "__main__":
    sys.exit(main())
