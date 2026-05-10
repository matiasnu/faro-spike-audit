"""LLM-backed fix strategies — last resort, paid tokens.

Only invoked when no deterministic or heuristic strategy can produce a
high-confidence patch. Wraps the LLMProvider abstraction so the underlying
model (Claude, Bedrock, OpenAI) is interchangeable.
"""

from faro_spike.strategies.ai.llm_strategy import LLMRemediationStrategy

__all__ = ["LLMRemediationStrategy"]
