"""Heuristic fix strategies — DOM context analysis without LLM.

These strategies look at neighbouring HTML attributes to recover semantic
information that a developer would have provided. They are not perfect,
but they bypass the LLM cost when the answer is plainly available in the
markup itself.
"""

from faro_spike.strategies.heuristic.alt_from_attrs import AltFromAttrsStrategy
from faro_spike.strategies.heuristic.button_name_from_image import (
    ButtonNameFromImageStrategy,
)
from faro_spike.strategies.heuristic.frame_title_from_src import (
    FrameTitleFromSrcStrategy,
)
from faro_spike.strategies.heuristic.label_from_placeholder import (
    LabelFromPlaceholderStrategy,
)
from faro_spike.strategies.heuristic.link_name_from_image import (
    LinkNameFromImageStrategy,
)

__all__ = [
    "AltFromAttrsStrategy",
    "ButtonNameFromImageStrategy",
    "FrameTitleFromSrcStrategy",
    "LabelFromPlaceholderStrategy",
    "LinkNameFromImageStrategy",
]
