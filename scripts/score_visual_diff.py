#!/usr/bin/env python3
"""Score two screenshots with simple visual-diff metrics.

The script uses Pillow when available. If Pillow is not installed, it exits with
a clear message instead of pretending to score the images.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


def load_pillow():
    try:
        from PIL import Image, ImageChops, ImageStat
    except Exception as exc:  # pragma: no cover - depends on environment
        print(
            "ERROR: Pillow is required for screenshot diffing. "
            "Install with `python3 -m pip install pillow` or run metadata-only QA.",
            file=sys.stderr,
        )
        raise SystemExit(2) from exc
    return Image, ImageChops, ImageStat


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    Image, ImageChops, ImageStat = load_pillow()

    source = Image.open(args.source).convert("RGBA")
    candidate = Image.open(args.candidate).convert("RGBA")

    width = min(source.width, candidate.width)
    height = min(source.height, candidate.height)
    source_crop = source.crop((0, 0, width, height))
    candidate_crop = candidate.crop((0, 0, width, height))

    diff = ImageChops.difference(source_crop, candidate_crop)
    stat = ImageStat.Stat(diff)
    rms = math.sqrt(sum(value * value for value in stat.rms) / len(stat.rms))
    normalized = min(100, (rms / 255) * 100)
    similarity = max(0, 100 - normalized)

    bbox = diff.getbbox()
    changed_area = 0
    if bbox:
        changed_area = ((bbox[2] - bbox[0]) * (bbox[3] - bbox[1])) / (width * height)

    result = {
        "source": str(args.source),
        "candidate": str(args.candidate),
        "comparedSize": {"width": width, "height": height},
        "rms": round(rms, 4),
        "similarityScore": round(similarity, 2),
        "changedAreaRatio": round(changed_area, 4),
        "sourceSize": {"width": source.width, "height": source.height},
        "candidateSize": {"width": candidate.width, "height": candidate.height},
        "notes": [
            "This score is a rough signal, not a design-quality verdict.",
            "Use the Visual QA Agent for category-level diagnosis."
        ]
    }

    payload = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

