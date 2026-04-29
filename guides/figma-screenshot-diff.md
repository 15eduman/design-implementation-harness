# Figma Screenshot Diff Guide

This guide describes a reusable way to connect Figma screenshot exports to
`score_visual_diff.py` for any product, service, or design system.

The goal is not to reduce design quality to one pixel score. The goal is to
give agents a stable visual signal that can trigger better QA and targeted
repair.

## When To Use

Use this flow when you have:

- a source Figma node,
- a candidate Figma node, app screen, or rendered webpage,
- a need to detect visual drift after implementation or composition.

Typical workflows:

- Figma source screen vs. React implementation screenshot.
- Figma source component vs. newly componentized Figma component.
- Figma source template vs. agent-composed Figma candidate.
- Old design system component vs. new migrated component.

## Mental Model

```txt
source node
  -> source screenshot

candidate node or app route
  -> candidate screenshot

source screenshot + candidate screenshot
  -> score_visual_diff.py
  -> rough visual signal
  -> Visual QA Agent
  -> repair instructions
```

The image diff is a signal. The Visual QA Agent still decides what the
difference means.

## Required Inputs

At minimum:

```txt
source.png
candidate.png
```

Recommended metadata:

```json
{
  "source": {
    "kind": "figma",
    "fileKey": "FIGMA_FILE_KEY",
    "nodeId": "SOURCE_NODE_ID",
    "name": "Source frame name"
  },
  "candidate": {
    "kind": "figma|web|native|image",
    "nodeId": "CANDIDATE_NODE_ID",
    "route": "http://localhost:3000/example",
    "name": "Candidate name"
  },
  "capture": {
    "viewport": { "width": 390, "height": 844 },
    "scale": 1,
    "background": "transparent|solid",
    "fullPage": false
  }
}
```

## Capture Rules

To make screenshot diff useful, source and candidate captures must be as
similar as possible.

### 1. Same Boundary

Compare equivalent boundaries:

- full screen to full screen,
- component to component,
- module to module,
- viewport crop to viewport crop.

Do not compare a full phone screen against only the content area.

### 2. Same Pixel Size

Prefer exact same image dimensions. If they differ, `score_visual_diff.py`
compares the shared top-left region only. That is useful for rough signals but
not ideal for pass/fail decisions.

### 3. Same Scale

Use a stable export scale, usually `1x` or `2x`.

For Figma-to-web QA, use:

```txt
Figma export scale: 1x
Browser device scale factor: 1
Viewport width/height: source frame width/expected QA viewport
```

### 4. Same State

Freeze dynamic UI before capture:

- time,
- loading states,
- carousel position,
- remote images,
- animation frame,
- hover/focus states,
- scroll position.

If dynamic content is intentional, document it in the QA report before scoring.

### 5. Same Background

A transparent Figma export compared to a solid web background can create noisy
diffs. Prefer source and candidate screenshots with the same background.

## Recommended Folder Layout

Use a neutral layout that can work for any service:

```txt
design-harness/
  captures/
    source/
      home.source.png
      card.source.png
    candidate/
      home.candidate.png
      card.candidate.png
    diff/
      home.diff.json
      card.diff.json
  reports/
    qa-report.draft.json
```

`captures/` is usually generated output. Commit examples only if useful for
documentation; otherwise ignore large screenshot sets in product repos.

## Figma Source Capture

When using Figma MCP, capture the source screenshot with `get_screenshot`:

```txt
fileKey: FIGMA_FILE_KEY
nodeId: SOURCE_NODE_ID
contentsOnly: false
```

Save the returned image as:

```txt
  captures/source/<case>.source.png
```

For component-level comparison, capture the component or module node directly,
not the whole page.

## Candidate Capture

Candidate capture depends on where the candidate lives.

### Candidate Is In Figma

Use `get_screenshot` for the candidate node:

```txt
fileKey: FIGMA_FILE_KEY
nodeId: CANDIDATE_NODE_ID
contentsOnly: false
```

Save as:

```txt
  captures/candidate/<case>.candidate.png
```

### Candidate Is A Web App

Use a browser automation tool to capture a stable viewport:

```txt
viewport: same width as source frame
deviceScaleFactor: 1
animations: disabled if possible
fullPage: false unless source is full-page
```

Save as:

```txt
  captures/candidate/<case>.candidate.png
```

### Candidate Is A Native App

Use a simulator or device screenshot with a known device size. If the source
Figma frame excludes OS chrome, crop the native screenshot to the same app
boundary before diffing.

## Running The Diff

```bash
python3 scripts/score_visual_diff.py \
  captures/source/home.source.png \
  captures/candidate/home.candidate.png \
  --out captures/diff/home.diff.json
```

Output example:

```json
{
  "comparedSize": { "width": 360, "height": 844 },
  "rms": 18.24,
  "similarityScore": 92.85,
  "changedAreaRatio": 0.1842
}
```

## How To Interpret Scores

Use the score as a triage signal, not a final design verdict.

| Similarity | Meaning | Suggested action |
| ---: | --- | --- |
| 97-100 | Very close or identical | Run category QA for subtle issues |
| 92-96 | Likely acceptable with small differences | Inspect typography, icons, and image crop |
| 85-91 | Visible drift | Run Visual QA Agent and repair |
| 70-84 | Major structural or asset mismatch | Replace weak modules with source-backed components |
| below 70 | Not comparable or wrong target | Re-capture or rebuild from source |

`changedAreaRatio` helps distinguish small global shifts from localized issues:

- low changed area + low similarity can indicate a severe localized mismatch,
- high changed area + good similarity can indicate subtle anti-aliasing or font
  differences across a large area,
- high changed area + low similarity usually means layout drift.

## Common False Positives

Image diff can overreact to:

- missing fonts,
- text anti-aliasing differences,
- device pixel ratio mismatch,
- remote image compression,
- transparent vs. solid background,
- time/status bar changes,
- small scroll offset changes.

For these cases, annotate the QA report and let the Visual QA Agent focus on
category-level issues.

## Common False Negatives

Image diff can miss design-quality problems when:

- the compared area is too large and a bad component is visually diluted,
- screenshots are downscaled,
- the wrong crop hides the failing module,
- source and candidate both contain the same placeholder.

Use module-level screenshots for important components.

## Multi-Level QA Strategy

Run diff at three levels:

```txt
1. full screen
2. viewport slices
3. critical components/modules
```

Example:

```txt
home-full
home-top-viewport
home-product-viewport
data-usage-card
product-card
bottom-agent-input
```

Full-screen diff catches global rhythm. Component diff catches local quality.

## Agent Integration Pattern

The Visual QA Agent should receive:

```json
{
  "sourceScreenshot": "captures/source/home.source.png",
  "candidateScreenshot": "captures/candidate/home.candidate.png",
  "diffReport": "captures/diff/home.diff.json",
  "moduleSpec": "docs/HOME_MODULE_SPEC.md",
  "qaChecklist": "docs/DESIGN_QA_CHECKLIST.md"
}
```

The agent should produce:

```json
{
  "overallScore": 88,
  "categoryScores": {
    "frameRhythm": 94,
    "cardGeometry": 90,
    "imageSlotFidelity": 72
  },
  "issues": [
    {
      "category": "imageSlotFidelity",
      "severity": "major",
      "observed": "Product image fills the card media slot as cover.",
      "expected": "Product object should sit inside the source safe area.",
      "repair": "Replace the product tile with a source-backed component instance."
    }
  ]
}
```

## CI Integration

For product repos, use diff as a non-blocking check first:

```txt
PR opened
  -> build story or route
  -> capture candidate screenshot
  -> fetch or use committed source screenshot
  -> run score_visual_diff.py
  -> upload diff JSON
  -> comment QA summary
```

Only make it blocking after the team has tuned thresholds for the design
system.

Suggested gates:

```json
{
  "warningThreshold": 92,
  "failureThreshold": 85,
  "criticalComponentFailureThreshold": 80
}
```

## Service-Neutral Config

Avoid service-specific names in the harness core. Keep service-specific details
in cases:

```json
{
  "cases": [
    {
      "id": "home-top-viewport",
      "source": {
        "kind": "figma",
        "fileKey": "FIGMA_FILE_KEY",
        "nodeId": "SOURCE_NODE_ID"
      },
      "candidate": {
        "kind": "web",
        "url": "http://localhost:3000",
        "selector": "[data-testid='home-screen']"
      },
      "capture": {
        "viewport": { "width": 360, "height": 844 },
        "scale": 1
      },
      "thresholds": {
        "warning": 92,
        "failure": 85
      }
    }
  ]
}
```

This keeps the same harness usable for commerce, finance, healthcare, SaaS,
internal tools, games, consumer products, or any other product UI.

## Practical Rule

If a candidate scores poorly, do not immediately tune individual pixels.

Ask first:

```txt
Did the agent redraw a source component that should have been reused?
```

If yes, replace it with the source-backed component. Pixel tuning comes after
source reuse is correct.
