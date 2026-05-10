"""Prompt for WCAG 1.1.1 — Non-text Content (alt-text generation).

Strategy:
    - We give Claude the offending HTML (typically `<img src="..." />`) plus the
      surrounding context so it can infer whether the image is decorative,
      informative or functional.
    - Claude is instructed to return *only* the patched HTML so we can apply
      the diff deterministically without parsing free-form text.
    - We explicitly forbid generic alt-text like "image" or "photo" because
      those fail WCAG meaningfulness in spirit even if the rule passes.
"""

from __future__ import annotations

from faro_spike.models import Violation


SYSTEM_PROMPT = """You are FARO, an accessibility remediation assistant.
Your task is to add a meaningful `alt` attribute to an HTML image element so
it complies with WCAG 2.2 success criterion 1.1.1 (Non-text Content).

Rules:
1. If the image is decorative (icon adjacent to a link with text, background
   visual ornament), return alt="".
2. If the image is informative, write a short alt (under 125 characters) that
   conveys the same information a sighted user would get.
3. If the image is functional (inside a button/link with no visible text),
   describe the action the control performs, not the image itself.
4. Never use the words "image", "photo", "picture" inside alt text — they are
   redundant for screen readers.
5. Use the same human language as the surrounding page when possible.

Output format:
Return ONLY the patched HTML element, no markdown fences, no explanation.
"""


def build_prompt(violation: Violation, *, page_language: str | None = None) -> str:
    """Build a user prompt for the alt-text remediation.

    Args:
        violation: The axe-core violation, expected to be a `image-alt` rule.
        page_language: Optional ISO language code of the page (e.g. "es", "en").

    Returns:
        The user message to send to Claude.
    """
    primary_node = violation.nodes[0]
    language_hint = (
        f"\n\nPage language hint: {page_language}." if page_language else ""
    )

    return f"""Original element to fix:
```html
{primary_node.html}
```

CSS selector path: {" > ".join(primary_node.target)}{language_hint}

Return only the corrected HTML element with the proper `alt` attribute."""
