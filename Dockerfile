# syntax=docker/dockerfile:1.7
#
# FARO Spike worker — Playwright-ready Python container.
#
# We start from Microsoft's official Playwright Python image, which already
# ships Chromium + every Linux system dependency it needs (libnss3, libxkb,
# fonts, etc.). Saves ~300 MB of layers vs building from python:slim and
# running `playwright install-deps` ourselves.

FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy AS base

# Don't write .pyc files; force unbuffered stdout for clean container logs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv

# Install uv (fast resolver) — single small binary.
COPY --from=ghcr.io/astral-sh/uv:0.5.7 /uv /uvx /usr/local/bin/

WORKDIR /app

# Layer 1: dependency manifests only — keeps the image cache hot when only
# source code changes.
COPY pyproject.toml ./
RUN uv venv /opt/venv && uv sync --no-install-project --no-dev

# Layer 2: project source.
COPY src/ ./src/
COPY tests/ ./tests/
RUN uv sync --no-dev

# Default runtime configuration. Override at `docker run` time with -e.
ENV HOST=0.0.0.0 \
    PORT=8000 \
    PAGE_LOAD_TIMEOUT_MS=30000 \
    MAX_REMEDIATIONS=10 \
    LOG_LEVEL=INFO \
    ENABLE_AI_REMEDIATION=false

EXPOSE 8000

# Health probe used by docker-compose and orchestrators.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python3 -c "import urllib.request,sys; \
        sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health',timeout=3).status==200 else 1)"

CMD ["/opt/venv/bin/uvicorn", "faro_spike.main:app", "--host", "0.0.0.0", "--port", "8000"]
