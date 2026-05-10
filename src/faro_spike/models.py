"""Pydantic models shared across the spike.

Kept intentionally small — only what is needed to represent an audit request,
the violations detected by axe-core, and the patches proposed by Claude.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class WCAGLevel(str, Enum):
    """WCAG conformance levels supported by FARO."""

    A = "A"
    AA = "AA"


class ViolationImpact(str, Enum):
    """Severity scale used by axe-core for a detected violation."""

    MINOR = "minor"
    MODERATE = "moderate"
    SERIOUS = "serious"
    CRITICAL = "critical"


class AuditRequest(BaseModel):
    """Input payload for POST /audit."""

    url: HttpUrl = Field(..., description="Public URL of the page to audit.")
    wcag_levels: list[WCAGLevel] = Field(
        default_factory=lambda: [WCAGLevel.A, WCAGLevel.AA],
        description="WCAG conformance levels to evaluate (default: A + AA).",
    )
    remediate: bool = Field(
        default=True,
        description="If True, call Claude to generate patches for each violation.",
    )


class ViolationNode(BaseModel):
    """A single DOM node where the violation was detected."""

    html: str = Field(..., description="HTML snippet of the offending element.")
    target: list[str] = Field(..., description="CSS selectors that locate the node.")
    failure_summary: str | None = Field(
        default=None,
        description="Human-readable summary of why the node fails the rule.",
    )


class Violation(BaseModel):
    """A WCAG rule violation reported by axe-core for one or more nodes."""

    rule_id: str = Field(..., description="axe-core rule identifier (e.g. 'image-alt').")
    wcag_criterion: str = Field(
        ...,
        description="WCAG success criterion ID (e.g. '1.1.1').",
    )
    impact: ViolationImpact
    description: str
    help: str
    help_url: str
    nodes: list[ViolationNode]


class Patch(BaseModel):
    """A code change proposed by the LLM to fix a violation."""

    violation_rule_id: str
    target_selector: str = Field(
        ...,
        description="CSS selector pointing to the node being patched.",
    )
    original_html: str
    patched_html: str
    explanation: str = Field(
        ...,
        description="Plain-language explanation of the fix for the developer review.",
    )
    confidence: Literal["high", "medium", "low"]


class AuditResponse(BaseModel):
    """Output payload for POST /audit."""

    url: HttpUrl
    duration_ms: int
    violations: list[Violation]
    patches: list[Patch]
    coverage_summary: dict[str, int] = Field(
        default_factory=dict,
        description="Counts grouped by impact level.",
    )
