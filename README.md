# Design Implementation Harness

A service-neutral harness for helping LLM agents implement, componentize, and
QA-review UI designs without losing the quality of the original source design.

한국어 문서는 [README.ko.md](README.ko.md)를 참고하세요.

It is built for Figma-to-app, Figma-to-Figma, and design-system migration
workflows where visual fidelity depends on details like spacing, image slots,
icon instances, masks, gradients, row rhythm, component reuse, and screenshot
QA.

## Why This Exists

LLMs can often recreate the broad structure of a UI, but high-quality product
design usually lives in small, source-specific decisions:

- exact gutters and card widths,
- icon slots vs. visual icon size,
- image crop safe areas,
- progress masks and gradients,
- fixed row heights,
- CTA baseline alignment,
- component density,
- source asset reuse.

When an agent starts from a generic style guide or a text-only prompt, these
details are easy to flatten into defaults. The result may be structurally
correct but visually weaker.

This harness gives agents a stricter workflow:

```txt
source design
  -> module inventory
  -> source-backed components
  -> candidate composition
  -> screenshot diff
  -> structured visual QA
  -> targeted repair
```

The goal is not to automate taste. The goal is to make design quality harder to
accidentally lose.

## Who This Is For

### Designers And Design System Owners

Use this when a high-quality Figma source keeps degrading during implementation
or screen expansion. The harness turns visual concerns into reusable component
rules and QA criteria.

### Frontend Engineers

Use this when design review feedback keeps coming back as "close, but not quite."
It helps separate measurable issues like gutter, card radius, image crop, and
CTA alignment from subjective taste.

### AI Agent Builders

Use this to split UI work into specialized agents:

```txt
Componentizer -> Composer -> Visual QA -> Repair
```

This is more reliable than asking one agent to design, implement, judge, and fix
everything in a single pass.

### Product Teams And QA

Use this when design fidelity should be part of release quality. It can produce
structured QA reports that are easier to discuss in PRs, QA reviews, or design
sign-off.

### Agencies And External Delivery Teams

Use this when a client provides Figma and expects faithful implementation. The
harness gives both sides clearer review language than "make it more like the
design."

## Best Fit

This harness works best when:

- there is a polished source design,
- fidelity matters,
- the UI is modular or component-based,
- multiple people or agents need to reproduce the same visual system,
- screenshots can be captured for source and candidate states.

It is useful for commerce, finance, SaaS, healthcare, internal tools,
education, native apps, consumer products, and design-system migrations. The
core is not tied to one brand, service, or product category.

## Poor Fit

This harness is less useful when:

- the design is still a loose wireframe,
- the goal is broad visual exploration,
- speed matters more than fidelity,
- every screen is intentionally unique,
- no stable source screenshot or component system exists.

## Core Principle

When a source design exists, agents should not begin by redrawing. They should
begin by identifying and reusing the source system.

Source priority:

1. Source Figma component or node.
2. Source screenshot.
3. Module spec.
4. QA checklist.
5. General design guide.
6. Agent judgment.

## Directory

```txt
design-harness/
  README.md
  README.ko.md
  design-harness.config.json
  agents.yaml
  prompts/
    agent-system.md
    componentizer.md
    composer.md
    visual-qa.md
    repair.md
  checklists/
    visual-fidelity.md
  schemas/
    qa-report.schema.json
    module-inventory.schema.json
  scripts/
    create_qa_report.py
    validate_qa_report.py
    build_agent_packet.py
    score_visual_diff.py
    create-qa-report.mjs
  guides/
    figma-screenshot-diff.md
  reports/
    sample-qa-report.md
```

## Quick Start

1. Update `design-harness.config.json`.

Set your own source design:

```json
{
  "source": {
    "figmaFileKey": "YOUR_FIGMA_FILE_KEY",
    "sourceNodeId": "SOURCE_NODE_ID",
    "sourceFrameName": "Source screen name",
    "sourceFrameSize": {
      "width": 390,
      "height": 844
    }
  }
}
```

2. Add module inventory.

```json
{
  "name": "ProductCard",
  "sourceNodeId": "123:456",
  "targetComponentName": "Commerce/ProductCard",
  "critical": true
}
```

3. Create a QA report draft.

```bash
python3 design-harness/scripts/create_qa_report.py
```

4. Validate the report shape.

```bash
python3 design-harness/scripts/validate_qa_report.py \
  --allow-draft \
  design-harness/reports/qa-report.draft.json
```

5. Build an agent prompt packet.

```bash
python3 design-harness/scripts/build_agent_packet.py visual_qa
```

6. Run screenshot diff when you have source and candidate images.

```bash
python3 design-harness/scripts/score_visual_diff.py \
  design-harness/captures/source/home.source.png \
  design-harness/captures/candidate/home.candidate.png \
  --out design-harness/captures/diff/home.diff.json
```

`score_visual_diff.py` requires Pillow:

```bash
python3 -m pip install pillow
```

## Agent Roles

Agent roles are described in `agents.yaml`.

### Source Reader

Reads Figma source metadata, screenshots, and module candidates. It should not
redraw or infer source geometry without metadata.

### Componentizer

Converts source modules into reusable components. It preserves source geometry,
masks, gradients, image slots, and icon instances.

Prompt: `prompts/componentizer.md`

### Composer

Builds candidate screens from source-backed component instances. It changes
content, order, image overrides, and allowed properties.

Prompt: `prompts/composer.md`

### Visual QA

Reviews source and candidate screenshots with a structured rubric. It produces
a report matching `schemas/qa-report.schema.json`.

Prompt: `prompts/visual-qa.md`

### Repair

Fixes only failed QA categories. It prefers replacing weak reconstructions with
source-backed components over tuning many pixels by hand.

Prompt: `prompts/repair.md`

## What This Harness Catches

- Generic mobile gutters replacing source gutters.
- Card radius drifting to default values.
- Image slots resizing with content.
- Product images losing safe crop.
- AI/helper rows becoming ordinary subtitles.
- Icons being replaced with approximate placeholders.
- Progress masks and gradients being flattened.
- Components being redrawn instead of reused.
- Candidate screenshots passing broad structure while losing local density.

## Screenshot Diff

The screenshot diff script is intentionally simple. It compares two images and
returns rough visual metrics:

- `similarityScore`
- `rms`
- `changedAreaRatio`
- compared dimensions

The score is a triage signal, not a final design verdict. A Visual QA Agent
should use the score alongside the module spec and checklist.

For a reusable capture and diff workflow, see:

- `guides/figma-screenshot-diff.md`

## QA Report

Reports should match `schemas/qa-report.schema.json`.

Each issue should include:

- category,
- severity,
- observed difference,
- expected source behavior,
- likely cause,
- repair instruction.

Example categories:

- `frameRhythm`
- `cardGeometry`
- `internalAlignment`
- `imageSlotFidelity`
- `typographyHierarchy`
- `aiLineGrammar`
- `dataResilience`
- `sourceComponentReuse`

## Codex Skill

A draft skill is included at:

```txt
skill/design-implementation-harness/SKILL.md
```

Use it as a starting point if you want Codex or another agent runtime to load
this workflow automatically for design implementation tasks.

## How To Generalize To Another Product

Replace service-specific values in `design-harness.config.json`:

- `figmaFileKey`
- `sourceNodeId`
- `sourceFrameName`
- `moduleInventory`
- `captureCases`
- linked specs/checklists

Keep the core harness neutral. Put product-specific details in config, module
inventory, source screenshots, and optional design docs.

## Practical Rule

If a candidate looks weak, ask this first:

```txt
Did the agent redraw a source component that should have been reused?
```

If yes, replace it with the source-backed component before tuning pixels.

## Limitations

- This does not replace a real design system.
- This does not guarantee good new visual direction without source examples.
- Image diff can overreact to fonts, anti-aliasing, scale, or dynamic content.
- Screenshot scores should be paired with structured visual QA.
