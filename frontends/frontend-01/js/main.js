// Nav mobile toggle
const navToggle = document.getElementById('nav-toggle');
const navMenu = document.getElementById('nav-menu');

if (navToggle && navMenu) {
  navToggle.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', isOpen);
    navToggle.textContent = isOpen ? '✕ Cerrar' : '☰ Menú';
  });
}

// Validación de formularios accesible
function setupForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return;

  const statusRegion = document.getElementById(`${formId}-status`);

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const fields = form.querySelectorAll('[data-required]');
    let firstError = null;

    fields.forEach((field) => {
      const errorEl = document.getElementById(`${field.id}-error`);
      const isEmpty = field.value.trim() === '';
      const isInvalid = isEmpty || (field.type === 'email' && !field.value.includes('@'));

      if (isInvalid) {
        field.setAttribute('aria-invalid', 'true');
        if (errorEl) {
          errorEl.textContent = isEmpty
            ? 'Este campo es obligatorio.'
            : 'Por favor ingresá un correo electrónico válido.';
          errorEl.setAttribute('aria-live', 'polite');
          errorEl.style.display = 'block';
        }
        if (!firstError) firstError = field;
      } else {
        field.setAttribute('aria-invalid', 'false');
        if (errorEl) {
          errorEl.textContent = '';
          errorEl.removeAttribute('aria-live');
          errorEl.style.display = 'none';
        }
      }
    });

    if (firstError) {
      firstError.focus();
      return;
    }

    if (statusRegion) {
      statusRegion.textContent = '¡Mensaje enviado con éxito! Nos pondremos en contacto pronto.';
      statusRegion.className = 'alert alert-success';
      statusRegion.removeAttribute('hidden');
      statusRegion.focus();
    }

    form.reset();
  });

  // Limpiar errores al corregir el campo
  form.querySelectorAll('input, textarea, select').forEach((field) => {
    field.addEventListener('input', () => {
      const errorEl = document.getElementById(`${field.id}-error`);
      if (field.value.trim() !== '') {
        field.setAttribute('aria-invalid', 'false');
        if (errorEl) {
          errorEl.textContent = '';
          errorEl.style.display = 'none';
        }
      }
    });
  });
}

setupForm('contact-form');
setupForm('reservation-form');
