"""Prompt for WCAG 1.4.3 — Contrast (Minimum).

Note: in production we will use a deterministic algorithm to compute the
new hex value (relative luminance + WCAG formula). We only fall back to
Claude when the violation involves complex backgrounds (gradients, images)
where the deterministic approach is not safe.

For the spike we ask Claude to suggest a new color *and* explain its choice
so we can compare against the deterministic algorithm later.
"""

from __future__ import annotations

from faro_spike.models import Violation


SYSTEM_PROMPT = """You are FARO, an accessibility remediation assistant.
Your task is to fix a color contrast violation under WCAG 2.2 success
criterion 1.4.3 (Contrast — Minimum), which requires:
    - 4.5:1 ratio for normal text
    - 3:1 ratio for large text (18pt+ or 14pt+ bold)

Rules:
1. Adjust ONLY the foreground color of the offending element. Do not change
   the background — that may cascade visually across the site.
2. Stay within the same hue when possible (preserve brand identity).
3. Output the new color as a hex value `#RRGGBB`.
4. Provide a one-sentence explanation suitable for a developer code review.

Output format (JSON, no markdown fences):
{
    "patched_color": "#RRGGBB",
    "explanation": "One sentence."
}
"""


def build_prompt(violation: Violation) -> str:
    """Build the user prompt for a contrast violation.

    Args:
        violation: The axe-core violation, expected to be a `color-contrast` rule.

    Returns:
        User message text. The system prompt is set separately by the caller.
    """
    primary_node = violation.nodes[0]
    return f"""Element with insufficient contrast:
```html
{primary_node.html}
```

Failure summary from axe-core:
{primary_node.failure_summary or "(no detail provided)"}

Return the JSON object as specified."""
