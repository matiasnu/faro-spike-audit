# Frontend 01 — HTML/CSS/JS puro — Accesible

Este frontend es la **línea base accesible**. No tiene problemas de accesibilidad intencionales.
Sirve como referencia para que el analizador pueda reportar `✅` en cada check.

---

## Qué tiene bien

### Global (todas las páginas)

| Check | Implementación |
|---|---|
| `lang="es"` en `<html>` | Todos los `.html` |
| `<title>` único por página | "Inicio — El Sauce", "Nosotros — El Sauce", etc. |
| Skip link "Saltar al contenido principal" | Primer elemento del `<body>`, visible al recibir foco |
| Landmarks semánticos | `<header role="banner">`, `<main>`, `<nav>`, `<footer role="contentinfo">` |
| Foco visible | `:focus-visible` con `outline: 3px solid #005fcc` — nunca oculto |
| Fuente escalable | `font-size: 100%` en `html`, unidades `rem` en todo el CSS |
| Contraste suficiente | Texto `#1a1a1a` sobre `#ffffff` (ratio ~19:1) |
| `prefers-reduced-motion` | Animaciones y transiciones desactivadas si el usuario lo prefiere |

### `/` — Inicio

| Check | Detalle |
|---|---|
| Imágenes con `alt` descriptivo | Tres cards con alt completo |
| Jerarquía de encabezados | `h1` → `h2` → `h3` sin saltos |
| Links con propósito claro | "Reservar una mesa", "Ver nuestro menú", "Ver receta" |
| Tabla con `<caption>`, `<th scope="col">` | Tabla de horarios |
| Sin contenido parpadeante | — |
| Sin `<iframe>` sin `title` | — |

### `/pages/about.html` — Nosotros

| Check | Detalle |
|---|---|
| Imagen con `alt` descriptivo y proporcional | Interior del restaurante |
| Tabla de equipo con `<caption>` y `<th scope="col">` | — |
| Jerarquía de encabezados correcta | `h1` → `h2` → `h3` |
| Breadcrumb con `aria-label` y `aria-current="page"` | — |

### `/pages/contact.html` — Contacto

| Check | Detalle |
|---|---|
| Todos los inputs con `<label>` asociado | `for` ↔ `id` en cada campo |
| Campos requeridos con `aria-required="true"` y `*` explicado con `<abbr>` | — |
| `aria-invalid` y `aria-describedby` en inputs | — |
| Mensaje de error con texto (no solo color) y `role="alert"` | — |
| Foco movido al primer campo inválido al enviar | `js/main.js` |
| Feedback de envío en DOM con `aria-live="polite"` | — |
| Botón con `min-height: 44px` | — |

### `/pages/reservation.html` — Reservas

| Check | Detalle |
|---|---|
| `<fieldset>` + `<legend>` para grupos de campos | Datos de contacto / Detalles |
| Selector de fecha nativo `<input type="date">` | Accesible con teclado y screen reader |
| Selector de hora con `<select>` nativo | Con `<optgroup>` para almuerzo/cena |
| Indicación de campos requeridos | `aria-required`, `*` con `<abbr>` |
| Validación con texto de error y `role="alert"` | — |

### `/pages/menu.html` — Menú

| Check | Detalle |
|---|---|
| Items del menú como `<ul>/<li>` | Lista semántica |
| Precios con `aria-label="Precio: $X.XXX"` | No depende solo del color |
| Filtros con `aria-pressed` actualizado | Estado comunicado al screen reader |
| `LiveAnnouncer` equivalente: sin JS extra | Los botones son `<button>` nativos |

---

## Lo que el analizador debería reportar

```
frontend-01/index.html              → sin errores detectados
frontend-01/pages/about.html        → sin errores detectados
frontend-01/pages/contact.html      → sin errores detectados
frontend-01/pages/reservation.html  → sin errores detectados
frontend-01/pages/menu.html         → sin errores detectados
```
