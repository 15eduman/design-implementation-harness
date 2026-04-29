# Design Implementation Harness

Use this repository as a source-fidelity design implementation harness.

## Default Workflow

1. Read `design-harness.config.json`.
2. Pick an agent role from `agents.yaml`.
3. Load the matching prompt from `prompts/`.
4. Prefer source-backed components or source nodes over redrawing.
5. Capture source and candidate screenshots before visual QA.
6. Produce or validate a QA report with `scripts/validate_qa_report.py`.
7. Repair only failed QA categories.

## Important Rules

- Do not redraw source modules when source nodes or components exist.
- Do not replace source icons, masks, gradients, or image crops with approximations.
- Do not apply generic layout defaults over source geometry.
- Use screenshot diff as a signal, not the final design verdict.

## Useful Commands

```bash
python3 scripts/create_qa_report.py
python3 scripts/validate_qa_report.py --allow-draft --strict-categories reports/qa-report.draft.json
python3 scripts/validate_qa_report.py --strict-categories --enforce-thresholds reports/qa-report.json
python3 scripts/build_agent_packet.py visual_qa
python3 scripts/score_visual_diff.py source.png candidate.png
python3 -m unittest discover -s tests
```
