"""Deterministic remediation for WCAG 3.1.1 — Language of Page.

axe-core flags this as `html-has-lang` when the `<html>` element has no
`lang` attribute, and `html-lang-valid` when the value is malformed.

Patch strategy: detect the page language from the violation context (when
available) or default to `es` for the Argentine market FARO targets first.
A future iteration will plug in a real language detector (e.g. fast-langdetect)
to be more accurate on multilingual sites.
"""

from __future__ import annotations

from faro_spike.models import Patch, Violation


class LangAttributeStrategy:
    """Add or fix the `lang` attribute on the `<html>` element."""

    name = "lang-attribute"
    cost_tier = "deterministic"
    supported_rules = frozenset({"html-has-lang", "html-lang-valid"})
    default_lang = "es"

    def can_handle(self, violation: Violation) -> bool:
        return violation.rule_id in self.supported_rules

    def fix(self, violation: Violation) -> Patch | None:
        if not violation.nodes:
            return None
        node = violation.nodes[0]
        html = node.html

        # Naive replacement: inject lang="es" right after <html.
        # Production should use a real HTML parser; for the spike this covers
        # the common case where axe gives us the literal opening <html ...> tag.
        if "<html" not in html.lower():
            return None

        if "lang=" in html.lower():
            patched = self._replace_lang(html, self.default_lang)
        else:
            patched = html.replace("<html", f'<html lang="{self.default_lang}"', 1)

        return Patch(
            violation_rule_id=violation.rule_id,
            target_selector=node.target[0] if node.target else "html",
            original_html=html,
            patched_html=patched,
            explanation=(
                f'Added lang="{self.default_lang}" on <html>. '
                "Default chosen for the Argentine market — replace with detected "
                "language if the site is multilingual."
            ),
            confidence="high",
        )

    @staticmethod
    def _replace_lang(html: str, new_value: str) -> str:
        # Replace any existing lang="..." occurrence inside the <html> tag.
        # Crude but adequate for the spike.
        import re
        return re.sub(
            r'(<html[^>]*?)\blang\s*=\s*"[^"]*"',
            rf'\1lang="{new_value}"',
            html,
            count=1,
            flags=re.IGNORECASE,
        )
