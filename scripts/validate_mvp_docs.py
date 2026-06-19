#!/usr/bin/env python3
"""Validate the docs skeleton created by scaffold_mvp_project.py."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED = {
    "goal.md": [
        "# Goal",
        "## User Request",
        "## MVP Definition",
        "## Assumptions",
        "## Non-Goals",
        "## Target User",
        "## Success Criteria",
    ],
    "mvp-flow.md": [
        "# MVP Flow",
        "## Milestone 1: Project Foundation",
        "## Milestone 2: Core Data or Domain Model",
        "## Milestone 3: Main User Workflow",
        "## Milestone 4: Verification and Demo",
        "## Later",
    ],
    "file-structure.md": ["# File Structure", "## Proposed Tree", "## Path Responsibilities"],
    "decisions.md": ["# Decisions", "## Technical Route", "## Initial Choices", "## Open Questions", "## Constraints"],
}


def validate_docs(target_dir: Path) -> list[str]:
    docs_dir = target_dir / "docs"
    errors: list[str] = []

    if not target_dir.exists():
        return [f"Directory not found: {target_dir}"]
    if not docs_dir.exists():
        return [f"docs directory not found: {docs_dir}"]
    if not (target_dir / "Archive").exists():
        errors.append(f"Archive directory not found: {target_dir / 'Archive'}")

    for filename, headings in REQUIRED.items():
        path = docs_dir / filename
        if not path.exists():
            errors.append(f"Missing {path}")
            continue
        content = path.read_text(encoding="utf-8")
        for heading in headings:
            if heading not in content:
                errors.append(f"{path} missing heading: {heading}")

    return errors


def validate(project_dir: Path, experiments: bool) -> list[str]:
    errors = validate_docs(project_dir)
    experiments_dir = project_dir / "experiments"

    if not experiments_dir.exists():
        errors.append(f"experiments directory not found: {experiments_dir}")
    elif experiments:
        for child in sorted(experiments_dir.iterdir()):
            if child.is_dir():
                errors.extend(validate_docs(child))

    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", help="Project folder containing docs/.")
    parser.add_argument("--experiments", action="store_true", help="Validate docs for each experiment directory too.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    errors = validate(Path(args.project_dir).expanduser().resolve(), args.experiments)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("MVP docs are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
