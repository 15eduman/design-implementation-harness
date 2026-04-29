# Sample QA Report

## Verdict

`needs_repair`

## Overall Score

`74 / 100`

## Category Scores

| Category | Score | Notes |
| --- | ---: | --- |
| frameRhythm | 90 | Frame width and gutter are correct. |
| cardGeometry | 82 | Main radius is correct, but one module height drifted. |
| internalAlignment | 70 | AI CTA row baseline differs from source. |
| imageSlotFidelity | 58 | Product image uses cover crop instead of source safe area. |
| typographyHierarchy | 80 | Font differs but hierarchy mostly holds. |
| aiLineGrammar | 72 | AI copy wraps in compact card. |
| dataResilience | 78 | Long Korean title changes card rhythm. |
| sourceComponentReuse | 62 | Two cards appear redrawn instead of instance-based. |

## Issues

1. Major: Product image crop is too large.
   - Expected: source product safe area within 100 x 100 media frame.
   - Repair: replace redrawn product card with source-backed `Home/ProductCard`.

2. Major: AI CTA wraps below message.
   - Expected: message and `AI 대화하기` stay in one row.
   - Repair: restore source AI row width and CTA x-position.

3. Minor: Card body feels loose.
   - Expected: fixed source module height and 20px card padding.
   - Repair: use source component instance instead of content-driven height.

