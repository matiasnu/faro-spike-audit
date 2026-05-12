'use client';
// [Visual total, Cognitiva] Inputs sin label — solo placeholder
// [Daltonismo]              Errores solo por borde rojo, sin texto
// [Visual total]            Sin aria-invalid, sin aria-describedby
// [Visual total]            aria-hidden="true" en el mensaje de error
// [Motora parcial]          Botón con target de 16px
// [Visual total]            alert() en vez de feedback en DOM
import { useState } from 'react';

export default function BadContactForm() {
  const [hasErrors, setHasErrors] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!name || !email || !message) {
      setHasErrors(true);
      return;
    }
    alert('Formulario enviado.');
    setName(''); setEmail(''); setMessage('');
    setHasErrors(false);
  }

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 500 }}>
      <input type="text" placeholder="Nombre completo" value={name} onChange={e => setName(e.target.value)}
        className={hasErrors && !name ? 'error' : ''} />
      <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)}
        className={hasErrors && !email ? 'error' : ''} />
      <input type="tel" placeholder="Teléfono" />
      <select><option value="">Asunto</option><option value="r">Reservas</option><option value="o">Otro</option></select>
      <textarea placeholder="Mensaje" rows={4} value={message} onChange={e => setMessage(e.target.value)}
        className={hasErrors && !message ? 'error' : ''} />
      {hasErrors && (
        <p style={{ color: '#e57373', fontSize: 11, marginBottom: 8 }} aria-hidden="true">
          Hay campos incompletos.
        </p>
      )}
      <button type="submit" style={{ padding: '2px 8px', fontSize: 11, border: '1px solid #ccc', background: '#ebebeb', color: '#aaa', cursor: 'pointer', borderRadius: 2 }}>
        Enviar
      </button>
    </form>
  );
}
