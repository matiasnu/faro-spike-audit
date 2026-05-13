# Principio 4: Robusto

> ¿Lo entienden las tecnologías asistivas?

| Problema | Discapacidad afectada |
|---|---|
| HTML inválido / mal anidado | Visual total (lector de pantalla) |
| Sin landmarks (`<main>`, `<nav>`, `<header>`, `<footer>`) | Visual total |
| `<div>` y `<span>` como botones sin `role` ni `tabindex` | Visual total, motora |
| `aria-label` vacío o incorrecto | Visual total |
| `aria-hidden="true"` en contenido importante | Visual total |
| `role` incorrecto para el elemento | Visual total |
| Estado de widget no comunicado (`aria-expanded`, `aria-checked`) | Visual total |
| `<iframe>` sin `title` | Visual total |
| Tabla sin `<th>` ni `scope` | Visual total |
| Form sin `<fieldset>` / `<legend>` en grupos | Visual total |
| Mensajes de estado no anunciados (sin `aria-live`) | Visual total |
| `<select>` reemplazado por divs sin ARIA completo | Visual total, motora |
