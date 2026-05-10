"""Deterministic remediation for WCAG 1.4.3 + 1.4.11 — Contrast.

Implements the relative-luminance algorithm from WCAG 2.2 Technique G18:

    L_relative = 0.2126*R + 0.7152*G + 0.0722*B

with the per-channel sRGB-to-linear transform:

    component_linear = component_srgb / 12.92                 if c_srgb <= 0.03928
                     = ((c_srgb + 0.055) / 1.055) ** 2.4      otherwise

Contrast ratio:

    ratio = (L_lighter + 0.05) / (L_darker + 0.05)

Targets:
    - 1.4.3 (text):           4.5  (3.0 for large text)
    - 1.4.11 (UI components): 3.0

Patch strategy: keep the foreground hue, walk it toward black or white in
HSL lightness steps until the ratio target is met. This preserves brand
identity better than blindly switching to #000 or #FFF.
"""

from __future__ import annotations

import colorsys
import logging
import re

from faro_spike.models import Patch, Violation

logger = logging.getLogger(__name__)

# axe-core attaches structured metadata to color-contrast violations on each
# node (`any[].data` includes fgColor, bgColor, contrastRatio, expectedContrastRatio).
# We do not currently parse axe's `any` payload — for the spike we infer from
# the inline style on the offending element, which covers the common case.

HEX_PATTERN = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})")
INLINE_STYLE_PATTERN = re.compile(r'style\s*=\s*"([^"]*)"', re.IGNORECASE)
COLOR_PROP_PATTERN = re.compile(r"\bcolor\s*:\s*([^;]+);?", re.IGNORECASE)
BG_PROP_PATTERN = re.compile(r"\bbackground(?:-color)?\s*:\s*([^;]+);?", re.IGNORECASE)


class ContrastStrategy:
    """Adjust the foreground color of an element so the contrast ratio passes."""

    name = "contrast-luminance"
    cost_tier = "deterministic"
    supported_rules = frozenset({"color-contrast", "color-contrast-enhanced"})
    target_ratio_text = 4.5
    target_ratio_ui = 3.0
    max_iterations = 100

    def can_handle(self, violation: Violation) -> bool:
        return violation.rule_id in self.supported_rules

    def fix(self, violation: Violation) -> Patch | None:
        if not violation.nodes:
            return None
        node = violation.nodes[0]

        fg_hex, bg_hex = self._extract_colors(node.html)
        if fg_hex is None or bg_hex is None:
            logger.debug(
                "contrast_strategy_skipped_no_inline_colors",
                extra={"html_snippet": node.html[:120]},
            )
            return None

        target = (
            self.target_ratio_ui
            if violation.rule_id == "color-contrast-enhanced"
            else self.target_ratio_text
        )

        adjusted_hex = self._adjust_to_meet_ratio(fg_hex, bg_hex, target)
        if adjusted_hex is None or adjusted_hex.lower() == fg_hex.lower():
            return None

        patched_html = node.html.replace(fg_hex, adjusted_hex, 1)
        ratio = self._contrast_ratio(adjusted_hex, bg_hex)

        return Patch(
            violation_rule_id=violation.rule_id,
            target_selector=node.target[0] if node.target else "unknown",
            original_html=node.html,
            patched_html=patched_html,
            explanation=(
                f"Foreground adjusted from {fg_hex} to {adjusted_hex} against "
                f"background {bg_hex} via WCAG luminance algorithm. "
                f"New ratio: {ratio:.2f}:1 (target {target}:1). "
                "Hue preserved by walking lightness in HSL space."
            ),
            confidence="high",
        )

    # ------------------------------------------------------------------
    # Color parsing
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_colors(html: str) -> tuple[str | None, str | None]:
        """Best-effort extraction of fg + bg from inline style attributes."""
        style_match = INLINE_STYLE_PATTERN.search(html)
        if not style_match:
            return None, None
        style = style_match.group(1)

        fg_match = COLOR_PROP_PATTERN.search(style)
        bg_match = BG_PROP_PATTERN.search(style)

        fg = ContrastStrategy._normalize_hex(fg_match.group(1)) if fg_match else None
        bg = ContrastStrategy._normalize_hex(bg_match.group(1)) if bg_match else "#FFFFFF"
        return fg, bg

    @staticmethod
    def _normalize_hex(value: str) -> str | None:
        value = value.strip()
        m = HEX_PATTERN.search(value)
        if not m:
            return None
        hex_value = m.group(1)
        if len(hex_value) == 3:
            hex_value = "".join(c * 2 for c in hex_value)
        return f"#{hex_value.upper()}"

    # ------------------------------------------------------------------
    # WCAG contrast math
    # ------------------------------------------------------------------

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        h = hex_color.lstrip("#")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    @staticmethod
    def _rgb_to_hex(r: int, g: int, b: int) -> str:
        return f"#{r:02X}{g:02X}{b:02X}"

    @staticmethod
    def _relative_luminance(hex_color: str) -> float:
        r, g, b = ContrastStrategy._hex_to_rgb(hex_color)

        def channel(c: int) -> float:
            srgb = c / 255.0
            return srgb / 12.92 if srgb <= 0.03928 else ((srgb + 0.055) / 1.055) ** 2.4

        return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

    @classmethod
    def _contrast_ratio(cls, fg_hex: str, bg_hex: str) -> float:
        l1 = cls._relative_luminance(fg_hex)
        l2 = cls._relative_luminance(bg_hex)
        lighter, darker = max(l1, l2), min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)

    # ------------------------------------------------------------------
    # Patch search: walk HSL lightness preserving hue
    # ------------------------------------------------------------------

    @classmethod
    def _adjust_to_meet_ratio(
        cls,
        fg_hex: str,
        bg_hex: str,
        target_ratio: float,
    ) -> str | None:
        """Return a new fg hex that meets target contrast against bg, or None."""
        if cls._contrast_ratio(fg_hex, bg_hex) >= target_ratio:
            return fg_hex

        r, g, b = cls._hex_to_rgb(fg_hex)
        h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

        bg_luminance = cls._relative_luminance(bg_hex)
        # If the background is light, push fg darker; otherwise push it lighter.
        step = -0.01 if bg_luminance > 0.5 else 0.01

        for _ in range(cls.max_iterations):
            l = max(0.0, min(1.0, l + step))
            nr, ng, nb = colorsys.hls_to_rgb(h, l, s)
            candidate = cls._rgb_to_hex(int(nr * 255), int(ng * 255), int(nb * 255))
            if cls._contrast_ratio(candidate, bg_hex) >= target_ratio:
                return candidate
            if l <= 0.0 or l >= 1.0:
                break
        return None
