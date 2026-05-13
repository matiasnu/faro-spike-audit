# Frontend 04 — Angular — No accesible

Este frontend es la **versión Angular con problemas de accesibilidad intencionales**.
Mismo stack que `frontend-03` pero sin ninguna de las prácticas accesibles.
Incluye problemas HTML/CSS clásicos **más** problemas exclusivos del framework Angular.

---

## Stack

- Angular 21 (standalone components)
- Sin `@angular/cdk/a11y`
- `FormsModule` (template-driven, sin validación accesible)
- Lazy loading por ruta (pero sin TitleStrategy ni focus management)

---

## Problemas introducidos

### Global — CSS / `src/index.html` / `app.ts` / `app.html`

| # | Problema | Discapacidad | WCAG | Archivo |
|---|---|---|---|---|
| G1 | `lang="en"` — idioma incorrecto, nunca actualizado | Visual total | Comprensible | `src/index.html` |
| G2 | `<title>` estático "Frontend04AngularNoAccesible" — no cambia entre rutas (sin `TitleStrategy`) | Visual total | Comprensible | `app.routes.ts` — sin `title:` en rutas |
| G3 | Sin `LiveAnnouncer` — los cambios de ruta no se anuncian al screen reader | Visual total | Robusto | `app.ts` |
| G4 | Sin focus management tras navegación — el foco queda en el link clickeado | Motora severa, Visual total | Operable | `app.ts` |
| G5 | Nav con `<div routerLink>` en vez de `<a routerLink>` — no son links reales | Motora severa, Visual total | Robusto | `app.html` |
| G6 | Sin landmarks semánticos — todo en `<div>` | Visual total | Robusto | `app.html` |
| G7 | Sin skip link | Motora severa | Operable | `app.html` |
| G8 | `outline: none !important` — foco completamente invisible | Motora severa | Operable | `styles.css` |
| G9 | `font-size: 13px` fijo — no escala con zoom del navegador | Baja visión | Perceptible | `styles.css` |
| G10 | Contraste insuficiente — `#999999` sobre `#ffffff` (ratio ~2.8:1) | Baja visión, Daltonismo | Perceptible | `styles.css` |

---

### `/` — Home (`pages/home/home.html`)

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| H1 | Banner parpadeante `animation: flash 0.8s infinite` sin control ni `prefers-reduced-motion` | Fotosensibilidad | Operable | `.flash-banner` en `styles.css` |
| H2 | Primera imagen sin `alt` | Visual total | Perceptible | `<img src="...risotto...">` |
| H3 | Segunda imagen con `alt="foto"` — genérico | Visual total | Perceptible | `<img alt="foto">` |
| H4 | Tercera imagen con `alt=""` incorrecto — contenido informativo | Visual total | Perceptible | `<img alt="">` |
| H5 | Links sin propósito: "Click aquí", "ver más", "leer más", "click aquí" | Visual total | Operable | `<a routerLink>` en hero y cards |
| H6 | Jerarquía rota — salta de `<h4>` a `<h2>` sin `<h1>` | Visual total | Comprensible | Secciones del template |
| H7 | Tabla sin `<caption>`, sin `<th>`, sin `scope` | Visual total | Robusto | `<table>` de horarios |
| H8 | `<iframe>` sin `title` | Visual total | Robusto | `<iframe src="about:blank">` |
| H9 | Targets de click pequeños (`.btn-sm`: 2px padding) | Motora parcial | Operable | `.btn-sm` en `styles.css` |

---

### `/about` — Nosotros (`pages/about/about.html`)

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| A1 | Imagen decorativa con `alt` de ~200 palabras — ruido para screen reader | Visual total | Perceptible | `<img>` principal |
| A2 | Imagen de texto (SVG inline) con `alt=""` — contenido clave no seleccionable ni escalable | Baja visión, Dislexia | Perceptible | `<img src="data:image/svg+xml...">` |
| A3 | Jerarquía rota: `<h1>` → `<h3>` → `<h5>` | Visual total | Comprensible | Encabezados del template |
| A4 | Tabla sin `<th>`, sin `scope`, sin `<caption>` | Visual total | Robusto | `<table>` del equipo |
| A5 | Color verde/rojo como único indicador de estado — sin texto alternativo | Daltonismo | Perceptible | Columna "Estado" — símbolo `●` |
| A6 | Sin breadcrumb ni indicación de página actual | Visual total | Comprensible | — |

---

### `/contact` — Contacto (`pages/contact/contact.html` + `contact.ts`)

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| C1 | Input de nombre sin `<label>` — solo `placeholder` | Visual total, Cognitiva | Robusto | `<input name="name">` |
| C2 | Input de email sin `<label>` | Visual total, Cognitiva | Robusto | `<input name="email">` |
| C3 | Input de teléfono sin `<label>` | Visual total, Cognitiva | Robusto | `<input name="phone">` |
| C4 | Select sin `<label>` | Visual total, Cognitiva | Robusto | `<select name="subject">` |
| C5 | Textarea sin `<label>` | Visual total, Cognitiva | Robusto | `<textarea name="message">` |
| C6 | Sin indicación de campos requeridos | Cognitiva | Comprensible | Todo el formulario |
| C7 | Errores solo por clase CSS `.error` (borde rojo) — sin texto | Daltonismo, Cognitiva | Perceptible | `contact.ts` — `onSubmit()` |
| C8 | Sin `aria-invalid` en campos inválidos | Visual total | Robusto | `contact.html` |
| C9 | Sin `aria-describedby` | Visual total | Robusto | Todos los inputs |
| C10 | Foco no se mueve al primer campo inválido al enviar | Motora severa, Visual total | Operable | `contact.ts` — `onSubmit()` |
| C11 | Mensaje de error con `aria-hidden="true"` — screen reader no lo puede leer | Visual total | Robusto | `contact.html` — `<p aria-hidden="true">` |
| C12 | Feedback de éxito con `alert()` nativo — no integrado en el DOM | Visual total | Robusto | `contact.ts` — `alert('Formulario enviado.')` |
| C13 | Botón con padding 2px — target de ~16px de alto | Motora parcial | Operable | `<button style="padding:2px 8px">` |

---

### `/reservation` — Reservas (`pages/reservation/reservation.html` + `reservation.ts`)

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| R1 | Calendario custom con `role="presentation" aria-hidden="true"` — invisible al screen reader | Visual total | Robusto | `<div role="presentation" aria-hidden="true">` |
| R2 | Días del calendario sin `tabindex` ni `role="button"` — inaccesibles con teclado | Motora severa | Operable | `<div (click)="selectedDate = ...">` |
| R3 | Dropdown de hora solo con CSS `:hover` — no funciona con teclado | Motora severa | Operable | `.hover-dropdown:hover` en `styles.css` |
| R4 | Valores de fecha y hora en `<input type="hidden">` — no anunciados | Visual total | Robusto | `[(ngModel)]="selectedDate"` en hidden inputs |
| R5 | Formulario multi-paso sin indicador de progreso ("Paso 1 de 3") | Cognitiva | Comprensible | `@if (currentStep() === N)` sin contexto |
| R6 | Cambio de paso sin `aria-live` ni movimiento de foco | Visual total | Robusto | `reservation.ts` — `nextStep()` / `prevStep()` |
| R7 | Todos los inputs sin `<label>` — solo `placeholder` | Visual total, Cognitiva | Robusto | Inputs del paso 1 |
| R8 | Timeout de 30s silencioso — destruye el formulario sin advertencia | Cognitiva, Motora | Operable | `reservation.ts` — `ngOnInit()` / `setTimeout` |
| R9 | Feedback de confirmación con `alert()` — no en DOM | Visual total | Robusto | `reservation.ts` — `submit()` |

---

### `/menu` — Menú (`pages/menu/menu.html` + `menu.ts`)

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| M1 | Items como `<div>` — sin `<ul>/<li>` ni `role="list"` | Visual total | Robusto | `.menu-div-item` |
| M2 | Precios solo en color verde — sin `aria-label` ni texto "Precio:" | Daltonismo | Perceptible | `.price-green` |
| M3 | Filtros como `<span>` — sin `role="button"` ni `tabindex` | Motora severa, Visual total | Robusto | `<span class="filter-tag">` |
| M4 | Sin `aria-pressed` en filtros | Visual total | Robusto | `menu.html` — `[class.active]` solo visual |
| M5 | Sin anuncio al filtrar (sin `LiveAnnouncer`) | Visual total | Robusto | `menu.ts` — `setFilter()` |
| M6 | Tags de dieta solo con emoji `🌱` `🌾` — sin texto alternativo | Visual total | Perceptible | `<span>{{ tag === 'vegan' ? '🌱' : '🌾' }}</span>` |

---

## Resumen por discapacidad

| Discapacidad | Cantidad | IDs |
|---|---|---|
| Visual total | 29 | G1–G7, H2–H6, H8, A1, A3, A4, A6, C1–C5, C8–C12, R1, R4, R6, R7, R9, M1, M4, M5 |
| Baja visión | 4 | G9, G10, A2, M2 |
| Daltonismo | 4 | G10, A5, C7, M2 |
| Motora severa | 8 | G4, G5, G7, G8, R2, R3, M3, C10 |
| Motora parcial | 2 | H9, C13 |
| Cognitiva | 7 | C1–C6, R5, R7, R8 |
| Fotosensibilidad | 1 | H1 |

## Problemas exclusivos de Angular (no detectables en HTML estático)

| ID | Problema | Por qué es Angular-específico |
|---|---|---|
| G2 | Sin `TitleStrategy` — `<title>` estático | En SPA el `<title>` no cambia solo con la URL; requiere un `TitleStrategy` activo |
| G3 | Sin `LiveAnnouncer` | Las SPAs navegan sin recargar la página — el screen reader no detecta el cambio sin un anuncio explícito |
| G4 | Sin focus management tras `NavigationEnd` | El router de Angular navega silenciosamente; el foco debe moverse programáticamente |
| G5 | `<div routerLink>` como navegación | Parece funcionar visualmente, pero no es un `<a>` — sin rol link, sin navegación por teclado |
| R6 | Cambio de paso sin aria-live | `@if` Angular oculta/muestra contenido sin que el screen reader lo sepa |
| R8 | Timeout en `ngOnInit` sin aviso | El formulario desaparece sin ningún anuncio accesible (`aria-live`) |

---

## Lo que el analizador debería reportar

```
frontend-04-angular-no-accesible/src/index.html                   ❌ [G1] lang incorrecto
frontend-04-angular-no-accesible/src/app/app.ts                    ❌ [G2] sin TitleStrategy
                                                                   ❌ [G3] sin LiveAnnouncer
                                                                   ❌ [G4] sin focus management
frontend-04-angular-no-accesible/src/app/app.html                  ❌ [G5] div routerLink
                                                                   ❌ [G6] sin landmarks
                                                                   ❌ [G7] sin skip link
frontend-04-angular-no-accesible/src/styles.css                    ❌ [G8] outline: none
                                                                   ❌ [G9] font-size fijo
                                                                   ❌ [G10] contraste bajo
frontend-04-angular-no-accesible/.../pages/home/home.html          ❌ [H1] banner parpadeante
                                                                   ❌ [H2] img sin alt
                                                                   ❌ [H3] alt genérico
                                                                   ❌ [H5] links sin propósito
                                                                   ❌ [H6] jerarquía rota
                                                                   ❌ [H7] tabla sin th/caption
                                                                   ❌ [H8] iframe sin title
frontend-04-angular-no-accesible/.../pages/about/about.html        ❌ [A1] alt excesivo
                                                                   ❌ [A2] texto en imagen
                                                                   ❌ [A3] jerarquía rota
                                                                   ❌ [A4] tabla sin th
                                                                   ❌ [A5] color como único indicador
frontend-04-angular-no-accesible/.../pages/contact/contact.html    ❌ [C1–C5] inputs sin label
                                                                   ❌ [C7] error solo por color
                                                                   ❌ [C11] aria-hidden en error
                                                                   ❌ [C13] target pequeño
frontend-04-angular-no-accesible/.../pages/reservation/reservation.html ❌ [R1] aria-hidden en calendario
                                                                   ❌ [R2] días sin tabindex
                                                                   ❌ [R3] dropdown solo hover
                                                                   ❌ [R5] sin progreso multi-paso
frontend-04-angular-no-accesible/.../pages/menu/menu.html          ❌ [M1] items como div
                                                                   ❌ [M2] precio sin label
                                                                   ❌ [M3] filtros como span
                                                                   ❌ [M4] sin aria-pressed
                                                                   ❌ [M6] tags solo emoji
```
