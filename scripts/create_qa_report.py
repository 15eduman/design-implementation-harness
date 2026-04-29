#!/usr/bin/env python3
"""Create a draft design QA report from harness config."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "out",
        nargs="?",
        type=Path,
        default=ROOT / "reports" / "qa-report.draft.json",
    )
    args = parser.parse_args()

    config = json.loads((ROOT / "design-harness.config.json").read_text(encoding="utf-8"))
    report = {
        "source": {
            "figmaFileKey": config["source"]["figmaFileKey"],
            "nodeId": config["source"]["sourceNodeId"],
            "screenshotPath": "",
        },
        "candidate": {
            "nodeId": "",
            "screenshotPath": "",
            "implementationPath": "",
        },
        "overallScore": 0,
        "categoryScores": {category: None for category in config["qaCategories"]},
        "issues": [],
        "verdict": "needs_repair",
        "nextStep": "Fill screenshots, run Visual QA Agent, then update scores and issues.",
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Created QA report draft: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

