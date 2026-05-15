'use client';

import { useState, useRef } from 'react';
import Link from 'next/link';

interface Errors { name?: string; email?: string; phone?: string; date?: string; time?: string; guests?: string; }

export default function ReservationForm() {
  const [submitted, setSubmitted] = useState(false);
  const [errors, setErrors] = useState<Errors>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});
  const successRef = useRef<HTMLDivElement>(null);

  function validate(data: FormData): Errors {
    const e: Errors = {};
    if (!data.get('name')) e.name = 'Este campo es obligatorio.';
    const email = data.get('email') as string;
    if (!email) e.email = 'Este campo es obligatorio.';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) e.email = 'Ingresá un correo electrónico válido.';
    if (!data.get('phone')) e.phone = 'Este campo es obligatorio.';
    if (!data.get('date')) e.date = 'Este campo es obligatorio.';
    if (!data.get('time')) e.time = 'Este campo es obligatorio.';
    const guests = Number(data.get('guests'));
    if (!guests) e.guests = 'Este campo es obligatorio.';
    else if (guests < 1) e.guests = 'El mínimo es 1 persona.';
    else if (guests > 20) e.guests = 'Para más de 20 personas, contactanos directamente.';
    return e;
  }

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    const errs = validate(data);
    setTouched({ name: true, email: true, phone: true, date: true, time: true, guests: true });
    setErrors(errs);
    if (Object.keys(errs).length > 0) {
      const firstInvalid = e.currentTarget.querySelector('[aria-invalid="true"]') as HTMLElement;
      firstInvalid?.focus();
      return;
    }
    setSubmitted(true);
    setTimeout(() => successRef.current?.focus(), 50);
  }

  const field = (name: keyof Errors) => ({
    'aria-required': 'true' as const,
    'aria-invalid': (touched[name] && !!errors[name] ? 'true' : undefined) as 'true' | undefined,
    onBlur: () => setTouched(t => ({ ...t, [name]: true })),
  });

  if (submitted) {
    return (
      <div ref={successRef} className="alert alert-success" role="status" aria-live="polite" tabIndex={-1}>
        ¡Reserva confirmada! Te contactaremos dentro de las 2 horas.
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} noValidate style={{ maxWidth: 600 }}>
      <fieldset>
        <legend>Datos de contacto</legend>

        <div className="form-group" style={{ marginTop: '1rem' }}>
          <label htmlFor="res-name">Nombre completo <span className="required-mark" aria-hidden="true">*</span></label>
          <input id="res-name" type="text" name="name" autoComplete="name" {...field('name')} />
          {touched.name && errors.name && <span className="field-error" role="alert">{errors.name}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="res-email">Correo electrónico <span className="required-mark" aria-hidden="true">*</span></label>
          <input id="res-email" type="email" name="email" autoComplete="email" {...field('email')} />
          {touched.email && errors.email && <span className="field-error" role="alert">{errors.email}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="res-phone">Teléfono <span className="required-mark" aria-hidden="true">*</span></label>
          <input id="res-phone" type="tel" name="phone" autoComplete="tel" {...field('phone')} />
          {touched.phone && errors.phone && <span className="field-error" role="alert">{errors.phone}</span>}
        </div>
      </fieldset>

      <fieldset>
        <legend>Detalles de la reserva</legend>

        <div className="form-group" style={{ marginTop: '1rem' }}>
          <label htmlFor="res-date">Fecha <span className="required-mark" aria-hidden="true">*</span></label>
          <input id="res-date" type="date" name="date" aria-describedby="res-date-hint" {...field('date')} />
          <span className="form-hint" id="res-date-hint">Reservas con al menos 24 hs de anticipación.</span>
          {touched.date && errors.date && <span className="field-error" role="alert">{errors.date}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="res-time">Horario <span className="required-mark" aria-hidden="true">*</span></label>
          <select id="res-time" name="time" {...field('time')}>
            <option value="">— Seleccioná un horario —</option>
            <optgroup label="Almuerzo">
              <option value="12:00">12:00</option>
              <option value="12:30">12:30</option>
              <option value="13:00">13:00</option>
              <option value="13:30">13:30</option>
            </optgroup>
            <optgroup label="Cena">
              <option value="20:00">20:00</option>
              <option value="20:30">20:30</option>
              <option value="21:00">21:00</option>
              <option value="21:30">21:30</option>
            </optgroup>
          </select>
          {touched.time && errors.time && <span className="field-error" role="alert">{errors.time}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="res-guests">Número de personas <span className="required-mark" aria-hidden="true">*</span></label>
          <input id="res-guests" type="number" name="guests" min={1} max={20} aria-describedby="res-guests-hint" {...field('guests')} />
          <span className="form-hint" id="res-guests-hint">Para más de 20 personas, contactanos directamente.</span>
          {touched.guests && errors.guests && <span className="field-error" role="alert">{errors.guests}</span>}
        </div>
      </fieldset>

      <div className="form-group">
        <label htmlFor="res-dietary">Restricciones alimentarias (opcional)</label>
        <textarea id="res-dietary" name="dietary" rows={3} placeholder="Ej: un comensal es celíaco..." />
      </div>

      <button type="submit" className="btn btn-primary">Confirmar reserva</button>
      <Link href="/" className="btn btn-secondary" style={{ marginLeft: '1rem' }}>Cancelar</Link>
    </form>
  );
}
