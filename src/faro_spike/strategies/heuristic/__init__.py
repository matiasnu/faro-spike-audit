"""Heuristic fix strategies — DOM context analysis without LLM.

These strategies look at neighbouring HTML attributes to recover semantic
information that a developer would have provided. They are not perfect,
but they bypass the LLM cost when the answer is plainly available in the
markup itself.
"""

from faro_spike.strategies.heuristic.alt_from_attrs import AltFromAttrsStrategy
from faro_spike.strategies.heuristic.label_from_placeholder import (
    LabelFromPlaceholderStrategy,
)

__all__ = ["AltFromAttrsStrategy", "LabelFromPlaceholderStrategy"]
