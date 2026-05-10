"""Prompt templates for each WCAG rule that the spike auto-remediates.

Each module exposes a `build_prompt(violation)` function that returns the
text we send to Claude. Keeping prompts isolated by rule lets us iterate on
them independently and run regression evals in the future.
"""

from faro_spike.prompts.alt_text import build_prompt as build_alt_text_prompt
from faro_spike.prompts.contrast import build_prompt as build_contrast_prompt

__all__ = ["build_alt_text_prompt", "build_contrast_prompt"]
