---
name: scaffold-mvp-project
description: Create or evolve an engineering project through a maintainable MVP workflow. Use when the user states a new engineering goal or wants to add an accepted feature after completing an MVP, and Codex should assume a long-lived technical route, parse the user's purpose, scaffold or inspect the project, create or update docs/ and Archive/, define the minimum workflow, and document file-structure changes before coding.
---

# Scaffold MVP Project

## Overview

Use this skill to turn a broad engineering goal into a concrete project workspace, then reuse the same planning loop for accepted features after the MVP is complete.

Core premise: plan with one long-lived, maintainable technical route that should remain valid as the project grows. Do not choose a disposable prototype route that will predictably require a full rewrite.

MVP means: after accepting that long-term technical premise, parse the user's real purpose, then implement the smallest core capability that serves that purpose. For later features, preserve the route and apply the same minimum-scope reasoning to the next useful increment. Documentation is updated before implementation.

## Workflow

1. Apply the technical-route premise.
   - Treat long-term maintainability as a requirement, not a later enhancement.
   - Prefer boring, durable, locally understandable choices over throwaway shortcuts.
   - If the user suggests a stack that conflicts with the likely future direction, document the concern in `docs/decisions.md` instead of silently following it.

2. Determine the lifecycle state.
   - For a new goal, create the project scaffold and initial docs.
   - For an accepted feature after the MVP, inspect the existing project and update the root docs in place; do not create a second project.
   - For an uncertain or disposable idea, use `experiments/<experiment-name>/` first. If the experiment is accepted, merge its outcome into the root docs before production implementation.

3. Parse the user's purpose.
   - Identify the real outcome the user wants, not only the literal feature request.
   - Name the first user or operator and their core job-to-be-done.
   - Separate the minimum core value from nice-to-have workflow, UI, automation, or deployment details.

4. Establish the project context.
   - If the user gives a path or name, preserve it.
   - If not, derive a short lowercase hyphen-case name from the goal.
   - If the destination is ambiguous, use the current workspace unless that would be unsafe or clearly surprising.
   - For a new project, prefer running `scripts/scaffold_mvp_project.py` to create the root, `docs/`, `Archive/`, and `experiments/`.
   - For a feature iteration, read the current root docs, source tree, tests, public interfaces, and relevant recent decisions before proposing changes.
   - Do not create source-code directories until the MVP plan and file structure have been written, unless the user explicitly asks for code scaffolding too.

5. Create or update the docs package.
   For a new project, create these files in `docs/`:
   - `goal.md`: user request, purpose analysis, MVP definition, assumptions, non-goals, target users or operators, and success criteria.
   - `mvp-flow.md`: the MVP process steps from setup through the first usable demo.
   - `file-structure.md`: proposed project file tree with one-line responsibility notes for each important path.
   - `decisions.md`: long-term maintainable technical route, initial choices, open questions, and constraints.
   - `Archive/`: a project-level archive for superseded plans, old notes, replaced artifacts, or retained context that should not clutter active docs.
   - `experiments/`: reserved workspace for future experimental features.
   For an accepted post-MVP feature:
   - Archive a snapshot of the current four docs under `Archive/` before replacing important planning context.
   - Update `goal.md` with the feature request, purpose, minimum scope, non-goals, and success criteria.
   - Update `mvp-flow.md` with the smallest feature milestones plus feature and regression verification.
   - Update `file-structure.md` with the current tree and exact new or changed paths; remove stale proposed paths.
   - Update `decisions.md` with route fit, implementation choice, compatibility or migration impact, constraints, and open questions.
   - Keep the root docs as the current source of truth. Do not leave the feature only in an archive, experiment folder, chat response, or appended TODO block.

6. Keep the MVP scope practical.
   - Prefer the smallest core workflow that demonstrates the core value.
   - Keep the selected technical route aligned with the future product, even when the first delivered slice is tiny.
   - Separate required MVP work from later enhancements.
   - Include verification steps for each major milestone.
   - Avoid over-designing infrastructure, abstractions, or optional services before the core loop is clear.

7. Report the result.
   - Link the project folder and created or updated docs files.
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

For an accepted feature after the MVP, update the existing root docs:

```bash
python scripts/scaffold_mvp_project.py --name my-project --dest . --feature saved-searches --feature-goal "Let users rerun a saved search"
```

This first archives the current docs under `Archive/docs-before-<feature>-<timestamp>/`, then adds marked feature-planning blocks to all four root docs. Replace every TODO and reconcile the main goal, workflow, tree, and decisions so the root docs describe the current project rather than merely preserving a change log. Use `--force` only to replace the marked blocks for that same feature.

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

Validate a specific accepted feature after completing its docs:

```bash
python scripts/validate_mvp_docs.py ./my-project --feature saved-searches
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
- Update the four root docs before implementing an accepted post-MVP feature, then reconcile them again after implementation if the actual structure or decision differs.
- Keep uncertain ideas in `experiments/`; use feature mode only after the capability is accepted into the product direction.
- If the user asked for planning only, stop after docs and do not implement code.
- If the user asked to build the project, pause after docs only long enough to summarize the scaffold, then continue into implementation.
- Keep file trees realistic for the likely stack, but mark framework choices as assumptions when the user has not specified them.
