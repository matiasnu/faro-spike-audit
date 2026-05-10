"""Cascade remediation engine.

Iterates over an ordered list of `FixStrategy` instances and returns the
first patch with confidence >= medium. The chain is built externally
(see `faro_spike.strategies.registry.build_default_strategies`) so the
ordering is configurable per environment.

Patches with confidence == "low" do not short-circuit: the next strategy
in the chain is given a chance to produce something better. This is what
implements the "deterministic first, AI last" guarantee.
"""

from __future__ import annotations

import logging
from typing import Iterable

from faro_spike.models import Patch, Violation
from faro_spike.strategies.base import FixStrategy

logger = logging.getLogger(__name__)

_CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}


class Remediator:
    """Apply a chain of fix strategies to one violation at a time."""

    def __init__(self, *, strategies: Iterable[FixStrategy]) -> None:
        self._strategies = list(strategies)
        if not self._strategies:
            raise ValueError("Remediator requires at least one strategy.")

    def remediate(self, violation: Violation) -> Patch | None:
        """Run the cascade. Returns the first acceptable patch, or None."""
        best_patch: Patch | None = None
        best_strategy: str | None = None

        for strategy in self._strategies:
            if not strategy.can_handle(violation):
                continue

            patch = strategy.fix(violation)
            if patch is None:
                continue

            if _CONFIDENCE_RANK[patch.confidence] >= _CONFIDENCE_RANK["medium"]:
                logger.info(
                    "patch_produced",
                    extra={
                        "rule_id": violation.rule_id,
                        "strategy": strategy.name,
                        "tier": strategy.cost_tier,
                        "confidence": patch.confidence,
                    },
                )
                return patch

            # Low-confidence patch: keep it as fallback, try later strategies.
            if best_patch is None:
                best_patch, best_strategy = patch, strategy.name

        if best_patch is not None:
            logger.info(
                "patch_produced_low_confidence",
                extra={"rule_id": violation.rule_id, "strategy": best_strategy},
            )
        else:
            logger.debug(
                "no_strategy_handled_violation",
                extra={"rule_id": violation.rule_id},
            )
        return best_patch
