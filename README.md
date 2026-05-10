# faro-spike-audit

> **FARO Spike 0** — proof of concept for the WCAG 2.2 audit + AI remediation pipeline.

This repository validates the technical viability of FARO's core flow before
committing to the full architecture in MVP Phase 1. It is intentionally
minimal: no database, no auth, no GitHub integration. **Do not use in
production.**

The goal is to answer two questions:

1. Can we reliably detect WCAG A + AA violations on a real-world public URL
   using `Playwright + axe-core`?
2. Can Claude generate code patches that a developer would accept on a Pull
   Request review?

If both answers are *yes*, FARO becomes feasible. If not, we pivot before
investing in the full stack.

## Scope

Two WCAG criteria covered for the spike:

| Criterion | Rule | Strategy |
| --- | --- | --- |
| 1.1.1 Non-text Content | `image-alt` | Claude generates alt-text from page context |
| 1.4.3 Contrast (Minimum) | `color-contrast` | Claude suggests new foreground hex |

Out of scope for the spike: keyboard traps, ARIA, multi-page crawling,
multimedia, GitHub PR creation, persistence.

## Stack

- **Python 3.12+**
- **FastAPI** — HTTP layer
- **Playwright** — headless Chromium to render JS-driven pages
- **axe-core** (CDN-injected) — Deque's WCAG rule engine
- **Anthropic Claude SDK** — patch generation
- **structlog** — JSON logs

## Quickstart

### Option A — Docker (recommended for the team)

```bash
# 1. Build and start. No .env or API key needed for the no-AI spike phase.
docker compose up --build

# 2. From another terminal, hit the endpoint.
curl -X POST http://localhost:8000/audit \
    -H "Content-Type: application/json" \
    -d '{"url": "https://www.example.com"}'
```

The container ships Chromium and every system dependency Playwright needs.
By default `ENABLE_AI_REMEDIATION=false`, so the worker runs end-to-end
using only the deterministic + heuristic strategies. To enable the LLM
tier later, copy `.env.example` to `.env`, set `ENABLE_AI_REMEDIATION=true`
plus `ANTHROPIC_API_KEY=...`, and restart with `docker compose up`.

### Option B — Local Python (for development with hot reload)

```bash
# 1. Install uv (https://docs.astral.sh/uv/) if you don't have it.
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install dependencies.
uv sync --extra dev

# 3. Install the Chromium binary Playwright will drive.
uv run playwright install chromium

# 4. (Optional) configure provider for AI remediation.
cp .env.example .env
# Leave ENABLE_AI_REMEDIATION=false for the spike, or set it to true and add ANTHROPIC_API_KEY.

# 5. Run the worker.
uv run faro-spike

# 6. Hit the endpoint.
curl -X POST http://localhost:8000/audit \
    -H "Content-Type: application/json" \
    -d '{"url": "https://www.example.com"}'
```

## Remediation engine

Patches are produced by a cascade of strategies in cost order:

1. **Deterministic** — pure algorithms (WCAG luminance for contrast,
   `lang` injection, `tabindex` cleanup, target size CSS, focus outline).
   Zero tokens, microsecond runtime, high confidence.
2. **Heuristic** — DOM context analysis (derive `alt` from `title`/
   `aria-label`, derive `aria-label` from `placeholder`/`name`).
   Still zero tokens, medium confidence.
3. **AI** (only when `ENABLE_AI_REMEDIATION=true`) — `LLMProvider`
   abstraction (Anthropic Claude by default; AWS Bedrock / OpenAI
   pluggable). Used as last resort for criteria where pure code
   cannot infer the right answer.

The Remediator returns the first patch with confidence ≥ medium. If
nothing applies, the violation is reported without a patch and the
client is expected to open a manual Issue.

## Project layout

```
faro-spike-audit/
├── README.md
├── Dockerfile                 ← Playwright + Python image
├── docker-compose.yml         ← One-command dev setup
├── pyproject.toml
├── .env.example
├── src/faro_spike/
│   ├── main.py                ← FastAPI app, POST /audit
│   ├── auditor.py             ← Playwright + axe-core injection
│   ├── remediator.py          ← Cascade engine (no LLM logic here)
│   ├── models.py              ← Pydantic models
│   ├── llm/                   ← Pluggable LLM provider (only if AI enabled)
│   │   ├── provider.py        ← LLMProvider Protocol
│   │   ├── factory.py         ← build_provider() reads LLM_PROVIDER env
│   │   └── anthropic_provider.py
│   ├── strategies/            ← Cascade fix strategies
│   │   ├── base.py            ← FixStrategy Protocol
│   │   ├── registry.py        ← build_default_strategies()
│   │   ├── deterministic/     ← contrast, lang, tabindex, target-size, focus
│   │   ├── heuristic/         ← alt from attrs, label from placeholder
│   │   └── ai/                ← LLMRemediationStrategy (lazy-loaded)
│   └── prompts/
│       ├── alt_text.py
│       └── contrast.py
└── tests/
    ├── test_auditor.py        ← unit + integration (Playwright gated)
    ├── test_strategies.py     ← cascade engine + per-strategy tests
    └── fixtures/sample_page.html
```

## Tests

```bash
# Unit tests (no network, no browser).
uv run pytest

# Integration test against the local HTML fixture (requires Chromium).
FARO_RUN_INTEGRATION=1 uv run pytest -k integration
```

## Acceptance criteria for the spike

The spike is considered successful (Sprint 0 closed) when:

1. The worker correctly identifies `image-alt` and `color-contrast`
   violations on **at least 3 real-world Argentine sites** (an agency web,
   a `.gob.ar` site, and a fintech) without crashing.
2. Claude returns a syntactically valid HTML patch in **≥ 80%** of cases for
   `image-alt` on a hand-curated corpus of 20 violations.
3. End-to-end audit + remediation of 10 violations completes in **under 30
   seconds** wall-clock time.
4. Per-scan Anthropic API cost stays **under USD 0.30** for a typical page.

If any of these fails, the spike report identifies the root cause and the
team decides whether to absorb it (slower MVP) or pivot the architecture.

## Context

FARO is the Final Project (Proyecto Final) for Ingeniería en Sistemas de
Información — UTN FRBA, course 5504, group 4 (2026 cohort).

Team:

- Maiolo, Joaquín — Equipo Dinamita
- **Nuñez, Matías Ezequiel** — Equipo Técnico (this repo's owner)
- Ruival, Julián — Equipo Docu
- Verger, Manuel — Equipo Docu
- **Villarruel, Ignacio** — Equipo Técnico (this repo's owner)
