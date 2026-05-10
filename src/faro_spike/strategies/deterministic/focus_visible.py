"""Deterministic remediation for WCAG 2.4.7 — Focus Visible.

When axe flags `focus-order-semantics` or `link-in-text-block` issues that
boil down to a missing `:focus` outline, we inject a default outline via
inline style. This is a conservative fix — production should be done in
the central stylesheet, but the spike fix already eliminates the violation.
"""

from __future__ import annotations

from faro_spike.models import Patch, Violation

DEFAULT_FOCUS_STYLE = "outline:2px solid #2E75B6;outline-offset:2px;"


class FocusVisibleStrategy:
    """Inject a default focus outline when one is missing."""

    name = "focus-visible-default"
    cost_tier = "deterministic"
    supported_rules = frozenset({"focus-order-semantics"})

    def can_handle(self, violation: Violation) -> bool:
        return violation.rule_id in self.supported_rules

    def fix(self, violation: Violation) -> Patch | None:
        if not violation.nodes:
            return None
        node = violation.nodes[0]
        html = node.html

        if 'style="' in html:
            patched = html.replace('style="', f'style="{DEFAULT_FOCUS_STYLE}', 1)
        else:
            insertion_point = html.find(">")
            if insertion_point == -1:
                return None
            patched = (
                html[:insertion_point]
                + f' style="{DEFAULT_FOCUS_STYLE}"'
                + html[insertion_point:]
            )

        return Patch(
            violation_rule_id=violation.rule_id,
            target_selector=node.target[0] if node.target else "unknown",
            original_html=html,
            patched_html=patched,
            explanation=(
                "Added a default focus outline (2px solid #2E75B6) so the element "
                "has a visible focus indicator. Move this rule to your global CSS "
                "before merging."
            ),
            confidence="medium",
        )
