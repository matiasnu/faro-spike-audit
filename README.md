# faro-spike-audit

> **FARO Spike 0** — proof of concept del motor de auditoría WCAG 2.2 + remediación.

Worker mínimo que recibe una URL, la renderiza con Chromium, corre axe-core
sobre el DOM post-JavaScript, y devuelve las violaciones detectadas + los
patches automáticos que el motor de cascada pudo generar.

**Pensado para validar la viabilidad técnica de FARO antes del MVP.** No es
production-ready: sin auth, sin DB, sin GitHub App, sin multi-tenant.

---

## TL;DR para correrlo en 3 comandos

```bash
git clone git@github.com:matiasnu/faro-spike-audit.git
cd faro-spike-audit
docker compose up --build
```

Listo. Endpoints en `http://localhost:8000`. **No necesitás API key ni `.env`** —
el spike corre por defecto con el motor determinístico + heurístico, sin gastar
un solo token.

---

## Requisitos

Solo uno: **Docker** con Compose v2.

| SO | Cómo instalarlo |
| :--- | :--- |
| macOS / Windows | [Docker Desktop](https://www.docker.com/products/docker-desktop/) — incluye todo. |
| macOS con Colima | `brew install colima docker docker-compose` y `colima start --cpu 4 --memory 6` |
| Linux | `sudo apt install docker-ce docker-compose-plugin` (ver [docs.docker.com](https://docs.docker.com/engine/install/)) |

**Verificá que el daemon esté corriendo** antes de seguir:

```bash
docker ps
```

Si te tira `Cannot connect to the Docker daemon`, arrancá Docker Desktop o
`colima start`.

---

## Probar el endpoint

### Health check

```bash
curl http://localhost:8000/health
# {"status":"ok","version":"0.1.0"}
```

### Auditar una URL

```bash
curl -s -X POST http://localhost:8000/audit \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.utn.edu.ar"}' | jq .
```

Respuesta abreviada:

```json
{
  "url": "https://www.utn.edu.ar",
  "duration_ms": 4321,
  "violations": [
    {
      "rule_id": "color-contrast",
      "wcag_criterion": "1.4.3",
      "impact": "serious",
      "nodes": [...]
    }
  ],
  "patches": [
    {
      "violation_rule_id": "color-contrast",
      "original_html": "<p style=\"color:#BBBBBB;...\">",
      "patched_html":  "<p style=\"color:#767676;...\">",
      "confidence": "high",
      "explanation": "Foreground adjusted from #BBBBBB to #767676..."
    }
  ],
  "coverage_summary": {"serious": 3, "moderate": 5, "minor": 2}
}
```

### Swagger UI (más cómodo)

Abrí en el browser: **http://localhost:8000/docs**

Tenés un playground interactivo para tirar requests, ver el schema completo de
`AuditRequest`/`AuditResponse` y compartirlo con los docentes en RD/RE.

### Output más legible

```bash
curl -s -X POST http://localhost:8000/audit -H "Content-Type: application/json" \
    -d '{"url":"https://www.utn.edu.ar"}' \
  | jq '{
      total_violations: (.violations | length),
      total_patches:    (.patches | length),
      duration_ms,
      coverage_summary,
      rules_detected:   [.violations[].rule_id] | unique,
      patches_summary:  [.patches[] | {rule: .violation_rule_id, confidence}]
    }'
```

---

## Cómo funciona el motor de remediación

Cada violación pasa por una **cascada** de strategies en orden de costo:

| Tier | Costo | Cuándo aplica | Reglas que cubre |
| :--- | :--- | :--- | :--- |
| 1. Determinístico | Cero tokens, microsegundos | Algoritmos puros (ej. luminancia WCAG) | contraste, lang, tabindex, target size, focus visible |
| 2. Heurístico | Cero tokens, milisegundos | El DOM ya tiene la respuesta cerca | alt-from-title, label-from-placeholder |
| 3. IA (opcional) | Tokens de Anthropic / Bedrock | Necesita entender semántica | alt-text contextual, reescritura de links genéricos |

El Remediator devuelve el **primer patch con confianza ≥ medium**. Si nada
aplica, la violación queda en el reporte sin patch (modelo human-in-the-loop:
el cliente la resuelve manualmente o se emite un Issue).

**Por defecto el tier 3 está apagado** (`ENABLE_AI_REMEDIATION=false`). El spike
demuestra la viabilidad sin gastar un token. Para activar IA más adelante:

```bash
cp .env.example .env
# editar y poner:
#   ENABLE_AI_REMEDIATION=true
#   ANTHROPIC_API_KEY=sk-ant-...
docker compose up
```

---

## Comandos útiles

```bash
# Levantar en foreground (logs en consola)
docker compose up

# Rebuild forzando que no use el cache
docker compose build --no-cache

# Ver logs sin attach
docker compose logs -f worker

# Apagar y limpiar
docker compose down

# Limpiar todo (incluye imagen)
docker compose down --rmi all
```

---

## Troubleshooting

**`Cannot connect to the Docker daemon`**
Arrancá Docker Desktop o `colima start`. Verificá con `docker ps`.

**`Readme file does not exist: README.md` durante el build**
Asegurate de tener este archivo en el repo. El build de hatchling lo lee como
metadata del paquete. Si lo ignoraste en `.dockerignore`, sacalo de ahí.

**`BrowserType.launch: Executable doesn't exist at /ms-playwright/...`**
Mismatch entre la versión del SDK Playwright (resuelto por `uv sync`) y el
Chromium que vino con la imagen base. Actualizá la imagen del Dockerfile a
la versión que pide el error y rebuildeá:
```bash
docker compose build --no-cache
```

**Apple Silicon (M1/M2/M3) — la imagen no carga**
Forzar arquitectura amd64 en Colima:
```bash
colima stop && colima start --arch x86_64 --cpu 4 --memory 6
```

**El audit tarda > 30 segundos sobre sitios grandes**
Subir el timeout en `docker-compose.yml`:
```yaml
environment:
  PAGE_LOAD_TIMEOUT_MS: "60000"
```

**Probar sin Docker (modo dev local)**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --extra dev
uv run playwright install chromium
uv run faro-spike
```

---

## Estructura del proyecto

```
faro-spike-audit/
├── README.md                  ← este archivo
├── Dockerfile                 ← imagen Playwright + Python + uv
├── docker-compose.yml         ← orquestación
├── pyproject.toml             ← deps + scripts
├── .env.example               ← variables (solo necesario para activar IA)
├── src/faro_spike/
│   ├── main.py                ← FastAPI: GET /health, POST /audit
│   ├── auditor.py             ← Playwright + axe-core (CDN-injected)
│   ├── remediator.py          ← orquestador de cascada
│   ├── models.py              ← Pydantic v2: AuditRequest, Violation, Patch
│   ├── strategies/            ← motor de cascada
│   │   ├── deterministic/     ← contraste, lang, tabindex, target-size, focus
│   │   ├── heuristic/         ← alt-from-attrs, label-from-placeholder
│   │   ├── ai/                ← LLM (lazy, solo si ENABLE_AI_REMEDIATION=true)
│   │   └── registry.py        ← build_default_strategies()
│   ├── llm/                   ← provider pluggable (Anthropic, Bedrock, ...)
│   └── prompts/               ← templates por criterio (alt_text, contrast)
└── tests/
    ├── test_auditor.py        ← unit tests + integración Playwright
    ├── test_strategies.py     ← cascada end-to-end + por strategy
    └── fixtures/sample_page.html  ← fixture con violaciones intencionales
```

---

## Tests

```bash
# Unit tests sin Chromium (rápidos)
docker compose run --rm worker pytest tests/test_strategies.py -q

# Integración con Chromium real (lento)
docker compose run --rm -e FARO_RUN_INTEGRATION=1 worker pytest -q
```

---

## Acceptance criteria del spike

El spike se considera exitoso (Sprint 0 cerrado) cuando:

1. El worker detecta violaciones WCAG sin crashear sobre **3 sitios reales**
   (un sitio universitario, un `.gob.ar` y una agencia web argentina).
2. La cascada determinística + heurística genera patches con confianza
   `high` o `medium` para al menos `1.4.3`, `3.1.1`, `2.4.3`, `2.5.8` y
   `image-alt` cuando hay título disponible.
3. El audit + remediation de hasta 10 violaciones termina en **< 30 segundos**
   wall-clock sobre páginas de complejidad media.
4. El motor corre **sin un solo token consumido** (modo default).

Si esos 4 puntos pasan, la viabilidad técnica de FARO queda demostrada antes
de invertir en MVP completo, según lo declarado en el Estudio de Factibilidad
y el Documento de Arquitectura del proyecto.

---

## Equipo

FARO — Proyecto Final UTN FRBA — Curso 5504 (K5052) — Grupo 4 — Cohorte 2026.

| Legajo | Integrante | Rol |
| :--- | :--- | :--- |
| 172.848-9 | Maiolo, Joaquín | Equipo Dinamita (Acta + WBS + Gantt) |
| **171.532-0** | **Nuñez, Matías Ezequiel** | **Equipo Técnico — owner de este repo** |
| 175.637-0 | Ruival, Julián | Equipo Docu |
| 220.979-2 | Verger, Manuel | Equipo Docu |
| **176.100-6** | **Villarruel, Ignacio** | **Equipo Técnico — co-owner de este repo** |

Profesores a cargo del proyecto: Balduzzi, Silvia · Ferrari Gallo, Valeria.
Director de cátedra: Mag. Ing. Gabriela Salem.
