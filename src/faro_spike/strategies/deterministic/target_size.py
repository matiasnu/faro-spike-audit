"""Deterministic remediation for WCAG 2.5.8 — Target Size (Minimum).

Interactive controls must measure at least 24x24 CSS pixels (WCAG 2.2 AA).
The fix is purely a CSS adjustment — append `min-width:24px;min-height:24px`
to the inline style of the offending element.
"""

from __future__ import annotations

from faro_spike.models import Patch, Violation

MIN_TARGET_PX = 24


class TargetSizeStrategy:
    """Apply min-width and min-height CSS to undersized interactive elements."""

    name = "target-size-css"
    cost_tier = "deterministic"
    supported_rules = frozenset({"target-size"})

    def can_handle(self, violation: Violation) -> bool:
        return violation.rule_id in self.supported_rules

    def fix(self, violation: Violation) -> Patch | None:
        if not violation.nodes:
            return None
        node = violation.nodes[0]
        html = node.html

        css_addition = f"min-width:{MIN_TARGET_PX}px;min-height:{MIN_TARGET_PX}px;"

        if 'style="' in html:
            patched = html.replace('style="', f'style="{css_addition}', 1)
        else:
            # Insert style attribute right before the closing of the opening tag.
            # Use the first '>' that is not inside an attribute value.
            insertion_point = html.find(">")
            if insertion_point == -1:
                return None
            patched = (
                html[:insertion_point]
                + f' style="{css_addition}"'
                + html[insertion_point:]
            )

        return Patch(
            violation_rule_id=violation.rule_id,
            target_selector=node.target[0] if node.target else "unknown",
            original_html=html,
            patched_html=patched,
            explanation=(
                f"Applied min-width:{MIN_TARGET_PX}px and min-height:{MIN_TARGET_PX}px "
                "to satisfy WCAG 2.2 AA target size minimum. Verify the surrounding "
                "layout still flows correctly."
            ),
            confidence="high",
        )
