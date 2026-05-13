// FRONTEND-02 — INTENCIONALMENTE NO ACCESIBLE
//
// Problemas en este archivo:
// [Visual total]   validación solo cambia clases CSS (color), sin texto de error ni aria
// [Visual total]   éxito/error no se anuncia — sin aria-live ni focus
// [Cognitiva]      no se limpian errores al corregir campos
// [Motora severa]  filtros de menú sin aria-pressed
// [Visual total]   nav mobile no actualiza aria-expanded

const navToggle = document.getElementById('nav-toggle');
const navMenu = document.getElementById('nav-menu');

if (navToggle && navMenu) {
  navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('open');
    // No actualiza aria-expanded
  });
}

function validateForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const inputs = form.querySelectorAll('input, textarea, select');
    let hasError = false;

    inputs.forEach((input) => {
      // Solo agrega clase visual — sin texto de error, sin aria-invalid
      if (!input.value.trim()) {
        input.classList.add('error');
        hasError = true;
      } else {
        input.classList.remove('error');
      }
    });

    if (!hasError) {
      // Muestra un alert del navegador — no integrado en el DOM accesiblemente
      alert('Formulario enviado.');
      form.reset();
    }
    // Si hay errores: no hay feedback, no se mueve el foco, no hay mensaje
  });
}

validateForm('contact-form');
validateForm('reservation-form');

// Filtros sin aria-pressed
document.querySelectorAll('.filter-tag').forEach((tag) => {
  tag.addEventListener('click', () => {
    document.querySelectorAll('.filter-tag').forEach((t) => t.classList.remove('active'));
    tag.classList.add('active');
    // No actualiza aria-pressed ni aria-selected
    // No anuncia el cambio a lectores de pantalla
  });
});

// Timeout silencioso — sin advertencia al usuario
setTimeout(() => {
  const form = document.getElementById('reservation-form');
  if (form) {
    form.innerHTML = '<p style="color:#ccc;font-size:12px;">La sesión expiró. Recargá la página.</p>';
    // No avisa antes, no ofrece extender, no anuncia con aria-live
  }
}, 30000);
