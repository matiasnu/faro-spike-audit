# Frontend 05 — Next.js — Accesible

Línea base accesible en **Next.js 16 con App Router**.
Sin problemas de accesibilidad intencionales.

## Stack

- Next.js 16 (App Router)
- Server Components para páginas estáticas
- Client Components (`'use client'`) para interactividad
- TypeScript

---

## Qué tiene bien

### Global — `layout.tsx` / `RouteAnnouncer.tsx` / `Nav.tsx`

| Check | Implementación |
|---|---|
| `lang="es"` en `<html>` | `layout.tsx` |
| `<title>` único por ruta | `metadata.title` con template `'%s — El Sauce'` en `layout.tsx` + `export const metadata` en cada `page.tsx` |
| Anuncio de cambio de ruta | `RouteAnnouncer.tsx` — Client Component con `usePathname` + `aria-live="assertive"` — Next.js App Router no lo hace por defecto |
| Skip link | `layout.tsx` — primer elemento del body |
| Landmarks semánticos | `<header role="banner">`, `<main id="main-content">`, `<footer role="contentinfo">` |
| Nav con `<Link>` semánticos | `Nav.tsx` — Client Component con `usePathname` para `aria-current="page"` |
| Foco visible | `:focus-visible` con outline, nunca oculto |
| Fuente escalable | `font-size: 100%` en html, unidades rem |
| Contraste suficiente | `#1a1a1a` sobre `#ffffff` |
| `prefers-reduced-motion` | Desactiva animaciones y transiciones |

### Server Components (páginas)

| Check | Página | Detalle |
|---|---|---|
| `generateMetadata` | Todas | "Inicio", "Nosotros", "Menú", "Reservas", "Contacto" |
| Jerarquía `h1→h2→h3` | Todas | Sin saltos |
| Imágenes con `alt` descriptivo | `/`, `/about` | — |
| Tabla con `<caption>` y `<th scope="col">` | `/`, `/about` | — |
| Breadcrumb con `aria-label` y `aria-current` | `/about`, `/menu`, `/contact`, `/reservation` | — |
| `<abbr title="obligatorio">*</abbr>` | `/contact`, `/reservation` | — |

### Client Components

| Check | Componente | Detalle |
|---|---|---|
| `aria-invalid` dinámico | `ContactForm`, `ReservationForm` | Se activa solo al tocar el campo |
| `aria-describedby` | `ContactForm`, `ReservationForm` | Apunta a hint o error según estado |
| `role="alert"` en errores | Ambos forms | Texto descriptivo, no solo color |
| Foco en primer campo inválido | Ambos forms | `querySelector('[aria-invalid="true"]')?.focus()` |
| `role="status" aria-live="polite"` | Ambos forms | Feedback de envío en el DOM |
| `<fieldset>/<legend>` | `ReservationForm` | Agrupa campos relacionados |
| `<select>` nativo con `<optgroup>` | `ReservationForm` | Selector de horario accesible con teclado |
| `aria-pressed` en filtros | `MenuFilters` | Estado comunicado al screen reader |
| `aria-live` al filtrar | `MenuFilters` | Anuncia "Mostrando veganos: 4 resultados" |
| `aria-label` en precios | `MenuFilters` | "Precio: $5.800" |
| Items de menú como `<ul><li>` | `MenuFilters` | Lista semántica |

---

## Lo que el analizador debería reportar

```
frontend-05-nextjs-accesible → sin errores detectados en todas las rutas
```
