"""Deterministic remediation for WCAG 1.4.4 — Resize Text.

axe rule: `meta-viewport`. The fix is to remove `user-scalable=no/0` and
any `maximum-scale` <= 1 from the viewport meta content, so users can zoom.
This is purely textual transformation — zero risk.
"""

from __future__ import annotations

import re

from faro_spike.models import Patch, Violation

CONTENT_PATTERN = re.compile(r'\bcontent\s*=\s*"([^"]*)"', re.IGNORECASE)
USER_SCALABLE_PATTERN = re.compile(r"\s*,?\s*user-scalable\s*=\s*(?:no|0)\s*,?\s*", re.IGNORECASE)
MAX_SCALE_PATTERN = re.compile(r"\s*,?\s*maximum-scale\s*=\s*(?:1(?:\.0)?|0(?:\.\d+)?)\s*,?\s*", re.IGNORECASE)


class MetaViewportStrategy:
    """Strip user-scalable=no and capped maximum-scale from meta viewport."""

    name = "meta-viewport-allow-zoom"
    cost_tier = "deterministic"
    supported_rules = frozenset({"meta-viewport"})

    def can_handle(self, violation: Violation) -> bool:
        return violation.rule_id in self.supported_rules

    def fix(self, violation: Violation) -> Patch | None:
        if not violation.nodes:
            return None
        node = violation.nodes[0]
        html = node.html

        match = CONTENT_PATTERN.search(html)
        if not match:
            return None
        original_content = match.group(1)

        cleaned = USER_SCALABLE_PATTERN.sub(", ", original_content)
        cleaned = MAX_SCALE_PATTERN.sub(", ", cleaned)
        cleaned = re.sub(r"\s*,\s*", ", ", cleaned).strip(" ,")

        if cleaned == original_content.strip():
            return None  # nothing to change

        patched_html = html.replace(
            f'content="{original_content}"',
            f'content="{cleaned}"',
            1,
        )

        return Patch(
            violation_rule_id=violation.rule_id,
            target_selector=node.target[0] if node.target else "meta[name=viewport]",
            original_html=html,
            patched_html=patched_html,
            explanation=(
                "Removed user-scalable=no and any maximum-scale<=1 from the viewport "
                "meta. Users with low vision can now zoom up to 500% as required by "
                "WCAG 2.2 1.4.4 (Resize Text)."
            ),
            confidence="high",
        )
