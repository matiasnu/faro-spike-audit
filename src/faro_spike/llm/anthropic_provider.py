"""Anthropic Claude implementation of LLMProvider.

Used by default during the spike because it has the lowest setup friction
(personal API key, free tier credits). Migrating to AWS Bedrock for the MVP
only requires writing a sibling provider class — `Remediator` does not change.
"""

from __future__ import annotations

import logging

from anthropic import Anthropic, APIError
from anthropic.types import MessageParam

from faro_spike.llm.provider import LLMCompletionError

logger = logging.getLogger(__name__)


class AnthropicProvider:
    """LLMProvider that calls the Anthropic Messages API."""

    name = "anthropic"

    def __init__(self, *, api_key: str, model: str) -> None:
        if not api_key:
            raise ValueError("Anthropic provider requires a non-empty API key.")
        self._client = Anthropic(api_key=api_key)
        self._model = model

    def complete(
        self,
        *,
        system: str,
        user_message: str,
        max_tokens: int = 1024,
    ) -> str:
        messages: list[MessageParam] = [{"role": "user", "content": user_message}]
        try:
            response = self._client.messages.create(
                model=self._model,
                max_tokens=max_tokens,
                system=system,
                messages=messages,
            )
        except APIError as exc:
            logger.error("anthropic_api_error", extra={"error": str(exc)})
            raise LLMCompletionError(f"Anthropic API failed: {exc}") from exc

        for block in response.content:
            if block.type == "text":
                return block.text

        raise LLMCompletionError("Anthropic returned no text content.")
