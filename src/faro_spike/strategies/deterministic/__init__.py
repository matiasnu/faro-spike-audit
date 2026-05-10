"""Deterministic fix strategies — pure code, no LLM.

These cover WCAG criteria where the correct patch can be computed
algorithmically from the offending HTML/CSS, with zero ambiguity:

    - 1.4.3 + 1.4.11 contrast (luminance algorithm)
    - 3.1.1 lang attribute (language detection)
    - 2.4.3 tabindex cleanup (remove tabindex > 0)
    - 2.5.8 target size (apply CSS min-height/min-width)
    - 2.4.7 focus visible (default outline if missing)

Each module exposes a single class implementing FixStrategy.
"""

from faro_spike.strategies.deterministic.contrast import ContrastStrategy
from faro_spike.strategies.deterministic.focus_visible import FocusVisibleStrategy
from faro_spike.strategies.deterministic.lang_attribute import LangAttributeStrategy
from faro_spike.strategies.deterministic.tabindex_cleanup import TabindexCleanupStrategy
from faro_spike.strategies.deterministic.target_size import TargetSizeStrategy

__all__ = [
    "ContrastStrategy",
    "FocusVisibleStrategy",
    "LangAttributeStrategy",
    "TabindexCleanupStrategy",
    "TargetSizeStrategy",
]
