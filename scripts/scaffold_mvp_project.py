#!/usr/bin/env python3
"""Create an MVP docs scaffold or update it for an accepted feature."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path


DOCS = {
    "goal.md": """# Goal

## User Request

{goal}

## Purpose Analysis

- TODO: Identify the real outcome the user wants.
- TODO: Name the first user or operator and their core job-to-be-done.
- TODO: Separate the minimum core value from nice-to-have details.

## MVP Definition

Use one long-lived, maintainable technical route that should remain valid as the project grows, then build the smallest core capability that serves the user's purpose.

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
- TODO: Confirm the long-lived maintainable technical route, runtime, package manager, and local run command.
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

## Long-Term Maintainable Technical Route

- TODO: Choose a route that can support the future product direction without a full rewrite.
- TODO: Explain why this route remains maintainable after the MVP grows.

## Initial Choices

- TODO: Record chosen stack, runtime, or storage assumptions.

## Open Questions

- TODO: Capture questions that need user confirmation.

## Constraints

- TODO: Note time, platform, security, integration, or deployment constraints.
""",
}


FEATURE_DOCS = {
    "goal.md": """## Feature: {feature_name}

### User Request

{goal}

### Purpose Analysis

- TODO: Identify the outcome this feature adds to the completed MVP.
- TODO: Name the user or operator and the job this feature improves.
- TODO: Confirm that the feature belongs in the product rather than an experiment.

### Minimum Feature Scope

- TODO: Define the smallest end-to-end capability that delivers the new value.

### Non-Goals

- TODO: List adjacent work that is intentionally excluded from this iteration.

### Success Criteria

- TODO: Define observable acceptance and regression criteria.
""",
    "mvp-flow.md": """## Feature Flow: {feature_name}

### Milestone 1: Current State and Route Fit

- TODO: Inspect the implemented MVP, active docs, tests, and current interfaces.
- TODO: Confirm how the feature extends the existing long-term technical route.
- Verification: TODO.

### Milestone 2: Domain or Interface Change

- TODO: Define the smallest data, API, or UI change required by the feature.
- Verification: TODO.

### Milestone 3: End-to-End Feature Workflow

- TODO: Implement the smallest complete path from user action to useful result.
- Verification: TODO.

### Milestone 4: Regression Check and Demo

- TODO: Verify the new feature and the original MVP workflow.
- TODO: Update user-facing entrypoints and known limitations.

### Later

- TODO: List follow-up improvements that are outside this feature iteration.
""",
    "file-structure.md": """## Feature Structure Update: {feature_name}

### Current Structure Impact

- TODO: Identify existing modules and boundaries affected by the feature.

### Proposed Changes

```text
TODO: Show only new or changed paths, then reconcile them with the main tree above.
```

### Path Responsibilities

- TODO: Describe the responsibility of each new or changed path.
""",
    "decisions.md": """## Feature Decision: {feature_name}

### Long-Term Route Fit

- TODO: Explain how the feature fits the existing maintainable technical route.

### Chosen Approach

- TODO: Record the smallest durable implementation choice.

### Compatibility and Migration

- TODO: Record data, API, configuration, or user-workflow compatibility concerns.

### Open Questions

- TODO: Capture decisions that still need confirmation.

### Constraints

- TODO: Note feature-specific platform, security, performance, or delivery constraints.
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


def feature_markers(feature_slug: str) -> tuple[str, str]:
    return f"<!-- feature:{feature_slug}:start -->", f"<!-- feature:{feature_slug}:end -->"


def render_feature_block(template: str, feature_name: str, feature_slug: str, goal: str) -> str:
    start, end = feature_markers(feature_slug)
    body = template.format(
        feature_name=feature_name.strip() or feature_slug,
        goal=goal.strip() or "TODO: Paste the feature request.",
    ).rstrip()
    return f"{start}\n{body}\n{end}"


def update_feature_block(path: Path, block: str, feature_slug: str, force: bool) -> None:
    content = path.read_text(encoding="utf-8").rstrip()
    start, end = feature_markers(feature_slug)

    if start in content:
        if not force:
            raise FileExistsError(f"{path} already contains feature {feature_slug}; pass --force to replace its block")
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
        content, count = pattern.subn(block, content, count=1)
        if count != 1:
            raise ValueError(f"Could not replace feature block in {path}")
    else:
        content = f"{content}\n\n{block}"

    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def archive_docs(project_dir: Path, feature_slug: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    archive_dir = project_dir / "Archive" / f"docs-before-{feature_slug}-{timestamp}"
    archive_dir.mkdir(parents=True, exist_ok=False)
    for filename in DOCS:
        shutil.copy2(project_dir / "docs" / filename, archive_dir / filename)
    return archive_dir


def update_feature(project_dir: Path, feature_name: str, goal: str, force: bool) -> tuple[Path, Path]:
    feature_slug = slugify(feature_name)
    docs_dir = project_dir / "docs"

    if not project_dir.exists():
        raise FileNotFoundError(f"{project_dir} does not exist; create the MVP project first")
    for filename in FEATURE_DOCS:
        if not (docs_dir / filename).exists():
            raise FileNotFoundError(f"{docs_dir / filename} does not exist; restore or create the MVP docs first")

    if not force:
        start, _ = feature_markers(feature_slug)
        for filename in FEATURE_DOCS:
            if start in (docs_dir / filename).read_text(encoding="utf-8"):
                raise FileExistsError(
                    f"{docs_dir / filename} already contains feature {feature_slug}; pass --force to replace its block"
                )

    archive_dir = archive_docs(project_dir, feature_slug)
    for filename, template in FEATURE_DOCS.items():
        block = render_feature_block(template, feature_name, feature_slug, goal)
        update_feature_block(docs_dir / filename, block, feature_slug, force)

    return docs_dir, archive_dir


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
    parser.add_argument("--feature", help="Accepted post-MVP feature name to add to the existing root docs.")
    parser.add_argument("--feature-goal", default="", help="Feature-specific goal; defaults to --goal.")
    parser.add_argument(
        "--experiment-only",
        action="store_true",
        help="Create only the experiment docs inside an existing project; do not create or update root docs.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite initial docs, or replace the marked block for an existing feature.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    dest = Path(args.dest).expanduser().resolve()
    project_dir = dest / slugify(args.name)

    if args.feature and args.experiment:
        raise ValueError("Choose either --feature or --experiment, not both")

    if args.feature:
        docs_dir, archive_dir = update_feature(
            project_dir,
            args.feature,
            args.feature_goal or args.goal,
            args.force,
        )
        print(docs_dir)
        print(archive_dir)
        return 0

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
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
