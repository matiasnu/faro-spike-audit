"""Heuristic fix for WCAG 1.1.1 — Non-text Content.

When an `<img>` is missing `alt` but already has a `title`, `aria-label`
or `aria-labelledby`, we can derive a sensible alt without calling the LLM.
This pattern is surprisingly common: developers add `title` for tooltips
without realising it does not satisfy axe.
"""

from __future__ import annotations

import re

from faro_spike.models import Patch, Violation

ATTRIBUTE_PATTERNS = {
    "title": re.compile(r'\btitle\s*=\s*"([^"]*)"', re.IGNORECASE),
    "aria-label": re.compile(r'\baria-label\s*=\s*"([^"]*)"', re.IGNORECASE),
}


class AltFromAttrsStrategy:
    """Copy a meaningful attribute (title, aria-label) into the alt attribute."""

    name = "alt-from-existing-attrs"
    cost_tier = "heuristic"
    supported_rules = frozenset({"image-alt"})

    def can_handle(self, violation: Violation) -> bool:
        return violation.rule_id in self.supported_rules

    def fix(self, violation: Violation) -> Patch | None:
        if not violation.nodes:
            return None
        node = violation.nodes[0]
        html = node.html

        for source, pattern in ATTRIBUTE_PATTERNS.items():
            match = pattern.search(html)
            if not match:
                continue
            value = match.group(1).strip()
            if not value or self._looks_like_filename(value):
                continue
            patched = self._inject_alt(html, value)
            if patched is None:
                continue
            return Patch(
                violation_rule_id=violation.rule_id,
                target_selector=node.target[0] if node.target else "unknown",
                original_html=html,
                patched_html=patched,
                explanation=(
                    f'Derived alt="{value}" from the existing {source} attribute. '
                    "Heuristic fix — review for fidelity before merging."
                ),
                confidence="medium",
            )
        return None

    @staticmethod
    def _inject_alt(html: str, alt_value: str) -> str | None:
        if "alt=" in html.lower():
            return None  # Already has alt; let another strategy handle invalid alt.
        if "<img" not in html.lower():
            return None
        # Insert alt right after the <img tag opening.
        return re.sub(
            r"(<img\b)",
            rf'\1 alt="{alt_value}"',
            html,
            count=1,
            flags=re.IGNORECASE,
        )

    @staticmethod
    def _looks_like_filename(value: str) -> bool:
        """Reject obvious filenames like 'banner.png' or 'IMG_4231'."""
        lowered = value.lower()
        return (
            lowered.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"))
            or lowered.startswith("img_")
            or lowered.startswith("dsc")
        )
