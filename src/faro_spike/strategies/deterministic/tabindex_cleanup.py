"""Deterministic remediation for WCAG 2.4.3 — Focus Order.

Positive `tabindex` values (anything > 0) override the natural DOM tab
order and almost always create accessibility bugs. The safe automated
fix is to demote the value to `0` (still focusable, but in DOM order).
Negative values (`tabindex="-1"`) are intentional and left untouched.

Reordering the actual DOM is too risky — that's a manual decision.
"""

from __future__ import annotations

import re

from faro_spike.models import Patch, Violation

TABINDEX_PATTERN = re.compile(r'\btabindex\s*=\s*"(\d+)"', re.IGNORECASE)


class TabindexCleanupStrategy:
    """Reset positive tabindex values to 0."""

    name = "tabindex-cleanup"
    cost_tier = "deterministic"
    supported_rules = frozenset({"tabindex"})

    def can_handle(self, violation: Violation) -> bool:
        return violation.rule_id in self.supported_rules

    def fix(self, violation: Violation) -> Patch | None:
        if not violation.nodes:
            return None
        node = violation.nodes[0]

        match = TABINDEX_PATTERN.search(node.html)
        if not match:
            return None
        original_value = int(match.group(1))
        if original_value == 0:
            return None  # Already compliant.

        patched_html = TABINDEX_PATTERN.sub('tabindex="0"', node.html, count=1)

        return Patch(
            violation_rule_id=violation.rule_id,
            target_selector=node.target[0] if node.target else "unknown",
            original_html=node.html,
            patched_html=patched_html,
            explanation=(
                f"Demoted tabindex from {original_value} to 0 to restore natural "
                "DOM tab order. Reordering the DOM itself is left to the developer "
                "because it can break visual layouts."
            ),
            confidence="high",
        )
