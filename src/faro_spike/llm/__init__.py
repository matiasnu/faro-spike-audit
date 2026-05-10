"""LLM provider abstraction.

The remediation engine talks to whichever LLM is configured via the
`LLMProvider` protocol. This isolates FARO from any single vendor and lets
the team swap models without touching business logic — important because:

    - The spike runs on Anthropic Claude with personal credits.
    - The MVP will likely run on AWS Bedrock with academic credits.
    - The future plan Pro / Agencias may use the cheapest provider per scan.

Adding a new provider only requires a new class that implements `complete()`.
"""

from faro_spike.llm.factory import build_provider
from faro_spike.llm.provider import LLMCompletionError, LLMProvider

__all__ = ["LLMProvider", "LLMCompletionError", "build_provider"]
