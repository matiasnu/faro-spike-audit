# Frontend 03 — Angular — Accesible

Este frontend es la **línea base accesible en Angular 21** (standalone components, lazy loading).
No tiene problemas de accesibilidad intencionales.
Sirve como referencia para que el analizador pueda reportar `✅` en cada check.

---

## Stack

- Angular 21 (standalone components)
- `@angular/cdk/a11y` — `LiveAnnouncer`
- `ReactiveFormsModule`
- Lazy loading por ruta

---

## Qué tiene bien

### Global — `app.ts` / `app.html` / `app.config.ts`

| Check | Implementación |
|---|---|
| `lang="es"` en `<html>` | `src/index.html` |
| `<title>` único por ruta | `PageTitleStrategy` en `app.config.ts` — genera "Inicio — El Sauce", "Menú — El Sauce", etc. |
| Anuncio de cambio de ruta al screen reader | `LiveAnnouncer.announce()` en `app.ts` tras cada `NavigationEnd` |
| Foco movido a `<main>` tras cada navegación | `setTimeout → main.focus()` en `app.ts` |
| Skip link "Saltar al contenido principal" | Primer elemento de `app.html` |
| Landmarks semánticos | `<header role="banner">`, `<main id="main-content">`, `<footer role="contentinfo">` |
| Nav con `<a routerLink>` | No `<div routerLink>` — los ítems son links reales |
| `aria-current="page"` en nav activo | `ariaCurrentWhenActive="page"` en cada `routerLinkActive` |
| Foco visible | `:focus-visible` con `outline: 3px solid #005fcc` — nunca oculto |
| Fuente escalable | `font-size: 100%` en `html`, unidades `rem` |
| Contraste suficiente | Texto `#1a1a1a` sobre `#ffffff` (ratio ~19:1) |
| `prefers-reduced-motion` | Desactiva animaciones y transiciones |

### `/` — Home (`pages/home/`)

| Check | Detalle |
|---|---|
| `h1` como primer encabezado | "Bienvenidos a El Sauce" |
| Jerarquía `h1` → `h2` → `h3` | — |
| Imágenes con `alt` descriptivo | Tres platos con alt completo |
| Links con propósito claro | "Reservar una mesa", "Ver nuestro menú", "Ver en el menú" |
| Tabla de horarios con `<caption>` y `<th scope="col">` | Renderizada con `@for` |

### `/about` — Nosotros (`pages/about/`)

| Check | Detalle |
|---|---|
| Breadcrumb con `aria-label` y `aria-current="page"` | — |
| Imagen con `alt` descriptivo y proporcional | — |
| Tabla de equipo con `<caption>` y `<th scope="col">` | Renderizada con `@for` |
| Jerarquía correcta `h1` → `h2` → `h3` | — |

### `/contact` — Contacto (`pages/contact/`)

| Check | Detalle |
|---|---|
| `ReactiveFormsModule` con validación | `Validators.required`, `Validators.email` |
| Todos los inputs con `<label>` | `for` ↔ `id` en cada campo |
| `aria-required="true"` y `*` con `<abbr>` | — |
| `[attr.aria-invalid]` dinámico | Se activa solo cuando el campo fue tocado y es inválido |
| `[attr.aria-describedby]` | Apunta al span de error o al hint según el estado |
| Mensaje de error con `role="alert"` | Texto descriptivo, no solo color |
| Foco movido al primer campo inválido | `document.querySelector('[aria-invalid="true"]')?.focus()` |
| Feedback de envío con `role="status" aria-live="polite"` | `@if (submitted())` con región live |
| Botón con `min-height: 44px` | Global en `styles.css` |

### `/reservation` — Reservas (`pages/reservation/`)

| Check | Detalle |
|---|---|
| `<fieldset>` + `<legend>` para grupos | "Datos de contacto" / "Detalles de la reserva" |
| Input de fecha nativo `<input type="date">` | Accesible con teclado y screen reader |
| Selector de hora con `<select>` nativo | Con `<optgroup>` |
| Validación accesible igual que `/contact` | `aria-invalid`, `role="alert"`, foco en error |
| Feedback de envío con `aria-live` | — |

### `/menu` — Menú (`pages/menu/`)

| Check | Detalle |
|---|---|
| Items como `<ul role="list"><li>` | Lista semántica |
| Precios con `[attr.aria-label]="'Precio: ' + dish.price"` | No depende solo del color |
| Filtros con `[attr.aria-pressed]` | Estado comunicado al screen reader |
| `LiveAnnouncer` al filtrar | Anuncia "Mostrando veganos: 4 resultados" |
| Tags de dieta con texto | "Vegano" / "Sin gluten" — no solo emoji |

---

## Lo que el analizador debería reportar

```
frontend-03-angular-accesible/src/index.html                → sin errores
frontend-03-angular-accesible/src/app/app.html              → sin errores
frontend-03-angular-accesible/src/app/pages/home/home.html  → sin errores
frontend-03-angular-accesible/src/app/pages/about/about.html    → sin errores
frontend-03-angular-accesible/src/app/pages/contact/contact.html → sin errores
frontend-03-angular-accesible/src/app/pages/reservation/reservation.html → sin errores
frontend-03-angular-accesible/src/app/pages/menu/menu.html  → sin errores
```
