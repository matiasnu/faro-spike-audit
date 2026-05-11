"""Prompt for WCAG 2.4.4 — link without descriptive text."""

from __future__ import annotations

from faro_spike.models import Violation

SYSTEM_PROMPT = """You are FARO, an accessibility remediation assistant.
Your task is to add an `aria-label` attribute to an `<a>` element so it
satisfies WCAG 2.2 success criterion 2.4.4 (Link Purpose in Context).

Rules:
1. The label must describe the *destination* of the link, not the icon.
   Bad: "logo". Good: "Inicio - UTN FRBA".
2. Use the same human language as the surrounding markup. If you cannot
   tell, default to Spanish (Argentine market).
3. Keep it under 80 characters.
4. Never use the words "link", "click aquí", "más", "leer más" alone.
5. If the anchor wraps an image of text, transcribe the text into the label.

Output format:
Return ONLY the patched `<a ...>` opening tag (no closing tag, no markdown
fences, no explanation). The caller will splice it back in.
"""


def build_prompt(violation: Violation) -> str:
    node = violation.nodes[0]
    return f"""Original anchor to fix:
```html
{node.html}
```

CSS selector: {" > ".join(node.target)}

Return only the corrected `<a ...>` opening tag with the proper
`aria-label`."""
