"""Heuristic fix for WCAG 4.1.2 — button without accessible name.

axe rule: `button-name`. Common pattern in Argentine sites (UTN, banks,
agencies) is a `<button>` whose only child is an `<img>` (search icon,
hamburger menu, etc.). The right fix is `aria-label` on the button derived
from the inner image's alt/title or, as fallback, from a humanised filename.

If nothing usable can be inferred, return None and let the LLM tier (or a
human Issue) take over.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

from faro_spike.models import Patch, Violation

INNER_IMG_PATTERN = re.compile(r"<img\b([^>]*)>", re.IGNORECASE)
ATTR_PATTERN = re.compile(r'\b(\w[\w-]*)\s*=\s*"([^"]*)"', re.IGNORECASE)
ARIA_LABEL_PATTERN = re.compile(r'\baria-label\s*=\s*"', re.IGNORECASE)
TYPE_PATTERN = re.compile(r'\btype\s*=\s*"(submit|reset|button)"', re.IGNORECASE)

DEFAULT_BY_TYPE = {
    "submit": "Enviar formulario",
    "reset": "Limpiar formulario",
}

# Filenames that carry no semantic value — we won't humanise these.
NOISE_PATTERNS = (
    re.compile(r"^img[_-]?\d+$", re.IGNORECASE),
    re.compile(r"^dsc[_-]?\d+$", re.IGNORECASE),
    re.compile(r"^[0-9a-f-]{20,}$", re.IGNORECASE),  # hashes / UUIDs
    re.compile(r"^untitled", re.IGNORECASE),
    re.compile(r"^image$", re.IGNORECASE),
)


class ButtonNameFromImageStrategy:
    """Synthesise an aria-label for buttons that wrap an icon."""

    name = "button-name-from-image"
    cost_tier = "heuristic"
    supported_rules = frozenset({"button-name"})

    def can_handle(self, violation: Violation) -> bool:
        return violation.rule_id in self.supported_rules

    def fix(self, violation: Violation) -> Patch | None:
        if not violation.nodes:
            return None
        node = violation.nodes[0]
        html = node.html

        if "<button" not in html.lower() or ARIA_LABEL_PATTERN.search(html):
            return None

        inferred, source = self._infer_label(html)
        if not inferred:
            return None

        patched = re.sub(
            r"(<button\b)",
            rf'\1 aria-label="{inferred}"',
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
                f'Derived aria-label="{inferred}" from {source}. '
                "Heuristic fix — review for fidelity before merging."
            ),
            confidence="medium",
        )

    # ------------------------------------------------------------------

    @classmethod
    def _infer_label(cls, html: str) -> tuple[str | None, str | None]:
        """Try, in order: inner img alt, inner img title, filename, button type."""
        inner_img_match = INNER_IMG_PATTERN.search(html)
        if inner_img_match:
            attrs = dict(ATTR_PATTERN.findall(inner_img_match.group(1)))

            if (alt := attrs.get("alt", "").strip()) and not cls._is_noise(alt):
                return alt, "inner img alt"

            if (title := attrs.get("title", "").strip()) and not cls._is_noise(title):
                return title, "inner img title"

            if (src := attrs.get("src")) and (humanised := cls._humanise_src(src)):
                return humanised, "inner img filename"

        if type_match := TYPE_PATTERN.search(html):
            default = DEFAULT_BY_TYPE.get(type_match.group(1).lower())
            if default:
                return default, f'button type="{type_match.group(1).lower()}"'

        return None, None

    @classmethod
    def _humanise_src(cls, src: str) -> str | None:
        path = urlparse(src).path
        stem = re.sub(r"\.[a-zA-Z0-9]+$", "", path.rsplit("/", 1)[-1])
        if not stem or cls._is_noise(stem):
            return None
        words = re.split(r"[\s_\-]+", stem.strip())
        cleaned = " ".join(w for w in words if w)
        return cleaned.capitalize() if cleaned else None

    @staticmethod
    def _is_noise(value: str) -> bool:
        return any(p.match(value) for p in NOISE_PATTERNS)
