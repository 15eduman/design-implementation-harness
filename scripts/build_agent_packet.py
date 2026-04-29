#!/usr/bin/env python3
"""Build a compact prompt packet for a specific design agent role."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


ROLE_PROMPTS = {
    "system": ROOT / "prompts" / "agent-system.md",
    "source_reader": ROOT / "prompts" / "source-reader.md",
    "componentizer": ROOT / "prompts" / "componentizer.md",
    "composer": ROOT / "prompts" / "composer.md",
    "visual_qa": ROOT / "prompts" / "visual-qa.md",
    "repair": ROOT / "prompts" / "repair.md",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("role", choices=sorted(ROLE_PROMPTS))
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    config = json.loads((ROOT / "design-harness.config.json").read_text(encoding="utf-8"))
    system_prompt = ROLE_PROMPTS["system"].read_text(encoding="utf-8")
    role_prompt = ROLE_PROMPTS[args.role].read_text(encoding="utf-8")
    prompt = system_prompt if args.role == "system" else f"{system_prompt}\n\n---\n\n{role_prompt}"

    packet = {
        "role": args.role,
        "source": config["source"],
        "documents": config["documents"],
        "thresholds": config["thresholds"],
        "sourceRules": config["sourceRules"],
        "moduleInventory": config["moduleInventory"],
        "prompt": prompt,
    }

    text = json.dumps(packet, indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
