"""Composes the default strategy chain for the Remediator.

The chain is built in cost order: deterministic → heuristic → AI. The AI
strategy is added only when AI remediation is explicitly enabled (env var
`ENABLE_AI_REMEDIATION=true`), so the spike can run end-to-end with zero
token consumption while we wait for an Anthropic key or AWS Bedrock access.
"""

from __future__ import annotations

import logging
import os

from faro_spike.strategies.base import FixStrategy
from faro_spike.strategies.deterministic import (
    ContrastStrategy,
    FocusVisibleStrategy,
    LangAttributeStrategy,
    MetaViewportStrategy,
    TabindexCleanupStrategy,
    TargetSizeStrategy,
)
from faro_spike.strategies.heuristic import (
    AltFromAttrsStrategy,
    ButtonNameFromImageStrategy,
    FrameTitleFromSrcStrategy,
    LabelFromPlaceholderStrategy,
    LinkNameFromImageStrategy,
)

logger = logging.getLogger(__name__)


def build_default_strategies(*, enable_ai: bool | None = None) -> list[FixStrategy]:
    """Return the ordered strategy chain to feed into Remediator.

    Args:
        enable_ai: Optional override. If None, reads `ENABLE_AI_REMEDIATION`
            from the environment (default `false`). When False, the chain
            stops at the heuristic tier and unhandled violations fall back
            to a human-reviewed Issue.
    """
    if enable_ai is None:
        enable_ai = os.environ.get("ENABLE_AI_REMEDIATION", "false").lower() == "true"

    chain: list[FixStrategy] = [
        # Deterministic tier (no tokens, microseconds).
        ContrastStrategy(),
        LangAttributeStrategy(),
        TabindexCleanupStrategy(),
        TargetSizeStrategy(),
        FocusVisibleStrategy(),
        MetaViewportStrategy(),
        # Heuristic tier (no tokens, DOM context analysis).
        AltFromAttrsStrategy(),
        ButtonNameFromImageStrategy(),
        LinkNameFromImageStrategy(),
        LabelFromPlaceholderStrategy(),
        FrameTitleFromSrcStrategy(),
    ]

    if enable_ai:
        # Lazy imports to keep `anthropic` out of the cold path when AI is off.
        from faro_spike.llm import build_provider
        from faro_spike.strategies.ai import LLMRemediationStrategy

        try:
            provider = build_provider()
            chain.append(LLMRemediationStrategy(provider=provider))
            logger.info("ai_strategy_enabled", extra={"provider": provider.name})
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "ai_strategy_disabled_provider_init_failed",
                extra={"error": str(exc)},
            )
    else:
        logger.info("ai_strategy_disabled_by_config")

    return chain
