# Frontend 02 — Problemas de accesibilidad introducidos intencionalmente

Este frontend es un sitio de restaurante (El Sauce) construido con HTML, CSS y JS puro,
diseñado para tener la mayor cantidad posible de problemas de accesibilidad detectables
por un analizador automatizado.

Cada problema está etiquetado con:
- La **discapacidad** que afecta
- El **principio WCAG** que viola (Perceptible / Operable / Comprensible / Robusto)
- El **archivo y elemento** concreto donde aparece

---

## Problemas transversales (presentes en todas las páginas)

| # | Problema | Discapacidad | WCAG | Archivo / elemento |
|---|---|---|---|---|
| T1 | Sin atributo `lang` en `<html>` | Visual total | Comprensible | Todos los `.html` |
| T2 | `outline: none !important` — foco completamente invisible al navegar con teclado | Motora severa | Operable | `css/styles.css` — regla global `*` |
| T3 | `font-size: 13px` fijo en `html` y `body` — no escala al aumentar el tamaño de fuente del navegador | Baja visión | Perceptible | `css/styles.css` |
| T4 | Sin landmarks semánticos — `<div>` en lugar de `<header>`, `<main>`, `<nav>`, `<footer>` | Visual total | Robusto | Todos los `.html` |
| T5 | Sin skip link "saltar al contenido principal" | Motora severa, Visual total | Operable | Todos los `.html` |
| T6 | `<title>` idéntico "Inicio" en todas las páginas — no permite identificar la página activa | Visual total | Comprensible | Todos los `.html` — `<head>` |
| T7 | Contraste de texto insuficiente — color `#999999` sobre `#ffffff` (ratio ~2.8:1, mínimo requerido 4.5:1) | Baja visión, Daltonismo | Perceptible | `css/styles.css` — variable `--color-text` |
| T8 | Contraste de texto secundario insuficiente — `#cccccc` sobre `#ffffff` (ratio ~1.6:1) | Baja visión | Perceptible | `css/styles.css` — variable `--color-text-muted` |
| T9 | Contraste de links en footer insuficiente — `#bbbbbb` sobre `#eeeeee` | Baja visión | Perceptible | `css/styles.css` — `.site-footer a` |

---

## `/` — index.html

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| H1 | Banner con animación `flash` parpadeante a 0.8s sin control de pausa ni `prefers-reduced-motion` | Fotosensibilidad | Operable | `.flash-banner` en `css/styles.css` |
| H2 | Primera imagen sin atributo `alt` — card de risotto | Visual total | Perceptible | `<img src="...risotto...">` |
| H3 | Segunda imagen con `alt="image2"` — genérico, sin descripción | Visual total | Perceptible | `<img alt="image2">` — card de salmón |
| H4 | Tercera imagen con `alt=""` incorrecto — la imagen es contenido informativo, no decorativa | Visual total | Perceptible | `<img alt="">` — card de tiramisú |
| H5 | Links de llamada a la acción sin contexto: "Click aquí", "Ver más", "Leer más", "Click aquí" | Visual total | Operable | `<a>` en hero y cards |
| H6 | Jerarquía de encabezados rota — salta de `<h1>` directamente a `<h4>` | Visual total | Comprensible | `<h4>Platos destacados</h4>`, `<h4>¿Por qué elegirnos?</h4>`, `<h4>Horarios</h4>` |
| H7 | Tabla de horarios sin `<caption>` | Visual total | Robusto | `<table>` de horarios |
| H8 | Tabla de horarios sin `<th>` — primera fila son `<td>` con estilo visual | Visual total | Robusto | Primera `<tr>` de la tabla |
| H9 | Tabla de horarios sin atributo `scope` en encabezados | Visual total | Robusto | Primera `<tr>` de la tabla |
| H10 | `<iframe>` sin atributo `title` | Visual total | Robusto | `<iframe src="about:blank">` |
| H11 | Botones "Click aquí" con padding de 2px × 6px — target de click < 24×24px | Motora parcial, Temblor | Operable | `.btn-sm` en `css/styles.css` |

---

## `/pages/about.html`

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| A1 | Imagen decorativa con `alt` de ~200 palabras — ruido excesivo para lector de pantalla | Visual total | Perceptible | `<img class="about-img">` |
| A2 | Imagen de texto (SVG inline con la cita del fundador) — no seleccionable, no escalable, `alt=""` vacío | Baja visión, Dislexia | Perceptible | `<img src="data:image/svg+xml...">` |
| A3 | Jerarquía de encabezados rota — `<h1>` → `<h3>` → `<h5>` sin pasar por h2 y h4 | Visual total | Comprensible | `<h3>Nuestros valores</h3>`, `<h5>` en cards |
| A4 | `<title>` duplicado "Inicio" — idéntico al de index.html | Visual total | Comprensible | `<head>` |
| A5 | Tabla de equipo sin `<th>`, sin `scope`, sin `<caption>` | Visual total | Robusto | `<table>` del equipo |
| A6 | Color verde (`#66bb6a`) y rojo (`#ef9a9a`) como único indicador del estado "activo/inactivo" del personal — sin texto alternativo | Daltonismo | Perceptible | Columna "Estado" en la tabla, símbolo `●` |
| A7 | Nota explicativa del color en fuente de 11px — debajo del ratio mínimo de tamaño legible | Baja visión | Perceptible | `<p style="font-size: 11px;">El color indica disponibilidad.</p>` |

---

## `/pages/contact.html`

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| C1 | Input de nombre sin `<label>` — solo `placeholder` (desaparece al escribir) | Visual total, Cognitiva | Robusto | `<input name="name" placeholder="Nombre completo">` |
| C2 | Input de email sin `<label>` | Visual total, Cognitiva | Robusto | `<input name="email" placeholder="Email">` |
| C3 | Input de teléfono sin `<label>` | Visual total, Cognitiva | Robusto | `<input name="phone" placeholder="Teléfono">` |
| C4 | Select de asunto sin `<label>` | Visual total, Cognitiva | Robusto | `<select name="subject">` |
| C5 | Textarea de mensaje sin `<label>` | Visual total, Cognitiva | Robusto | `<textarea name="message">` |
| C6 | Ningún campo indica que es obligatorio — sin `aria-required`, sin texto, sin asterisco explicado | Cognitiva | Comprensible | Todo el formulario |
| C7 | Errores de validación indicados solo por borde rojo (clase `.error`) — sin texto de error en el DOM | Daltonismo, Cognitiva | Perceptible | `css/styles.css` — `.error { border-color: #e57373 }` |
| C8 | Sin `aria-invalid` en campos con error | Visual total | Robusto | `js/main.js` — función `validateForm()` |
| C9 | Sin `aria-describedby` vinculando campos con sus mensajes de error | Visual total | Robusto | Todos los inputs |
| C10 | Al enviar con errores: foco no se mueve al primer campo inválido | Motora severa, Visual total | Operable | `js/main.js` — función `validateForm()` |
| C11 | Feedback de éxito mediante `alert()` nativo — no integrado en el DOM ni anunciado por lector de pantalla | Visual total | Robusto | `js/main.js` — `alert('Formulario enviado.')` |
| C12 | Sin región `aria-live` para anunciar resultados del envío | Visual total | Robusto | `<div id="contact-form-status">` — sin `aria-live` ni `role="status"` |
| C13 | Botón de envío con padding 2px × 8px — target de ~14px de alto, muy por debajo de los 44px recomendados | Motora parcial | Operable | `<button style="padding: 2px 8px">` |
| C14 | Link de email con texto "click aquí" sin contexto | Visual total | Operable | `<a href="mailto:...">click aquí</a>` |

---

## `/pages/reservation.html`

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| R1 | Calendario de fecha completamente custom — `role="presentation" aria-hidden="true"` — invisible para screen reader | Visual total | Robusto | `<div class="fake-calendar" aria-hidden="true">` |
| R2 | Días del calendario sin `tabindex` ni `role="button"` — inaccesibles con teclado | Motora severa | Operable | `<div onclick="selectDay(this)">` |
| R3 | Dropdown de horario solo se abre con `:hover` — no funciona con `Tab`, `Enter` ni flechas | Motora severa | Operable | `.time-picker:hover .time-picker-options` en `css/styles.css` |
| R4 | Valor seleccionado del calendario y dropdown guardado en `<input type="hidden">` — no legible por screen reader | Visual total | Robusto | `<input type="hidden" id="selected-date">`, `<input type="hidden" id="selected-time">` |
| R5 | Sin `<fieldset>` ni `<legend>` para agrupar campos relacionados | Visual total | Robusto | Todos los pasos del formulario |
| R6 | Formulario multi-paso sin indicador de progreso ("Paso 1 de 3") — ni visual ni para screen reader | Cognitiva | Comprensible | `<div class="step">` — sin `aria-label`, sin contador |
| R7 | Al cambiar de paso: sin `aria-live`, sin movimiento de foco — el screen reader no sabe que cambió el contenido | Visual total | Robusto | `js` — función `showStep()` |
| R8 | Todos los inputs sin `<label>` — solo `placeholder` | Visual total, Cognitiva | Robusto | Inputs en paso 1 |
| R9 | Timeout silencioso de 30 segundos — destruye el formulario sin advertencia previa, sin opción de extender | Cognitiva, Motora | Operable | `js/main.js` — `setTimeout(..., 30000)` |
| R10 | Feedback de confirmación mediante `alert()` — no integrado en el DOM | Visual total | Robusto | `js` — función `submitReservation()` |

---

## `/pages/menu.html`

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| M1 | Items del menú como `<div>` — sin `<ul>/<li>` ni `role="list"` | Visual total | Robusto | `.menu-div-item` — todos los platos |
| M2 | Precios solo en color verde (`#66bb6a`) sin label textual ("Precio:") ni `aria-label` | Daltonismo | Perceptible | `<div class="price-green">` |
| M3 | Botones de filtro como `<span>` — sin `role="button"`, sin `tabindex` | Motora severa, Visual total | Robusto | `<span class="filter-tag">` |
| M4 | Filtros sin `aria-pressed` — estado activo comunicado solo visualmente (clase `.active`) | Visual total | Robusto | `js` — filtros de menú |
| M5 | Cambio de resultados al filtrar sin `aria-live` — el screen reader no anuncia cuántos platos quedaron | Visual total | Robusto | `js` — evento `click` en `.filter-tag` |
| M6 | Tags de dieta solo con emoji `🌱` y `🌾` — sin texto alternativo para screen reader | Visual total | Perceptible | `<span class="menu-tag">🌱</span>` |
| M7 | Jerarquía de encabezados: aparece `<h3>` sin `<h2>` previo en la página | Visual total | Comprensible | `<h3>Entradas</h3>` etc. |
| M8 | Texto de descripción en 11px fijo — por debajo del mínimo legible recomendado (14px) | Baja visión | Perceptible | `.menu-div-desc { font-size: 11px }` |

---

## Resumen por discapacidad

| Discapacidad | Cantidad de problemas | IDs |
|---|---|---|
| Visual total | 31 | T4, T5, T6, H2, H3, H4, H5, H6, H7, H8, H9, H10, A1, A3, A4, A5, C1–C5, C8, C9, C10, C11, C12, C14, R1, R4, R5, R7, R10, M1, M4, M5, M7 |
| Baja visión | 7 | T3, T7, T8, T9, A2, A7, M8 |
| Daltonismo | 4 | T7, T8, A6, C7, M2 |
| Motora severa | 7 | T2, T5, R2, R3, C10, M3, R7 |
| Motora parcial / Temblor | 3 | H11, C13, T2 |
| Cognitiva | 7 | C1–C5, C6, C7, R6, R9 |
| Fotosensibilidad | 1 | H1 |

---

## Resumen por principio WCAG

| Principio | Cantidad |
|---|---|
| Perceptible | 14 |
| Operable | 9 |
| Comprensible | 8 |
| Robusto | 19 |

---

## Lo que el analizador debería reportar

```
frontend-02-no-accesible/index.html
  ❌ [T1]  Sin lang en <html>
  ❌ [T5]  Sin skip link
  ❌ [T6]  <title> no único ("Inicio")
  ❌ [H1]  Contenido parpadeante sin control (animation: flash)
  ❌ [H2]  <img> sin alt
  ❌ [H3]  alt genérico ("image2")
  ❌ [H5]  Links sin propósito ("click aquí", "ver más")
  ❌ [H6]  Jerarquía de encabezados rota (h1 → h4)
  ❌ [H7]  Tabla sin <caption>
  ❌ [H8]  Tabla sin <th>
  ❌ [H9]  Tabla sin scope
  ❌ [H10] <iframe> sin title
  ❌ [H11] Target de click < 24px

frontend-02-no-accesible/pages/about.html
  ❌ [A1]  Alt de imagen decorativa excesivamente largo (>200 palabras)
  ❌ [A2]  Texto embebido en imagen (no seleccionable)
  ❌ [A3]  Jerarquía rota (h1 → h3 → h5)
  ❌ [A5]  Tabla sin th/scope/caption
  ❌ [A6]  Color como único indicador de estado

frontend-02-no-accesible/pages/contact.html
  ❌ [C1–C5]  Inputs sin <label>
  ❌ [C6]     Campos requeridos sin indicación
  ❌ [C7]     Errores solo por color
  ❌ [C8]     Sin aria-invalid
  ❌ [C9]     Sin aria-describedby
  ❌ [C11]    Feedback con alert() — no en DOM
  ❌ [C12]    Sin aria-live
  ❌ [C13]    Target de botón < 24px

frontend-02-no-accesible/pages/reservation.html
  ❌ [R1]  Calendario con aria-hidden="true"
  ❌ [R2]  Días sin tabindex ni role=button
  ❌ [R3]  Dropdown solo con :hover
  ❌ [R5]  Sin fieldset/legend
  ❌ [R6]  Multi-paso sin indicador de progreso
  ❌ [R9]  Timeout sin advertencia (30s)

frontend-02-no-accesible/pages/menu.html
  ❌ [M1]  Items como <div> en vez de <ul><li>
  ❌ [M2]  Precios sin label textual
  ❌ [M3]  Filtros como <span> sin role=button
  ❌ [M4]  Sin aria-pressed en filtros
  ❌ [M5]  Sin aria-live al filtrar
  ❌ [M6]  Tags de dieta solo con emoji

css/styles.css (global)
  ❌ [T2]  outline: none !important
  ❌ [T3]  font-size fijo en px
  ❌ [T7]  Contraste texto principal insuficiente
  ❌ [T8]  Contraste texto secundario insuficiente
```
