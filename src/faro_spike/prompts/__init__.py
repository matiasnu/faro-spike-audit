"""Prompt templates for each WCAG rule that the spike auto-remediates.

Each module exposes `SYSTEM_PROMPT` and a `build_prompt(violation)` function
returning the user-side text to send to the LLM. Keeping prompts isolated by
rule lets us iterate independently and run regression evals later.
"""

from faro_spike.prompts import alt_text, button_name, contrast, link_name

__all__ = ["alt_text", "button_name", "contrast", "link_name"]
