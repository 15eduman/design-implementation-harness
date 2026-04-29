#!/usr/bin/env python3
"""Validate a design QA report against the lightweight harness rules.

This script intentionally uses only Python's standard library so it can run in
small agent environments without dependency installation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_TOP_LEVEL = {
    "source",
    "candidate",
    "overallScore",
    "categoryScores",
    "issues",
    "verdict",
}

VALID_VERDICTS = {
    "pass",
    "pass_with_minor_repairs",
    "needs_repair",
    "rebuild_from_source",
}

VALID_SEVERITIES = {"critical", "major", "minor"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_score(name: str, value: object, allow_null: bool = False) -> None:
    if value is None and allow_null:
        return
    if not isinstance(value, (int, float)):
        fail(f"{name} must be a number")
    if not 0 <= value <= 100:
        fail(f"{name} must be between 0 and 100")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--allow-draft", action="store_true")
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "design-harness.config.json",
        help="Harness config used for strict category validation.",
    )
    parser.add_argument("--strict-categories", action="store_true")
    parser.add_argument("--enforce-thresholds", action="store_true")
    args = parser.parse_args()

    data = json.loads(args.report.read_text(encoding="utf-8"))

    missing = REQUIRED_TOP_LEVEL - set(data)
    if missing:
        fail(f"missing required fields: {', '.join(sorted(missing))}")

    if data["verdict"] not in VALID_VERDICTS:
        fail(f"invalid verdict: {data['verdict']}")

    validate_score("overallScore", data["overallScore"])

    if not isinstance(data["categoryScores"], dict):
        fail("categoryScores must be an object")

    if args.strict_categories:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        expected = set(config.get("qaCategories", []))
        actual = set(data["categoryScores"])
        missing_categories = expected - actual
        extra_categories = actual - expected
        if missing_categories:
            fail(f"missing category scores: {', '.join(sorted(missing_categories))}")
        if extra_categories:
            fail(f"unknown category scores: {', '.join(sorted(extra_categories))}")

    for name, score in data["categoryScores"].items():
        validate_score(f"categoryScores.{name}", score, allow_null=args.allow_draft)

    if args.enforce_thresholds:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        thresholds = config.get("thresholds", {})
        overall_pass = thresholds.get("overallPassScore")
        category_minimum = thresholds.get("criticalCategoryMinimum")

        if overall_pass is not None and data["overallScore"] < overall_pass:
            fail(f"overallScore {data['overallScore']} is below threshold {overall_pass}")

        if category_minimum is not None:
            for name, score in data["categoryScores"].items():
                if score is None and args.allow_draft:
                    continue
                if score < category_minimum:
                    fail(f"categoryScores.{name} {score} is below threshold {category_minimum}")

    if not isinstance(data["issues"], list):
        fail("issues must be an array")
    for index, issue in enumerate(data["issues"]):
        for field in ["category", "severity", "observed", "expected", "repair"]:
            if field not in issue:
                fail(f"issues[{index}] missing {field}")
        if issue["severity"] not in VALID_SEVERITIES:
            fail(f"issues[{index}] has invalid severity {issue['severity']}")

    print(f"OK: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
