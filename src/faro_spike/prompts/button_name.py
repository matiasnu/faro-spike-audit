"""Prompt for WCAG 4.1.2 — button without accessible text."""

from __future__ import annotations

from faro_spike.models import Violation

SYSTEM_PROMPT = """You are FARO, an accessibility remediation assistant.
Your task is to add an `aria-label` attribute to a `<button>` so it
satisfies WCAG 2.2 success criterion 4.1.2 (Name, Role, Value).

Rules:
1. The label must describe the *action* the button performs (e.g. "Buscar",
   "Cerrar diálogo"), not the icon inside it.
2. Use the same human language as the surrounding markup. If you cannot
   tell, default to Spanish (Argentine market).
3. Keep it under 60 characters.
4. Never use the words "button", "boton", "click here", "clickear acá".

Output format:
Return ONLY the patched `<button ...>` opening tag (no closing tag, no
markdown fences, no explanation). The caller will splice it back in.
"""


def build_prompt(violation: Violation) -> str:
    node = violation.nodes[0]
    return f"""Original button to fix:
```html
{node.html}
```

CSS selector: {" > ".join(node.target)}

Return only the corrected `<button ...>` opening tag with the proper
`aria-label`."""
