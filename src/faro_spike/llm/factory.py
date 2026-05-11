"""Factory that builds an LLMProvider from environment variables.

The provider is selected at process start through `LLM_PROVIDER`:

    LLM_PROVIDER=anthropic   ANTHROPIC_API_KEY + CLAUDE_MODEL
    LLM_PROVIDER=bedrock     (future) AWS credentials + BEDROCK_MODEL
    LLM_PROVIDER=openai      (future) OPENAI_API_KEY + OPENAI_MODEL

Adding a new option only requires extending the `_BUILDERS` registry.
"""

from __future__ import annotations

import os
from typing import Callable

from faro_spike.llm.provider import LLMProvider


def _build_anthropic() -> LLMProvider:
    # Imported lazily so the `anthropic` package is not required when only
    # using a different provider.
    from faro_spike.llm.anthropic_provider import AnthropicProvider

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    model = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
    return AnthropicProvider(api_key=api_key, model=model)


def _build_groq() -> LLMProvider:
    from faro_spike.llm.groq_provider import GroqProvider

    api_key = os.environ.get("GROQ_API_KEY", "")
    model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
    return GroqProvider(api_key=api_key, model=model)


# Registry of available providers. New providers only need to be registered here.
_BUILDERS: dict[str, Callable[[], LLMProvider]] = {
    "anthropic": _build_anthropic,
    "groq": _build_groq,
}


def build_provider(name: str | None = None) -> LLMProvider:
    """Instantiate the configured LLMProvider.

    Args:
        name: Optional provider override. If omitted, reads `LLM_PROVIDER`
            from the environment, defaulting to ``anthropic``.

    Raises:
        ValueError: If the requested provider is not registered.
    """
    name = name or os.environ.get("LLM_PROVIDER", "anthropic")
    name = name.lower().strip()

    if name not in _BUILDERS:
        available = ", ".join(sorted(_BUILDERS))
        raise ValueError(
            f"Unknown LLM provider '{name}'. Available providers: {available}."
        )

    return _BUILDERS[name]()
