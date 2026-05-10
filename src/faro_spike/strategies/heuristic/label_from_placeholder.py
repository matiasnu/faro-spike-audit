"""Heuristic fix for WCAG 3.3.2 — Labels or Instructions.

If an `<input>` has no associated `<label>` but ships with a meaningful
`placeholder`, `name`, or `aria-label` we can synthesise an `aria-label`
from that data. Placeholders alone do not satisfy WCAG 3.3.2 (they
disappear when the user types), so we mirror the value as `aria-label`.
"""

from __future__ import annotations

import re

from faro_spike.models import Patch, Violation

PLACEHOLDER_PATTERN = re.compile(r'\bplaceholder\s*=\s*"([^"]*)"', re.IGNORECASE)
NAME_PATTERN = re.compile(r'\bname\s*=\s*"([^"]*)"', re.IGNORECASE)
ARIA_LABEL_PATTERN = re.compile(r'\baria-label\s*=\s*"', re.IGNORECASE)


class LabelFromPlaceholderStrategy:
    """Promote a placeholder/name into an aria-label when no label is present."""

    name = "aria-label-from-placeholder"
    cost_tier = "heuristic"
    supported_rules = frozenset({"label", "label-title-only"})

    def can_handle(self, violation: Violation) -> bool:
        return violation.rule_id in self.supported_rules

    def fix(self, violation: Violation) -> Patch | None:
        if not violation.nodes:
            return None
        node = violation.nodes[0]
        html = node.html

        if "<input" not in html.lower() and "<select" not in html.lower():
            return None
        if ARIA_LABEL_PATTERN.search(html):
            return None  # Already has aria-label.

        derived = None
        source = None
        if (m := PLACEHOLDER_PATTERN.search(html)) and m.group(1).strip():
            derived = m.group(1).strip()
            source = "placeholder"
        elif (m := NAME_PATTERN.search(html)) and m.group(1).strip():
            derived = self._humanize(m.group(1).strip())
            source = "name"

        if not derived:
            return None

        patched = re.sub(
            r"(<(?:input|select)\b)",
            rf'\1 aria-label="{derived}"',
            html,
            count=1,
            flags=re.IGNORECASE,
        )

        return Patch(
            violation_rule_id=violation.rule_id,
            target_selector=node.target[0] if node.target else "unknown",
            original_html=html,
            patched_html=patched,
            explanation=(
                f'Derived aria-label="{derived}" from the existing {source} '
                "attribute. Heuristic fix — a real <label> remains preferable."
            ),
            confidence="medium",
        )

    @staticmethod
    def _humanize(name: str) -> str:
        """Turn 'first_name' or 'firstName' into 'First name'."""
        cleaned = re.sub(r"[_-]+", " ", name)
        cleaned = re.sub(r"(?<!^)(?=[A-Z])", " ", cleaned)
        return cleaned.strip().capitalize()
