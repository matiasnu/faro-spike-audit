'use client';
// [Visual total]   Algunos items de nav como <div> sin semántica de link
// [Motora severa]  Sin aria-current — el screen reader no sabe qué página está activa
// [Visual total]   Sin landmarks: no es un <nav>
import Link from 'next/link';

export default function BadNav() {
  return (
    <div style={{ display: 'flex', gap: 5 }}>
      <Link href="/" style={{ color: '#d0e8f5', fontSize: 12, padding: '4px 8px', textDecoration: 'none' }}>Inicio</Link>
      <div style={{ color: '#d0e8f5', fontSize: 12, padding: '4px 8px', cursor: 'pointer' }}
        onClick={() => window.location.href = '/about'}>
        Nosotros
      </div>
      <div style={{ color: '#d0e8f5', fontSize: 12, padding: '4px 8px', cursor: 'pointer' }}
        onClick={() => window.location.href = '/menu'}>
        Menú
      </div>
      <Link href="/reservation" style={{ color: '#d0e8f5', fontSize: 12, padding: '4px 8px', textDecoration: 'none' }}>Reservas</Link>
      <Link href="/contact" style={{ color: '#d0e8f5', fontSize: 12, padding: '4px 8px', textDecoration: 'none' }}>Contacto</Link>
    </div>
  );
}
