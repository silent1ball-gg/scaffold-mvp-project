---
name: scaffold-mvp-project
description: Create a new engineering project folder and lightweight docs package before implementation. Use when the user states an engineering goal, product idea, app/tool request, or build objective and wants Codex to first assume a long-lived maintainable technical route, parse the user's purpose, scaffold the project, create docs/ and Archive/ directories, define MVP workflow steps, and document the initial project file structure before coding.
---

# Scaffold MVP Project

## Overview

Use this skill to turn a broad engineering goal into a concrete project workspace before implementation.

Core premise: plan with one long-lived, maintainable technical route that should remain valid as the project grows. Do not choose a disposable prototype route that will predictably require a full rewrite.

MVP means: after accepting that long-term technical premise, parse the user's real purpose, then implement the smallest core capability that serves that purpose. The first deliverable is the project folder and its planning structure, not production code.

## Workflow

1. Apply the technical-route premise.
   - Treat long-term maintainability as a requirement, not a later enhancement.
   - Prefer boring, durable, locally understandable choices over throwaway shortcuts.
   - If the user suggests a stack that conflicts with the likely future direction, document the concern in `docs/decisions.md` instead of silently following it.

2. Parse the user's purpose.
   - Identify the real outcome the user wants, not only the literal feature request.
   - Name the first user or operator and their core job-to-be-done.
   - Separate the minimum core value from nice-to-have workflow, UI, automation, or deployment details.

3. Determine the project folder name.
   - If the user gives a path or name, preserve it.
   - If not, derive a short lowercase hyphen-case name from the goal.
   - If the destination is ambiguous, use the current workspace unless that would be unsafe or clearly surprising.

4. Create the project folder first.
   - Prefer running `scripts/scaffold_mvp_project.py` to create the root project directory, `docs/` skeleton, `Archive/`, and default `experiments/` directory.
   - Do not create source-code directories until the MVP plan and file structure have been written, unless the user explicitly asks for code scaffolding too.

5. Write the docs package.
   Create these files in `docs/`:
   - `goal.md`: user request, purpose analysis, MVP definition, assumptions, non-goals, target users or operators, and success criteria.
   - `mvp-flow.md`: the MVP process steps from setup through the first usable demo.
   - `file-structure.md`: proposed project file tree with one-line responsibility notes for each important path.
   - `decisions.md`: long-term maintainable technical route, initial choices, open questions, and constraints.
   - `Archive/`: a project-level archive for superseded plans, old notes, replaced artifacts, or retained context that should not clutter active docs.
   - `experiments/`: reserved workspace for future experimental features.

6. Keep the MVP scope practical.
   - Prefer the smallest core workflow that demonstrates the core value.
   - Keep the selected technical route aligned with the future product, even when the first delivered slice is tiny.
   - Separate required MVP work from later enhancements.
   - Include verification steps for each major milestone.
   - Avoid over-designing infrastructure, abstractions, or optional services before the core loop is clear.

7. Report the result.
   - Link the created project folder and docs files.
   - Summarize the parsed user purpose.
   - Summarize the long-term maintainable technical-route assumption.
   - Summarize the MVP steps and the proposed file structure.
   - Call out assumptions and any decisions that need user confirmation.

## Scripts

Use `scripts/scaffold_mvp_project.py` for repeatable folder and docs creation:

```bash
python scripts/scaffold_mvp_project.py --name my-project --goal "Build a local search tool" --dest .
```

The script creates the project folder, `docs/`, `Archive/`, `experiments/`, and the four required docs files with stable section templates. After running it, replace TODOs with goal-specific planning and adjust `file-structure.md` to match the likely implementation stack.

For an experimental feature, scaffold it as a nested mini-project under `experiments/`:

```bash
python scripts/scaffold_mvp_project.py --name my-project --dest . --experiment new-feature --experiment-goal "Try a faster import flow" --experiment-only
```

This creates `my-project/experiments/new-feature/docs/` and `my-project/experiments/new-feature/Archive/` with the same four docs: `goal.md`, `mvp-flow.md`, `file-structure.md`, and `decisions.md`. Treat each experiment as an isolated MVP with its own goal, steps, and file structure before merging it into the main project plan.

Use `scripts/validate_mvp_docs.py` before reporting completion:

```bash
python scripts/validate_mvp_docs.py ./my-project
```

The validation script checks that the required docs, headings, `Archive/`, and top-level `experiments/` directory exist. Add `--experiments` to validate every experiment folder too:

```bash
python scripts/validate_mvp_docs.py ./my-project --experiments
```

## Document Templates

Use the user's language when writing docs.

For `goal.md`, include:

```markdown
# Goal

## User Request

## Purpose Analysis

## MVP Definition

## Assumptions

## Non-Goals

## Target User

## Success Criteria
```

For `mvp-flow.md`, include:

```markdown
# MVP Flow

## Milestone 1: Project Foundation

## Milestone 2: Core Data or Domain Model

## Milestone 3: Main User Workflow

## Milestone 4: Verification and Demo

## Later
```

For `file-structure.md`, include:

```markdown
# File Structure

## Proposed Tree

## Path Responsibilities
```

Default project tree:

```text
<project-name>/
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

For `decisions.md`, include:

```markdown
# Decisions

## Long-Term Maintainable Technical Route

## Initial Choices

## Open Questions

## Constraints
```

## Implementation Guardrails

- Use the scaffolding script for directory and template creation when possible; use `mkdir -p` or equivalent only when the script is not appropriate.
- Use existing repo conventions if the folder is being created inside an existing repository.
- If the user asked for planning only, stop after docs and do not implement code.
- If the user asked to build the project, pause after docs only long enough to summarize the scaffold, then continue into implementation.
- Keep file trees realistic for the likely stack, but mark framework choices as assumptions when the user has not specified them.
