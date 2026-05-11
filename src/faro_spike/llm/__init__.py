"""LLM provider abstraction.

The remediation engine talks to whichever LLM is configured via the
`LLMProvider` protocol. This isolates FARO from any single vendor and lets
the team swap models without touching business logic. Default: Groq (free
tier, no training on user data, sub-200ms latency).

    - Spike default: Groq + Llama 3.3 70B Versatile (free tier).
    - Optional: Anthropic Claude Sonnet (paid tokens, premium quality).
    - Future: AWS Bedrock with academic credits, OpenAI, Gemini, ...

Adding a new provider only requires a new class that implements `complete()`
and a one-line entry in `factory._BUILDERS`.
"""

from faro_spike.llm.factory import build_provider
from faro_spike.llm.provider import LLMCompletionError, LLMProvider

__all__ = ["LLMProvider", "LLMCompletionError", "build_provider"]
