// Server Component — shell estático, formulario en Client Component
import type { Metadata } from 'next';
import Link from 'next/link';
import ContactForm from '@/components/ContactForm';

export const metadata: Metadata = { title: 'Contacto' };

export default function ContactPage() {
  return (
    <>
      <nav className="breadcrumb" aria-label="Ruta de navegación">
        <ol>
          <li><Link href="/">Inicio</Link></li>
          <li><span aria-current="page">Contacto</span></li>
        </ol>
      </nav>

      <h1>Contacto</h1>
      <p style={{ margin: '0.75rem 0 2rem' }}>
        Completá el formulario y te respondemos dentro de las 24 horas hábiles.
        Los campos marcados con <abbr title="obligatorio">*</abbr> son obligatorios.
      </p>

      {/* Client Component — maneja estado del formulario */}
      <ContactForm />

      <section aria-labelledby="info-heading" style={{ marginTop: '3rem' }}>
        <h2 id="info-heading">También podés encontrarnos aquí</h2>
        <dl style={{ marginTop: '1rem', display: 'grid', gap: '0.75rem' }}>
          <div><dt style={{ fontWeight: 'bold' }}>Dirección</dt><dd>Av. Libertador 4200, Palermo, Buenos Aires</dd></div>
          <div><dt style={{ fontWeight: 'bold' }}>Teléfono</dt><dd><a href="tel:+541155551234">11 5555-1234</a></dd></div>
          <div><dt style={{ fontWeight: 'bold' }}>Correo</dt><dd><a href="mailto:hola@elsauce.com.ar">hola@elsauce.com.ar</a></dd></div>
        </dl>
      </section>
    </>
  );
}
