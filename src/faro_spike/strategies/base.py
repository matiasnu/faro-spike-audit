"""Strategy contract for the cascade remediation engine.

Each strategy decides if it can handle a violation, and if so, returns a
Patch (or None to defer to the next strategy). Strategies are composed
into an ordered chain by `Remediator`.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from faro_spike.models import Patch, Violation


@runtime_checkable
class FixStrategy(Protocol):
    """A pluggable remediation strategy."""

    name: str
    """Short identifier used in logs and patch metadata (e.g. 'contrast-algo')."""

    cost_tier: str
    """One of 'deterministic', 'heuristic', 'ai' — used for ordering and metrics."""

    def can_handle(self, violation: Violation) -> bool:
        """Return True if this strategy is responsible for `violation`'s rule_id."""
        ...

    def fix(self, violation: Violation) -> Patch | None:
        """Produce a Patch for the violation, or None if the strategy cannot solve it."""
        ...
