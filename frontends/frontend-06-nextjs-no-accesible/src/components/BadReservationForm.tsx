'use client';
// [Motora severa]  Calendario custom con aria-hidden="true" — inaccesible
// [Motora severa]  Dropdown de hora solo con :hover — no con teclado
// [Cognitiva]      Multi-paso sin indicador de progreso
// [Cognitiva]      Timeout silencioso de 30s
// [Visual total]   Sin labels, sin aria-invalid, sin feedback en DOM
import { useState, useEffect } from 'react';

export default function BadReservationForm() {
  const [step, setStep] = useState(1);
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedTime, setSelectedTime] = useState('');
  const [expired, setExpired] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setExpired(true), 30000);
    return () => clearTimeout(t);
  }, []);

  if (expired) return <p style={{ color: '#ccc', fontSize: 12 }}>La sesión expiró. Recargá la página.</p>;

  return (
    <div style={{ maxWidth: 480 }}>
      {step === 1 && (
        <div>
          <input type="text" placeholder="Tu nombre" />
          <input type="email" placeholder="Tu email" />
          <input type="tel" placeholder="Tu teléfono" />
          <button className="btn" onClick={() => setStep(2)}>Siguiente</button>
        </div>
      )}
      {step === 2 && (
        <div>
          <p style={{ fontSize: 12, color: '#bbb', marginBottom: 6 }}>Seleccioná una fecha (solo mouse):</p>
          <div role="presentation" aria-hidden="true" style={{ border: '1px solid #ddd', padding: 10, fontSize: 12, color: '#aaa', marginBottom: 10 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, color: '#bbb' }}>
              <span style={{ cursor: 'pointer' }}>◀</span>
              <span>Mayo 2026</span>
              <span style={{ cursor: 'pointer' }}>▶</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7,1fr)', gap: 4, textAlign: 'center' }}>
              {['Lu','Ma','Mi','Ju','Vi','Sa','Do'].map(d => <div key={d} style={{ fontWeight: 'bold', color: '#ccc' }}>{d}</div>)}
              {Array.from({ length: 31 }, (_, i) => i + 1).map(d => (
                <div key={d} onClick={() => setSelectedDate(String(d))}
                  style={{ padding: 4, cursor: 'pointer', borderRadius: 2, background: selectedDate === String(d) ? '#7fb3d3' : '', color: selectedDate === String(d) ? '#fff' : '' }}>
                  {d}
                </div>
              ))}
            </div>
          </div>

          <p style={{ fontSize: 12, color: '#bbb', marginBottom: 4 }}>Horario (pasá el mouse):</p>
          <div className="hover-dropdown" style={{ marginBottom: 10 }}>
            <div style={{ border: '1px solid #ddd', padding: '6px 8px', fontSize: 12, color: '#aaa', borderRadius: 2, background: '#fafafa' }}>
              {selectedTime || 'Seleccioná un horario'}
            </div>
            <div className="hover-dropdown-content">
              {['12:00','12:30','13:00','20:00','20:30','21:00'].map(t => (
                <div key={t} onClick={() => setSelectedTime(t)}>{t}</div>
              ))}
            </div>
          </div>

          <input type="number" placeholder="Personas" />
          <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
            <button className="btn" onClick={() => setStep(1)}>Atrás</button>
            <button className="btn" onClick={() => setStep(3)}>Siguiente</button>
          </div>
        </div>
      )}
      {step === 3 && (
        <div>
          <textarea placeholder="Restricciones alimentarias (opcional)" rows={3} />
          <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
            <button className="btn" onClick={() => setStep(2)}>Atrás</button>
            <button className="btn" onClick={() => alert('Reserva enviada.')}>Confirmar</button>
          </div>
        </div>
      )}
    </div>
  );
}
