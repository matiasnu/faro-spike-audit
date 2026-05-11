"""Groq implementation of LLMProvider.

Groq runs open-weight models (Llama 3.3 70B by default) on custom LPU
hardware with sub-200ms time-to-first-token. The free tier accepts
1000 requests/day per model — enough for the spike and the early MVP
without a credit card.

Two practical reasons FARO defaults to Groq when AI remediation is on:

    1. Privacy: Groq does not train on user prompts. Anthropic's free
       tier and Google Gemini's free tier do, which is unacceptable
       once we audit code from real banking or agency clients.
    2. Coding quality: Llama 3.3 70B scores 88.4% on HumanEval, on par
       with Claude Sonnet for HTML/CSS/ARIA generation tasks.

The Groq SDK is API-compatible with OpenAI's chat.completions, so
swapping to OpenAI later is a one-line change.
"""

from __future__ import annotations

import logging

from groq import APIError, Groq

from faro_spike.llm.provider import LLMCompletionError

logger = logging.getLogger(__name__)


class GroqProvider:
    """LLMProvider that calls Groq's chat.completions API."""

    name = "groq"

    def __init__(self, *, api_key: str, model: str) -> None:
        if not api_key:
            raise ValueError("Groq provider requires a non-empty API key.")
        self._client = Groq(api_key=api_key)
        self._model = model

    def complete(
        self,
        *,
        system: str,
        user_message: str,
        max_tokens: int = 1024,
    ) -> str:
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_message},
                ],
            )
        except APIError as exc:
            logger.error("groq_api_error", extra={"error": str(exc)})
            raise LLMCompletionError(f"Groq API failed: {exc}") from exc

        if not response.choices:
            raise LLMCompletionError("Groq returned no choices.")

        text = response.choices[0].message.content
        if not text:
            raise LLMCompletionError("Groq returned empty content.")

        return text
