"""FARO Spike 0 — proof of concept for WCAG 2.2 audit + AI remediation.

This package validates the technical viability of the core audit pipeline:
    URL → Playwright (render DOM) → axe-core (detect violations) →
    Claude API (generate patches) → JSON response.

It is intentionally minimal: no database, no auth, no GitHub integration.
The goal is to de-risk the most critical part of FARO before committing to
the full architecture in MVP Phase 1.
"""

__version__ = "0.1.0"
