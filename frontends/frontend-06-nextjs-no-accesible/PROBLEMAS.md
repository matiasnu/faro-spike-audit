# Frontend 06 — Next.js — No accesible

Versión Next.js con **problemas de accesibilidad intencionales**.
Incluye problemas HTML/CSS clásicos + problemas exclusivos de Next.js/SSR.

## Stack

- Next.js 16 (App Router)
- Server Components con HTML inaccesible
- Client Components (`'use client'`) sin ARIA
- TypeScript

---

## Problemas introducidos

### Global — CSS / `layout.tsx` / `BadNav.tsx`

| # | Problema | Discapacidad | WCAG | Archivo |
|---|---|---|---|---|
| G1 | `lang="en"` incorrecto — el idioma real es español | Visual total | Comprensible | `layout.tsx` |
| G2 | Sin `metadata.title` por ruta — `<title>` siempre igual para todas las páginas | Visual total | Comprensible | `layout.tsx` — sin template, sin `generateMetadata` en pages |
| G3 | Sin `RouteAnnouncer` — cambios de ruta completamente silenciosos para screen reader | Visual total | Robusto | `layout.tsx` — Next.js App Router no anuncia navegación por defecto |
| G4 | Sin skip link | Motora severa | Operable | `layout.tsx` |
| G5 | Sin landmarks: `<div>` en lugar de `<header>`, `<main>`, `<nav>`, `<footer>` | Visual total | Robusto | `layout.tsx` |
| G6 | Nav con `<div onClick>` para "Nosotros" y "Menú" — no son links reales | Motora severa, Visual total | Robusto | `BadNav.tsx` |
| G7 | Sin `aria-current` en ningún ítem de la nav | Visual total | Comprensible | `BadNav.tsx` |
| G8 | `outline: none !important` global — foco invisible | Motora severa | Operable | `globals.css` |
| G9 | `font-size: 13px` fijo — no escala con preferencias del navegador | Baja visión | Perceptible | `globals.css` |
| G10 | Contraste insuficiente — `#999999` sobre `#ffffff` (ratio ~2.8:1) | Baja visión, Daltonismo | Perceptible | `globals.css` |

---

### `/` — Home (`app/page.tsx`) — Server Component

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| H1 | Banner parpadeante `animation: flash 0.8s infinite` sin `prefers-reduced-motion` | Fotosensibilidad | Operable | `.flash-banner` |
| H2 | Primera imagen sin atributo `alt` | Visual total | Perceptible | `<img src="...risotto...">` |
| H3 | Segunda imagen con `alt="foto"` genérico | Visual total | Perceptible | `<img alt="foto">` |
| H4 | Tercera imagen con `alt=""` incorrecto (contenido informativo) | Visual total | Perceptible | `<img alt="">` |
| H5 | Links sin propósito: "Click aquí", "ver más", "leer más", "click aquí" | Visual total | Operable | `<Link>` en hero y cards |
| H6 | Jerarquía rota — solo `<h4>` y `<h2>`, sin `<h1>` como primer encabezado | Visual total | Comprensible | `page.tsx` |
| H7 | Tabla de horarios sin `<caption>`, sin `<th>`, sin `scope` | Visual total | Robusto | `<table>` en `page.tsx` |
| H8 | `<iframe>` sin atributo `title` | Visual total | Robusto | `<iframe src="about:blank">` |
| H9 | Targets de link con `.btn-sm` — padding 2px, < 24px de alto | Motora parcial | Operable | `.btn-sm` en `globals.css` |

---

### `/about` — Nosotros (`app/about/page.tsx`) — Server Component

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| A1 | Imagen decorativa con `alt` de ~200 palabras — ruido para screen reader | Visual total | Perceptible | `<img>` principal |
| A2 | Imagen de texto (SVG inline) con `alt=""` — contenido clave no accesible | Baja visión, Dislexia | Perceptible | `<img src="data:image/svg+xml...">` |
| A3 | Jerarquía rota: `<h1>` → `<h3>` → `<h5>` | Visual total | Comprensible | Encabezados del page |
| A4 | Tabla sin `<th>`, sin `scope`, sin `<caption>` | Visual total | Robusto | `<table>` del equipo |
| A5 | Color verde/rojo como único indicador de estado — sin texto alternativo | Daltonismo | Perceptible | Columna "Estado" — símbolo `●` |
| A6 | Sin breadcrumb ni indicación de página actual | Visual total | Comprensible | — |

---

### `/contact` — Contacto (`BadContactForm.tsx`) — Client Component

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| C1 | Input de nombre sin `<label>` — solo `placeholder` | Visual total, Cognitiva | Robusto | `<input placeholder="Nombre completo">` |
| C2 | Input de email sin `<label>` | Visual total, Cognitiva | Robusto | `<input placeholder="Email">` |
| C3 | Input de teléfono sin `<label>` | Visual total, Cognitiva | Robusto | `<input placeholder="Teléfono">` |
| C4 | Select sin `<label>` | Visual total, Cognitiva | Robusto | `<select>` |
| C5 | Textarea sin `<label>` | Visual total, Cognitiva | Robusto | `<textarea>` |
| C6 | Errores solo por clase `.error` (borde rojo) — sin texto | Daltonismo, Cognitiva | Perceptible | `BadContactForm.tsx` — `className={hasErrors && !name ? 'error' : ''}` |
| C7 | Sin `aria-invalid` en campos inválidos | Visual total | Robusto | `BadContactForm.tsx` |
| C8 | Sin `aria-describedby` | Visual total | Robusto | Todos los inputs |
| C9 | Mensaje de error con `aria-hidden="true"` — screen reader no lo lee | Visual total | Robusto | `<p aria-hidden="true">Hay campos incompletos.</p>` |
| C10 | Foco no se mueve al primer campo inválido al enviar | Motora severa, Visual total | Operable | `BadContactForm.tsx` — `handleSubmit` |
| C11 | Feedback de éxito con `alert()` — no integrado en el DOM | Visual total | Robusto | `BadContactForm.tsx` — `alert('Formulario enviado.')` |
| C12 | Botón con padding 2px — target de ~16px de alto | Motora parcial | Operable | `<button style="padding: 2px 8px">` |
| C13 | Link de email con texto "click aquí" | Visual total | Operable | `<a>click aquí</a>` |

---

### `/reservation` — Reservas (`BadReservationForm.tsx`) — Client Component

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| R1 | Calendario custom con `role="presentation" aria-hidden="true"` — invisible al screen reader | Visual total | Robusto | `<div role="presentation" aria-hidden="true">` |
| R2 | Días del calendario sin `tabindex` ni `role="button"` — inaccesibles con teclado | Motora severa | Operable | `<div onClick={() => setSelectedDate(...)}` |
| R3 | Dropdown de hora solo con CSS `:hover` — no funciona con teclado | Motora severa | Operable | `.hover-dropdown:hover` en `globals.css` |
| R4 | Multi-paso sin indicador de progreso ("Paso 1 de 3") | Cognitiva | Comprensible | `BadReservationForm.tsx` — `{step === N && ...}` sin contexto |
| R5 | Cambio de paso sin `aria-live` ni movimiento de foco | Visual total | Robusto | `BadReservationForm.tsx` — `setStep()` |
| R6 | Todos los inputs sin `<label>` — solo `placeholder` | Visual total, Cognitiva | Robusto | Inputs del paso 1 |
| R7 | Timeout de 30s silencioso — destruye el formulario sin advertencia | Cognitiva, Motora | Operable | `BadReservationForm.tsx` — `useEffect → setTimeout → setExpired(true)` |
| R8 | Feedback de confirmación con `alert()` — no en el DOM | Visual total | Robusto | `BadReservationForm.tsx` — `alert('Reserva enviada.')` |

---

### `/menu` — Menú (`BadMenuFilters.tsx`) — Client Component

| # | Problema | Discapacidad | WCAG | Elemento |
|---|---|---|---|---|
| M1 | Items como `<div>` — sin `<ul>/<li>` ni `role="list"` | Visual total | Robusto | `.menu-div-item` |
| M2 | Precios solo en color verde — sin `aria-label` ni texto "Precio:" | Daltonismo | Perceptible | `.price-green` |
| M3 | Filtros como `<span>` sin `role="button"` ni `tabindex` | Motora severa, Visual total | Robusto | `<span className="filter-tag">` |
| M4 | Sin `aria-pressed` en filtros — estado activo solo visual | Visual total | Robusto | `BadMenuFilters.tsx` — `className={filter === f ? 'active' : ''}` |
| M5 | Sin `aria-live` al filtrar — el screen reader no sabe cuántos resultados hay | Visual total | Robusto | `BadMenuFilters.tsx` — `setFilter()` |
| M6 | Tags de dieta solo con emoji `🌱` `🌾` — sin texto alternativo | Visual total | Perceptible | `<span>{t === 'vegan' ? '🌱' : '🌾'}</span>` |

---

## Problemas exclusivos de Next.js/SSR

| ID | Problema | Por qué es Next.js-específico |
|---|---|---|
| G2 | Sin `generateMetadata` — `<title>` estático para todas las rutas | En Next.js App Router el título no cambia entre rutas sin `export const metadata` o `generateMetadata` en cada `page.tsx` |
| G3 | Sin `RouteAnnouncer` | Next.js App Router eliminó el anunciador de rutas built-in que tenía Pages Router. Sin un componente custom con `usePathname + aria-live`, el screen reader no detecta la navegación |
| G6 | `<div onClick>` como nav en Client Component | Patrón frecuente en Next.js cuando se mezclan Server y Client Components sin pensar en semántica |
| R5 | `useState` para paso sin `aria-live` | `{step === N && <form>}` oculta/muestra con React sin que el screen reader lo detecte |
| R7 | `useEffect + setTimeout` como timeout silencioso | El formulario desaparece sin ningún anuncio accesible — patrón fácil de introducir en Client Components |

---

## Resumen por discapacidad

| Discapacidad | Cantidad | IDs |
|---|---|---|
| Visual total | 30 | G1–G5, G7, H2–H6, H8, A1, A3, A4, A6, C1–C5, C7–C11, C13, R1, R4, R5, R6, R8, M1, M4, M5 |
| Baja visión | 4 | G9, G10, A2, M2 |
| Daltonismo | 4 | G10, A5, C6, M2 |
| Motora severa | 7 | G4, G6, G8, R2, R3, M3, C10 |
| Motora parcial | 2 | H9, C12 |
| Cognitiva | 6 | C1–C6, R4, R6, R7 |
| Fotosensibilidad | 1 | H1 |

---

## Lo que el analizador debería reportar

```
frontend-06-nextjs-no-accesible/src/app/layout.tsx        ❌ [G1] lang="en" incorrecto
                                                           ❌ [G2] sin metadata.title por ruta
                                                           ❌ [G3] sin RouteAnnouncer
                                                           ❌ [G4] sin skip link
                                                           ❌ [G5] sin landmarks
frontend-06-nextjs-no-accesible/src/components/BadNav.tsx ❌ [G6] div onClick como nav
                                                           ❌ [G7] sin aria-current
frontend-06-nextjs-no-accesible/src/app/globals.css       ❌ [G8] outline: none
                                                           ❌ [G9] font-size fijo
                                                           ❌ [G10] contraste bajo
frontend-06-nextjs-no-accesible/src/app/page.tsx          ❌ [H1–H9]
frontend-06-nextjs-no-accesible/src/app/about/page.tsx    ❌ [A1–A6]
frontend-06-nextjs-no-accesible/src/components/BadContactForm.tsx  ❌ [C1–C13]
frontend-06-nextjs-no-accesible/src/components/BadReservationForm.tsx ❌ [R1–R8]
frontend-06-nextjs-no-accesible/src/components/BadMenuFilters.tsx  ❌ [M1–M6]
```
