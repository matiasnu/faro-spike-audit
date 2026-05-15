// Server Component — shell estático, formulario en Client Component
import type { Metadata } from 'next';
import Link from 'next/link';
import ReservationForm from '@/components/ReservationForm';

export const metadata: Metadata = { title: 'Reservas' };

export default function ReservationPage() {
  return (
    <>
      <nav className="breadcrumb" aria-label="Ruta de navegación">
        <ol>
          <li><Link href="/">Inicio</Link></li>
          <li><span aria-current="page">Reservas</span></li>
        </ol>
      </nav>

      <h1>Reservá tu mesa</h1>
      <p style={{ margin: '0.75rem 0 2rem' }}>
        Completá el formulario y te confirmamos la reserva dentro de las 2 horas.
        Los campos con <abbr title="obligatorio">*</abbr> son obligatorios.
      </p>

      {/* Client Component — maneja estado del formulario multi-paso */}
      <ReservationForm />

      <section aria-labelledby="politica-heading" style={{ marginTop: '3rem' }}>
        <h2 id="politica-heading">Política de reservas</h2>
        <ul style={{ marginTop: '1rem', paddingLeft: '1.25rem', lineHeight: 2 }}>
          <li>Las reservas se confirman por correo dentro de las 2 horas.</li>
          <li>Cancelaciones sin cargo hasta 4 horas antes del turno.</li>
          <li>La mesa se mantiene reservada durante 15 minutos pasado el horario.</li>
        </ul>
      </section>
    </>
  );
}
