"""FastAPI entry point for the FARO audit spike.

Endpoints:
    GET  /health  → liveness probe
    POST /audit   → run the full pipeline against a URL and return JSON

Run locally with:
    uvicorn faro_spike.main:app --reload
or:
    faro-spike  (declared as a script in pyproject.toml)
"""

from __future__ import annotations

import logging
import os
from collections import Counter

import structlog
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from faro_spike import __version__
from faro_spike.auditor import AuditError, audit_url
from faro_spike.models import AuditRequest, AuditResponse, Patch
from faro_spike.remediator import Remediator
from faro_spike.strategies import build_default_strategies

load_dotenv()

# Structured logging — easier to grep when running multiple audits in parallel.
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(message)s",
)
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)

logger = structlog.get_logger()

app = FastAPI(
    title="FARO Spike — Audit Worker",
    description=(
        "Proof of concept that validates the technical viability of FARO's "
        "audit + remediation pipeline. Not for production use."
    ),
    version=__version__,
)


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe used by Docker / Railway / curl smoke tests."""
    return {"status": "ok", "version": __version__}


@app.post("/audit", response_model=AuditResponse)
def audit(request: AuditRequest) -> AuditResponse:
    """Audit a public URL and (optionally) generate AI-assisted patches."""
    timeout_ms = int(os.environ.get("PAGE_LOAD_TIMEOUT_MS", "30000"))
    max_remediations = int(os.environ.get("MAX_REMEDIATIONS", "10"))

    try:
        violations, duration_ms = audit_url(
            url=str(request.url),
            levels=request.wcag_levels,
            page_load_timeout_ms=timeout_ms,
        )
    except AuditError as exc:
        logger.error("audit_failed", url=str(request.url), error=str(exc))
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    patches: list[Patch] = []
    if request.remediate and violations:
        strategies = build_default_strategies()
        remediator = Remediator(strategies=strategies)
        for violation in violations[:max_remediations]:
            patch = remediator.remediate(violation)
            if patch is not None:
                patches.append(patch)

    coverage = Counter(v.impact.value for v in violations)

    logger.info(
        "audit_done",
        url=str(request.url),
        violations=len(violations),
        patches=len(patches),
        duration_ms=duration_ms,
    )

    return AuditResponse(
        url=request.url,
        duration_ms=duration_ms,
        violations=violations,
        patches=patches,
        coverage_summary=dict(coverage),
    )


@app.exception_handler(Exception)
def unhandled_exception_handler(_request, exc: Exception) -> JSONResponse:  # noqa: ANN001
    """Catch-all so the spike never returns a stack trace to the client."""
    logger.exception("unhandled_exception", error=str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Check worker logs."},
    )


def run() -> None:
    """Entry point for `faro-spike` console script."""
    import uvicorn

    uvicorn.run(
        "faro_spike.main:app",
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "8000")),
        reload=False,
    )
