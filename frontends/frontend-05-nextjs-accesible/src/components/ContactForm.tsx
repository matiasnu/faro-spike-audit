'use client';

import { useState, useRef } from 'react';

interface FieldError { name?: string; email?: string; subject?: string; message?: string; }

export default function ContactForm() {
  const [submitted, setSubmitted] = useState(false);
  const [errors, setErrors] = useState<FieldError>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});
  const successRef = useRef<HTMLDivElement>(null);

  function validate(data: FormData): FieldError {
    const e: FieldError = {};
    if (!data.get('name')) e.name = 'Este campo es obligatorio.';
    const email = data.get('email') as string;
    if (!email) e.email = 'Este campo es obligatorio.';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) e.email = 'Ingresá un correo electrónico válido.';
    if (!data.get('subject')) e.subject = 'Este campo es obligatorio.';
    if (!data.get('message')) e.message = 'Este campo es obligatorio.';
    return e;
  }

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    const errs = validate(data);
    setTouched({ name: true, email: true, subject: true, message: true });
    setErrors(errs);

    if (Object.keys(errs).length > 0) {
      const firstInvalid = e.currentTarget.querySelector('[aria-invalid="true"]') as HTMLElement;
      firstInvalid?.focus();
      return;
    }
    setSubmitted(true);
    setTimeout(() => successRef.current?.focus(), 50);
  }

  if (submitted) {
    return (
      <div ref={successRef} className="alert alert-success" role="status" aria-live="polite" tabIndex={-1}>
        ¡Mensaje enviado con éxito! Nos pondremos en contacto pronto.
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} noValidate style={{ maxWidth: 600 }}>
      <div className="form-group">
        <label htmlFor="contact-name">
          Nombre completo <span className="required-mark" aria-hidden="true">*</span>
        </label>
        <input id="contact-name" type="text" name="name" autoComplete="name"
          aria-required="true"
          aria-invalid={touched.name && !!errors.name ? 'true' : undefined}
          aria-describedby={touched.name && errors.name ? 'contact-name-error' : undefined}
          onBlur={() => setTouched(t => ({ ...t, name: true }))}
        />
        {touched.name && errors.name && (
          <span className="field-error" id="contact-name-error" role="alert">{errors.name}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="contact-email">
          Correo electrónico <span className="required-mark" aria-hidden="true">*</span>
        </label>
        <input id="contact-email" type="email" name="email" autoComplete="email"
          aria-required="true"
          aria-invalid={touched.email && !!errors.email ? 'true' : undefined}
          aria-describedby={touched.email && errors.email ? 'contact-email-error' : 'contact-email-hint'}
          onBlur={() => setTouched(t => ({ ...t, email: true }))}
        />
        <span className="form-hint" id="contact-email-hint">Ejemplo: nombre@correo.com</span>
        {touched.email && errors.email && (
          <span className="field-error" id="contact-email-error" role="alert">{errors.email}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="contact-phone">Teléfono (opcional)</label>
        <input id="contact-phone" type="tel" name="phone" autoComplete="tel" />
      </div>

      <div className="form-group">
        <label htmlFor="contact-subject">
          Asunto <span className="required-mark" aria-hidden="true">*</span>
        </label>
        <select id="contact-subject" name="subject"
          aria-required="true"
          aria-invalid={touched.subject && !!errors.subject ? 'true' : undefined}
          onBlur={() => setTouched(t => ({ ...t, subject: true }))}
        >
          <option value="">— Seleccioná un asunto —</option>
          <option value="reservation">Consulta sobre reservas</option>
          <option value="event">Eventos y celebraciones</option>
          <option value="feedback">Comentarios sobre tu visita</option>
          <option value="other">Otro</option>
        </select>
        {touched.subject && errors.subject && (
          <span className="field-error" role="alert">{errors.subject}</span>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="contact-message">
          Mensaje <span className="required-mark" aria-hidden="true">*</span>
        </label>
        <textarea id="contact-message" name="message" rows={5}
          aria-required="true"
          aria-invalid={touched.message && !!errors.message ? 'true' : undefined}
          onBlur={() => setTouched(t => ({ ...t, message: true }))}
        />
        {touched.message && errors.message && (
          <span className="field-error" role="alert">{errors.message}</span>
        )}
      </div>

      <button type="submit" className="btn btn-primary">Enviar mensaje</button>
    </form>
  );
}
