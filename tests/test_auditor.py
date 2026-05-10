"""Smoke tests for the auditor.

The integration test is opt-in via the ``FARO_RUN_INTEGRATION`` env var
because it requires a real Chromium binary installed by Playwright.

To enable, after `uv sync --extra dev`, run:
    playwright install chromium
    FARO_RUN_INTEGRATION=1 pytest -k integration
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from faro_spike.auditor import _extract_wcag_criterion, _parse_impact, audit_url
from faro_spike.models import ViolationImpact, WCAGLevel

FIXTURE = Path(__file__).parent / "fixtures" / "sample_page.html"


def test_extract_wcag_criterion_picks_specific_tag() -> None:
    tags = ["wcag2aa", "wcag143"]
    assert _extract_wcag_criterion(tags) == "1.4.3"


def test_extract_wcag_criterion_unknown_for_non_numeric_tags() -> None:
    assert _extract_wcag_criterion(["best-practice"]) == "unknown"


def test_parse_impact_defaults_to_moderate() -> None:
    assert _parse_impact(None) is ViolationImpact.MODERATE


def test_parse_impact_handles_unknown_values() -> None:
    assert _parse_impact("catastrophic") is ViolationImpact.MODERATE


def test_parse_impact_returns_known_value() -> None:
    assert _parse_impact("critical") is ViolationImpact.CRITICAL


@pytest.mark.skipif(
    os.environ.get("FARO_RUN_INTEGRATION") != "1",
    reason="Integration test requires Playwright Chromium installed.",
)
def test_audit_local_fixture_detects_known_violations() -> None:
    """End-to-end: audit the local fixture and assert key violations are caught."""
    url = FIXTURE.resolve().as_uri()
    violations, duration_ms = audit_url(
        url=url,
        levels=[WCAGLevel.A, WCAGLevel.AA],
    )

    rule_ids = {v.rule_id for v in violations}

    # The fixture intentionally fails these rules. If axe-core stops detecting
    # them we want the test to scream.
    assert "image-alt" in rule_ids, "Expected 1.1.1 image-alt violation"
    assert "color-contrast" in rule_ids, "Expected 1.4.3 color-contrast violation"
    assert "html-has-lang" in rule_ids, "Expected 3.1.1 html-has-lang violation"

    assert duration_ms > 0
