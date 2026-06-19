# Scaffold MVP Project

Codex skill for turning a broad engineering goal into a concrete project folder with a lightweight MVP planning package.

When this skill is used, Codex should first scaffold the project workspace, create `docs/`, write the core MVP planning files, and document the proposed file structure before implementation begins.

## Contents

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
└── scripts/
    ├── scaffold_mvp_project.py
    └── validate_mvp_docs.py
```

## What It Creates

For a new project:

```text
my-project/
├── docs/
│   ├── goal.md
│   ├── mvp-flow.md
│   ├── file-structure.md
│   └── decisions.md
└── experiments/
```

For an experimental feature:

```text
my-project/
└── experiments/
    └── faster-import/
        └── docs/
            ├── goal.md
            ├── mvp-flow.md
            ├── file-structure.md
            └── decisions.md
```

Each experiment is treated as its own mini MVP before it is merged into the main project plan.

## Script Usage

Create a project scaffold:

```bash
python scripts/scaffold_mvp_project.py \
  --name my-project \
  --goal "Build a local search tool" \
  --dest .
```

Add an experimental feature scaffold:

```bash
python scripts/scaffold_mvp_project.py \
  --name my-project \
  --dest . \
  --experiment faster-import \
  --experiment-goal "Try a faster import flow" \
  --experiment-only
```

Validate the project docs:

```bash
python scripts/validate_mvp_docs.py ./my-project
```

Validate the project docs and all experiment docs:

```bash
python scripts/validate_mvp_docs.py ./my-project --experiments
```

## Installing As A Codex Skill

Clone this repository into your Codex skills directory:

```bash
git clone https://github.com/silent1ball-gg/scaffold-mvp-project.git \
  ~/.codex/skills/scaffold-mvp-project
```

Then invoke it with:

```text
Use $scaffold-mvp-project to turn this engineering goal into a project folder, docs, MVP steps, and file structure.
```
