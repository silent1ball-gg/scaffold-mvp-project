#!/usr/bin/env python3
"""Create a project folder with an MVP docs skeleton."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DOCS = {
    "goal.md": """# Goal

## User Request

{goal}

## MVP Definition

Build the smallest core capability first on a technical route that should not need to be completely thrown away later.

## Assumptions

- TODO: Capture implementation assumptions.

## Non-Goals

- TODO: List what is intentionally out of scope for the MVP.

## Target User

- TODO: Describe the first user or operator.

## Success Criteria

- TODO: Define what makes the MVP usable.
""",
    "mvp-flow.md": """# MVP Flow

## Milestone 1: Project Foundation

- TODO: Create the repository or project folder.
- TODO: Confirm the future-preserving technical route, runtime, package manager, and local run command.
- Verification: TODO.

## Milestone 2: Core Data or Domain Model

- TODO: Define the smallest useful domain objects, files, or data shape.
- Verification: TODO.

## Milestone 3: Main User Workflow

- TODO: Implement the core workflow from input to useful output.
- Verification: TODO.

## Milestone 4: Verification and Demo

- TODO: Run the project locally and exercise the MVP path.
- TODO: Document known limitations.

## Later

- TODO: List enhancements that should wait until after the first usable demo.
""",
    "file-structure.md": """# File Structure

## Proposed Tree

```text
{project_name}/
├── docs/
│   ├── goal.md
│   ├── mvp-flow.md
│   ├── file-structure.md
│   └── decisions.md
├── Archive/
├── experiments/
│   └── <experiment-name>/
│       ├── Archive/
│       └── docs/
│           ├── goal.md
│           ├── mvp-flow.md
│           ├── file-structure.md
│           └── decisions.md
└── README.md
```

## Path Responsibilities

- `docs/`: Planning and handoff documents for the MVP.
- `docs/goal.md`: Goal, assumptions, non-goals, target user, and success criteria.
- `docs/mvp-flow.md`: Milestones from foundation to first demo.
- `docs/file-structure.md`: Proposed file tree and path responsibilities.
- `docs/decisions.md`: Initial choices, open questions, and constraints.
- `Archive/`: Archived plans, superseded notes, old experiment snapshots, and other retained material that should not clutter active docs.
- `experiments/`: Isolated mini-projects for experimental features.
- `experiments/<experiment-name>/docs/`: Experiment-specific goal, MVP flow, file structure, and decisions.
- `experiments/<experiment-name>/Archive/`: Archived material for that experiment.
- `README.md`: Short project entrypoint once implementation begins.
""",
    "decisions.md": """# Decisions

## Technical Route

- TODO: Choose a route that can support the future product direction without a full rewrite.

## Initial Choices

- TODO: Record chosen stack, runtime, or storage assumptions.

## Open Questions

- TODO: Capture questions that need user confirmation.

## Constraints

- TODO: Note time, platform, security, integration, or deployment constraints.
""",
}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "mvp-project"


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; pass --force to overwrite")
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_docs(target_dir: Path, display_name: str, goal: str, force: bool) -> None:
    docs_dir = target_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "Archive").mkdir(parents=True, exist_ok=True)

    for filename, template in DOCS.items():
        write_file(
            docs_dir / filename,
            template.format(goal=goal.strip() or "TODO: Paste the user request.", project_name=display_name),
            force,
        )


def scaffold_project(name: str, dest: Path, goal: str, force: bool) -> Path:
    project_name = slugify(name)
    project_dir = dest / project_name

    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "experiments").mkdir(parents=True, exist_ok=True)
    write_docs(project_dir, project_name, goal, force)

    return project_dir


def scaffold_experiment(project_dir: Path, experiment_name: str, goal: str, force: bool) -> Path:
    experiment_slug = slugify(experiment_name)
    experiment_dir = project_dir / "experiments" / experiment_slug

    experiment_dir.mkdir(parents=True, exist_ok=True)
    write_docs(experiment_dir, experiment_slug, goal, force)

    return experiment_dir


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="Project folder name; normalized to lowercase hyphen-case.")
    parser.add_argument("--goal", default="", help="Original user goal to place in docs/goal.md.")
    parser.add_argument("--dest", default=".", help="Destination directory where the project folder is created.")
    parser.add_argument("--experiment", help="Optional experiment feature name to scaffold under experiments/.")
    parser.add_argument("--experiment-goal", default="", help="Experiment-specific goal; defaults to --goal.")
    parser.add_argument(
        "--experiment-only",
        action="store_true",
        help="Create only the experiment docs inside an existing project; do not create or update root docs.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing docs files.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    dest = Path(args.dest).expanduser().resolve()
    project_dir = dest / slugify(args.name)

    if not args.experiment_only:
        project_dir = scaffold_project(args.name, dest, args.goal, args.force)
    elif not project_dir.exists():
        raise FileNotFoundError(f"{project_dir} does not exist; omit --experiment-only to create it")

    if args.experiment:
        experiment_dir = scaffold_experiment(
            project_dir,
            args.experiment,
            args.experiment_goal or args.goal,
            args.force,
        )
        print(experiment_dir)
    else:
        print(project_dir)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except FileExistsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
