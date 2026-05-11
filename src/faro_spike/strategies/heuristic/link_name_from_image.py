"""Heuristic fix for WCAG 2.4.4 — link without accessible text.

axe rule: `link-name`. Most cases in real Argentine sites: a banner link
wraps an `<img>` with no text and the anchor has no aria-label. We can
synthesise a label from:

    1. inner img alt / title (if non-empty and not noise)
    2. existing title / aria-labelledby on the anchor
    3. humanised path of the href when it carries semantic value
       (e.g. /reuniones-informativas-febrero-2026/ → "Reuniones informativas febrero 2026")

If everything fails we defer to the LLM tier or leave the violation for
human review.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

from faro_spike.models import Patch, Violation

INNER_IMG_PATTERN = re.compile(r"<img\b([^>]*)>", re.IGNORECASE)
ATTR_PATTERN = re.compile(r'\b(\w[\w-]*)\s*=\s*"([^"]*)"', re.IGNORECASE)
ARIA_LABEL_PATTERN = re.compile(r'\baria-label\s*=\s*"', re.IGNORECASE)
ANCHOR_TITLE_PATTERN = re.compile(r'<a\b[^>]*\btitle\s*=\s*"([^"]+)"', re.IGNORECASE)
HREF_PATTERN = re.compile(r'\bhref\s*=\s*"([^"]+)"', re.IGNORECASE)

NOISE_PATTERNS = (
    re.compile(r"^img[_-]?\d+$", re.IGNORECASE),
    re.compile(r"^dsc[_-]?\d+$", re.IGNORECASE),
    re.compile(r"^[0-9a-f-]{20,}$", re.IGNORECASE),
    re.compile(r"^banner[_-]?\w*$", re.IGNORECASE),
    re.compile(r"^logo[_-]?\w*$", re.IGNORECASE),
    re.compile(r"^image$", re.IGNORECASE),
)

# Pages we recognise from URL path conventions and label naturally.
PATH_LABEL_HINTS = {
    "siuguarani": "Acceso a SIU Guaraní",
    "campus": "Campus virtual",
    "biblioteca": "Biblioteca",
    "contacto": "Contacto",
    "/en": "English version",
    "/en/": "English version",
}


class LinkNameFromImageStrategy:
    """Synthesise an aria-label for anchors that wrap an icon or image banner."""

    name = "link-name-from-image"
    cost_tier = "heuristic"
    supported_rules = frozenset({"link-name"})

    def can_handle(self, violation: Violation) -> bool:
        return violation.rule_id in self.supported_rules

    def fix(self, violation: Violation) -> Patch | None:
        if not violation.nodes:
            return None
        node = violation.nodes[0]
        html = node.html

        if "<a" not in html.lower() or ARIA_LABEL_PATTERN.search(html):
            return None

        inferred, source = self._infer_label(html)
        if not inferred:
            return None

        patched = re.sub(
            r"(<a\b)",
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
        # 1) Anchor's own title attribute.
        if title_match := ANCHOR_TITLE_PATTERN.search(html):
            value = title_match.group(1).strip()
            if value and not cls._is_noise(value):
                return value, "anchor title attribute"

        # 2) Inner image alt / title / filename.
        if inner_img_match := INNER_IMG_PATTERN.search(html):
            attrs = dict(ATTR_PATTERN.findall(inner_img_match.group(1)))

            if (alt := attrs.get("alt", "").strip()) and not cls._is_noise(alt):
                return alt, "inner img alt"

            if (title := attrs.get("title", "").strip()) and not cls._is_noise(title):
                return title, "inner img title"

            if (src := attrs.get("src")) and (humanised := cls._humanise_src(src)):
                return humanised, "inner img filename"

        # 3) Humanised href path.
        if href_match := HREF_PATTERN.search(html):
            href = href_match.group(1)
            if hinted := cls._hinted_label(href):
                return hinted, "href path hint"
            if humanised := cls._humanise_path(href):
                return humanised, "href path slug"

        return None, None

    @staticmethod
    def _hinted_label(href: str) -> str | None:
        path = urlparse(href).path or href
        for needle, label in PATH_LABEL_HINTS.items():
            if needle in path:
                return label
        return None

    @classmethod
    def _humanise_path(cls, href: str) -> str | None:
        path = urlparse(href).path
        if not path or path in {"/", ""}:
            return None
        last = [seg for seg in path.split("/") if seg][-1] if path else ""
        if not last or cls._is_noise(last):
            return None
        words = re.split(r"[\s_\-]+", last.strip())
        cleaned = " ".join(w for w in words if w and not w.isdigit())
        return cleaned.capitalize() if cleaned else None

    @classmethod
    def _humanise_src(cls, src: str) -> str | None:
        path = urlparse(src).path
        stem = re.sub(r"\.[a-zA-Z0-9]+$", "", path.rsplit("/", 1)[-1])
        if not stem or cls._is_noise(stem):
            return None
        words = re.split(r"[\s_\-]+", stem.strip())
        cleaned = " ".join(w for w in words if w and not w.isdigit())
        return cleaned.capitalize() if cleaned else None

    @staticmethod
    def _is_noise(value: str) -> bool:
        return any(p.match(value) for p in NOISE_PATTERNS)
