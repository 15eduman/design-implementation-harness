---
name: design-implementation-harness
description: Use when implementing, componentizing, or QA-reviewing Figma-based UI designs where visual fidelity matters. Guides agents to reuse source components, run screenshot QA, produce structured reports, and repair design drift.
---

# Design Implementation Harness

Use this skill for Figma-to-code, Figma-to-Figma, or source-design-to-component
work where the goal is preserving original design quality.

## Workflow

1. Read `design-harness/design-harness.config.json`.
2. Load the relevant prompt from `design-harness/prompts/`.
3. Use source Figma nodes or source-backed components before drawing anything.
4. Compose candidates from instances or source-derived modules.
5. Capture source and candidate screenshots.
6. Produce a QA report matching `design-harness/schemas/qa-report.schema.json`.
7. Repair only failed QA categories.

## Rules

- Do not redraw modules when a source node/component exists.
- Do not replace icons, masks, gradients, or image crops with approximations.
- Do not apply generic mobile defaults over source measurements.
- Prefer replacing weak reconstructions with source-backed components.

## Scripts

- Create a QA draft:
  `python3 design-harness/scripts/create_qa_report.py` if present, or
  `node design-harness/scripts/create-qa-report.mjs`.
- Validate a QA report:
  `python3 design-harness/scripts/validate_qa_report.py --allow-draft design-harness/reports/qa-report.draft.json`.
- Build an agent packet:
  `python3 design-harness/scripts/build_agent_packet.py visual_qa`.
- Score screenshots when Pillow is installed:
  `python3 design-harness/scripts/score_visual_diff.py source.png candidate.png`.

## Agent Roles

Use `design-harness/agents.yaml` to choose the role:

- `componentizer`: source modules to reusable components.
- `composer`: component instances to candidate screen.
- `visual_qa`: screenshot and metadata review.
- `repair`: targeted fixes from QA report.

