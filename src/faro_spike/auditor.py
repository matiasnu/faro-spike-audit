"""Audit a page using Playwright + axe-core.

The flow:
    1. Launch a Chromium browser via Playwright.
    2. Navigate to the target URL and wait for the network to be idle so
       JavaScript-driven content has had a chance to render.
    3. Inject the axe-core library from the official CDN into the page.
    4. Run axe.run() with the WCAG 2.1 + 2.2 A & AA tags only — this is the
       compliance scope of the FARO MVP.
    5. Parse the JSON results into our Pydantic Violation model.

axe-core is loaded directly from a CDN instead of vendored as a Python
dependency because (a) it ships official JavaScript builds, (b) we always
want the latest WCAG 2.2 rules, and (c) it avoids a transitive Node toolchain
inside our Python project.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from playwright.sync_api import Browser, Page, sync_playwright

from faro_spike.models import (
    Violation,
    ViolationImpact,
    ViolationNode,
    WCAGLevel,
)

logger = logging.getLogger(__name__)

# Pinned to a major version to keep the spike reproducible. Bump intentionally.
AXE_CORE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js"

# axe-core tag mapping for WCAG 2.1 + 2.2 levels A and AA.
# See https://github.com/dequelabs/axe-core/blob/develop/doc/API.md#axe-core-tags
WCAG_TAGS_BY_LEVEL: dict[WCAGLevel, list[str]] = {
    WCAGLevel.A: ["wcag2a", "wcag21a", "wcag22a"],
    WCAGLevel.AA: ["wcag2aa", "wcag21aa", "wcag22aa"],
}


class AuditError(Exception):
    """Raised when the audit pipeline cannot complete."""


def audit_url(
    url: str,
    levels: list[WCAGLevel],
    page_load_timeout_ms: int = 30_000,
) -> tuple[list[Violation], int]:
    """Run an axe-core audit against `url` and return the violations and elapsed ms.

    Args:
        url: Public URL to audit. Must be reachable from the runtime.
        levels: WCAG conformance levels to evaluate.
        page_load_timeout_ms: How long Playwright will wait for the page to load.

    Returns:
        A tuple of (violations, duration_ms).

    Raises:
        AuditError: If the page cannot be loaded or axe-core cannot run.
    """
    started_at = time.monotonic()
    tags = _resolve_tags(levels)

    logger.info("Starting audit", extra={"url": url, "tags": tags})

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            _navigate(page, url, page_load_timeout_ms)
            _inject_axe_core(page)
            raw_results = _run_axe(page, tags)
        finally:
            browser.close()

    violations = [_parse_violation(item) for item in raw_results.get("violations", [])]
    duration_ms = int((time.monotonic() - started_at) * 1000)

    logger.info(
        "Audit complete",
        extra={
            "url": url,
            "violations": len(violations),
            "duration_ms": duration_ms,
        },
    )
    return violations, duration_ms


def _resolve_tags(levels: list[WCAGLevel]) -> list[str]:
    """Translate WCAG levels into the axe-core tag list."""
    tags: list[str] = []
    for level in levels:
        tags.extend(WCAG_TAGS_BY_LEVEL[level])
    return tags


def _navigate(page: Page, url: str, timeout_ms: int) -> None:
    """Navigate to the target URL and wait for network activity to settle."""
    try:
        page.goto(url, wait_until="networkidle", timeout=timeout_ms)
    except Exception as exc:  # noqa: BLE001
        raise AuditError(f"Failed to load {url}: {exc}") from exc


def _inject_axe_core(page: Page) -> None:
    """Inject axe-core from the CDN into the current page context."""
    try:
        page.add_script_tag(url=AXE_CORE_CDN)
    except Exception as exc:  # noqa: BLE001
        raise AuditError(f"Failed to inject axe-core: {exc}") from exc


def _run_axe(page: Page, tags: list[str]) -> dict[str, Any]:
    """Execute axe.run() in the page context and return the parsed JSON."""
    script = """
        async (tags) => {
            const results = await axe.run(document, {
                runOnly: { type: 'tag', values: tags }
            });
            return results;
        }
    """
    return page.evaluate(script, tags)


def _parse_violation(payload: dict[str, Any]) -> Violation:
    """Translate one axe-core violation entry into our Pydantic model."""
    return Violation(
        rule_id=payload["id"],
        wcag_criterion=_extract_wcag_criterion(payload.get("tags", [])),
        impact=_parse_impact(payload.get("impact")),
        description=payload.get("description", ""),
        help=payload.get("help", ""),
        help_url=payload.get("helpUrl", ""),
        nodes=[
            ViolationNode(
                html=node.get("html", ""),
                target=[str(t) for t in node.get("target", [])],
                failure_summary=node.get("failureSummary"),
            )
            for node in payload.get("nodes", [])
        ],
    )


def _extract_wcag_criterion(tags: list[str]) -> str:
    """Pick the most specific WCAG criterion tag (e.g. 'wcag111' → '1.1.1')."""
    for tag in tags:
        if tag.startswith("wcag") and len(tag) >= 7 and tag[4:].isdigit():
            digits = tag[4:]
            return f"{digits[0]}.{digits[1]}.{digits[2:]}"
    return "unknown"


def _parse_impact(value: str | None) -> ViolationImpact:
    """Map axe-core impact strings to our enum, defaulting to MODERATE."""
    if value is None:
        return ViolationImpact.MODERATE
    try:
        return ViolationImpact(value)
    except ValueError:
        logger.warning("Unknown axe-core impact, defaulting to moderate", extra={"impact": value})
        return ViolationImpact.MODERATE


def _ensure_browser_alive(browser: Browser) -> None:
    """Defensive check used by integration tests to fail fast on driver issues."""
    if not browser.is_connected():
        raise AuditError("Playwright browser disconnected before the audit could finish.")
