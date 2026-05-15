"""Heuristic fix for WCAG 4.1.2 — `<iframe>` without accessible name.

axe rule: `frame-title`. We synthesise a `title` attribute from the src
URL using domain-specific keyword detection. Common cases observed in
Argentine sites:

    - Bot-protection / WAF iframes (Incapsula, Cloudflare, reCAPTCHA)
    - Brand logos served from CDN (logo.prismasystems.com.ar, etc.)
    - Embedded video (YouTube, Vimeo)
    - Map embeds (Google Maps)

If nothing matches we still emit a generic but honest title built from
the iframe's domain — better than failing axe, easy to override.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

from faro_spike.models import Patch, Violation

SRC_PATTERN = re.compile(r'\bsrc\s*=\s*"([^"]+)"', re.IGNORECASE)
TITLE_PATTERN = re.compile(r'\btitle\s*=\s*"', re.IGNORECASE)
NAME_PATTERN = re.compile(r'\bname\s*=\s*"([^"]+)"', re.IGNORECASE)

# Keyword → friendly Spanish title mapping.
KEYWORD_HINTS: tuple[tuple[str, str], ...] = (
    ("incapsula", "Verificación de seguridad"),
    ("recaptcha", "Verificación de seguridad reCAPTCHA"),
    ("hcaptcha", "Verificación de seguridad hCaptcha"),
    ("challenge", "Verificación de seguridad"),
    ("cloudflare", "Verificación de seguridad"),
    ("youtube", "Video embebido"),
    ("youtu.be", "Video embebido"),
    ("vimeo", "Video embebido"),
    ("/maps", "Mapa embebido"),
    ("google.com/maps", "Mapa de Google"),
    ("logo", "Logotipo"),
    ("payment", "Pasarela de pago"),
    ("checkout", "Pasarela de pago"),
)


class FrameTitleFromSrcStrategy:
    """Synthesise a title attribute for iframes that have none."""

    name = "frame-title-from-src"
    cost_tier = "heuristic"
    supported_rules = frozenset({"frame-title"})

    def can_handle(self, violation: Violation) -> bool:
        return violation.rule_id in self.supported_rules

    def fix(self, violation: Violation) -> Patch | None:
        if not violation.nodes:
            return None
        node = violation.nodes[0]
        html = node.html

        if "<iframe" not in html.lower() or TITLE_PATTERN.search(html):
            return None

        inferred, source = self._infer_title(html)
        if not inferred:
            return None

        patched = re.sub(
            r"(<iframe\b)",
            rf'\1 title="{inferred}"',
            html,
            count=1,
            flags=re.IGNORECASE,
        )

        return Patch(
            violation_rule_id=violation.rule_id,
            target_selector=node.target[0] if node.target else "iframe",
            original_html=html,
            patched_html=patched,
            explanation=(
                f'Derived title="{inferred}" from {source}. Heuristic fix — '
                "review for fidelity before merging."
            ),
            confidence="medium",
        )

    @staticmethod
    def _infer_title(html: str) -> tuple[str | None, str | None]:
        # 1) name attribute (rare but free win)
        if name_match := NAME_PATTERN.search(html):
            value = name_match.group(1).strip()
            if value:
                return value, "iframe name attribute"

        # 2) src — try keyword hints first, then fall back to domain
        if src_match := SRC_PATTERN.search(html):
            src = src_match.group(1)
            lowered = src.lower()
            for keyword, label in KEYWORD_HINTS:
                if keyword in lowered:
                    return label, f"iframe src keyword '{keyword}'"

            try:
                parsed = urlparse(src)
                host = (parsed.hostname or "").replace("www.", "")
                if host:
                    return f"Contenido embebido de {host}", "iframe src domain"
            except ValueError:
                pass

        return None, None
