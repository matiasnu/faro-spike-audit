"""LLM provider contract.

We use `typing.Protocol` (PEP 544) instead of an abstract base class so
implementations can be plain dataclasses or wrappers without inheriting
from FARO. This keeps the API surface minimal and the test stubs trivial.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


class LLMCompletionError(RuntimeError):
    """Raised when the underlying LLM provider fails to return usable text."""


@runtime_checkable
class LLMProvider(Protocol):
    """Anything FARO calls to turn a prompt into a completion."""

    name: str
    """Short identifier used for logs and metrics (e.g. 'anthropic', 'bedrock')."""

    def complete(
        self,
        *,
        system: str,
        user_message: str,
        max_tokens: int = 1024,
    ) -> str:
        """Send a single-turn completion request and return the text response.

        Args:
            system: System prompt setting role and rules.
            user_message: User content to remediate.
            max_tokens: Upper bound on completion length.

        Returns:
            The model's text response with no surrounding metadata.

        Raises:
            LLMCompletionError: When the provider cannot produce text.
        """
        ...
