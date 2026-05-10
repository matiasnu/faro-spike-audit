"""Unit tests for the deterministic and heuristic fix strategies.

These run with no network and no Playwright — they validate the cascade
engine against synthetic Violation fixtures so the spike can be exercised
even without API keys or Chromium installed.
"""

from __future__ import annotations

import pytest

from faro_spike.models import Violation, ViolationImpact, ViolationNode
from faro_spike.remediator import Remediator
from faro_spike.strategies import build_default_strategies
from faro_spike.strategies.deterministic import (
    ContrastStrategy,
    LangAttributeStrategy,
    TabindexCleanupStrategy,
    TargetSizeStrategy,
)
from faro_spike.strategies.heuristic import (
    AltFromAttrsStrategy,
    LabelFromPlaceholderStrategy,
)


def _violation(rule_id: str, html: str, wcag: str = "1.4.3") -> Violation:
    return Violation(
        rule_id=rule_id,
        wcag_criterion=wcag,
        impact=ViolationImpact.SERIOUS,
        description="test",
        help="test",
        help_url="https://example.com",
        nodes=[ViolationNode(html=html, target=["html > body > x"])],
    )


# ---------- Contrast ----------

class TestContrastStrategy:
    def test_lifts_dark_text_on_white_to_meet_4_5_to_1(self) -> None:
        strategy = ContrastStrategy()
        v = _violation(
            "color-contrast",
            '<p style="color: #BBBBBB; background-color: #FFFFFF;">Hola</p>',
        )
        patch = strategy.fix(v)
        assert patch is not None
        assert "#BBBBBB" not in patch.patched_html
        assert patch.confidence == "high"

    def test_no_change_when_ratio_already_passes(self) -> None:
        strategy = ContrastStrategy()
        v = _violation(
            "color-contrast",
            '<p style="color: #000000; background-color: #FFFFFF;">Hola</p>',
        )
        # Ratio is already 21:1 — strategy should return None or unchanged.
        patch = strategy.fix(v)
        assert patch is None

    def test_skips_when_no_inline_style(self) -> None:
        strategy = ContrastStrategy()
        v = _violation("color-contrast", "<p>Hola</p>")
        assert strategy.fix(v) is None

    def test_contrast_ratio_white_on_black_is_21(self) -> None:
        ratio = ContrastStrategy._contrast_ratio("#FFFFFF", "#000000")
        assert round(ratio, 1) == 21.0


# ---------- Lang attribute ----------

class TestLangAttribute:
    def test_adds_lang_when_missing(self) -> None:
        v = _violation("html-has-lang", '<html><head></head></html>', wcag="3.1.1")
        patch = LangAttributeStrategy().fix(v)
        assert patch is not None
        assert 'lang="es"' in patch.patched_html

    def test_replaces_invalid_lang(self) -> None:
        v = _violation("html-lang-valid", '<html lang="xx-invalid">', wcag="3.1.1")
        patch = LangAttributeStrategy().fix(v)
        assert patch is not None
        assert 'lang="es"' in patch.patched_html
        assert "xx-invalid" not in patch.patched_html


# ---------- Tabindex ----------

class TestTabindexCleanup:
    def test_demotes_positive_tabindex_to_zero(self) -> None:
        v = _violation("tabindex", '<a tabindex="5" href="/x">Link</a>', wcag="2.4.3")
        patch = TabindexCleanupStrategy().fix(v)
        assert patch is not None
        assert 'tabindex="0"' in patch.patched_html

    def test_skips_when_tabindex_already_zero(self) -> None:
        v = _violation("tabindex", '<a tabindex="0">Link</a>', wcag="2.4.3")
        assert TabindexCleanupStrategy().fix(v) is None


# ---------- Target size ----------

class TestTargetSize:
    def test_appends_min_width_and_height(self) -> None:
        v = _violation("target-size", '<button>X</button>', wcag="2.5.8")
        patch = TargetSizeStrategy().fix(v)
        assert patch is not None
        assert "min-width:24px" in patch.patched_html
        assert "min-height:24px" in patch.patched_html


# ---------- Heuristic alt ----------

class TestAltFromAttrs:
    def test_copies_title_into_alt(self) -> None:
        v = _violation(
            "image-alt",
            '<img src="/x" title="Foto del equipo de FARO">',
            wcag="1.1.1",
        )
        patch = AltFromAttrsStrategy().fix(v)
        assert patch is not None
        assert 'alt="Foto del equipo de FARO"' in patch.patched_html

    def test_rejects_filename_like_titles(self) -> None:
        v = _violation("image-alt", '<img src="/x" title="banner.png">', wcag="1.1.1")
        assert AltFromAttrsStrategy().fix(v) is None


# ---------- Heuristic label ----------

class TestLabelFromPlaceholder:
    def test_copies_placeholder_into_aria_label(self) -> None:
        v = _violation(
            "label",
            '<input type="email" placeholder="Correo electrónico">',
            wcag="3.3.2",
        )
        patch = LabelFromPlaceholderStrategy().fix(v)
        assert patch is not None
        assert 'aria-label="Correo electrónico"' in patch.patched_html

    def test_humanizes_name_attribute(self) -> None:
        v = _violation("label", '<input name="first_name">', wcag="3.3.2")
        patch = LabelFromPlaceholderStrategy().fix(v)
        assert patch is not None
        assert 'aria-label="First name"' in patch.patched_html


# ---------- End-to-end cascade ----------

class TestCascade:
    def test_default_chain_runs_without_ai(self) -> None:
        chain = build_default_strategies(enable_ai=False)
        # No AI strategy should be present.
        assert all(s.cost_tier in {"deterministic", "heuristic"} for s in chain)

    def test_remediator_picks_first_high_confidence_patch(self) -> None:
        strategies = build_default_strategies(enable_ai=False)
        remediator = Remediator(strategies=strategies)
        v = _violation(
            "color-contrast",
            '<p style="color: #BBBBBB; background-color: #FFFFFF;">Hola</p>',
        )
        patch = remediator.remediate(v)
        assert patch is not None
        assert patch.confidence == "high"

    def test_remediator_returns_none_for_unhandled_rule(self) -> None:
        strategies = build_default_strategies(enable_ai=False)
        remediator = Remediator(strategies=strategies)
        v = _violation("some-future-rule", "<div></div>", wcag="9.9.9")
        assert remediator.remediate(v) is None
