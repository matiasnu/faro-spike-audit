"""Layered remediation strategies.

FARO follows a cascade: each violation is attempted by strategies in order
of cost — deterministic algorithms first (no tokens, microseconds), then
heuristic DOM-context analysis (still no tokens), and finally LLM-backed
remediation (paid tokens, slower) only if nothing else can produce a
high-confidence patch.

The Remediator iterates the strategies and returns the first patch with
confidence >= medium. If no strategy applies, the violation falls back to
a human-reviewed Issue (out of spike scope).

This design lets the spike run end-to-end with ZERO API calls during the
audit phase — covering ~60% of the auto-remediated criteria in the MVP
without any LLM cost.
"""

from faro_spike.strategies.base import FixStrategy
from faro_spike.strategies.registry import build_default_strategies

__all__ = ["FixStrategy", "build_default_strategies"]
