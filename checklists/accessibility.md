# Accessibility Checklist

Use this alongside visual fidelity QA. A visually faithful implementation still
fails if users cannot navigate, read, or operate it.

## Structure

- Interactive elements have accessible names.
- Headings follow a meaningful order.
- Repeated cards expose a useful title or label.
- Decorative images are ignored by assistive technology.
- Informative images have alt text or equivalent labels.

## Keyboard And Focus

- Keyboard users can reach every actionable element.
- Focus order follows visual order.
- Focus indicators are visible against the background.
- Composite widgets do not trap focus.

## Color And Contrast

- Body text meets WCAG contrast expectations.
- Icon-only controls remain understandable with labels or tooltips.
- Color is not the only way to convey state or severity.

## Motion And State

- Loading, disabled, selected, expanded, and error states are announced or clear.
- Motion can be reduced when the platform supports reduced motion.
- Dynamic content updates do not unexpectedly move focus.

## Repair Bias

Prefer fixing accessibility through component-level semantics so every instance
benefits from the change.

