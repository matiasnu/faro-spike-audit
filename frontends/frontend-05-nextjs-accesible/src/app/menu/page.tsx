// Server Component — datos en servidor, filtros en cliente
import type { Metadata } from 'next';
import Link from 'next/link';
import MenuFilters from '@/components/MenuFilters';

export const metadata: Metadata = { title: 'Menú' };

export default function MenuPage() {
  return (
    <>
      <nav className="breadcrumb" aria-label="Ruta de navegación">
        <ol>
          <li><Link href="/">Inicio</Link></li>
          <li><span aria-current="page">Menú</span></li>
        </ol>
      </nav>

      <h1>Nuestra carta</h1>
      <p style={{ margin: '0.75rem 0 0.5rem', color: 'var(--color-text-muted)' }}>
        Precios en pesos argentinos, incluyen IVA.
      </p>

      {/* Client Component — maneja filtros interactivos */}
      <MenuFilters />
    </>
  );
}
