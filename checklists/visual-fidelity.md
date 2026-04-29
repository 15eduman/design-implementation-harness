# Visual Fidelity Checklist

Use this checklist before accepting a candidate screen.

## Critical Pass Items

- The candidate uses source-backed components or source-derived nodes.
- Frame width matches the source reference.
- Main gutter matches the source reference.
- Feed module width matches the source reference.
- Module gap matches the source reference.
- Card radius matches the source reference.
- Icon slots and visual icon sizes match the source reference.
- Image slots preserve object inspection and safe crops.
- Masks and gradients are preserved.
- AI CTA rows keep source grammar and alignment.

## Failure Signals

- The candidate looks like a wireframe with correct text.
- Product images are cropped or scaled as generic covers.
- Icons are approximate or visually heavier than source.
- Cards feel taller, looser, or more spacious than source.
- AI copy behaves like a normal subtitle.
- Repeated modules have inconsistent x positions.
- Bottom navigation or agent prompt floats differently from source.

## Repair Bias

Prefer replacing a weak reconstruction with a source-backed component over
tuning many small values by hand.

