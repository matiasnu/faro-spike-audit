import type { Metadata } from 'next';
import './globals.css';
import Link from 'next/link';
import Nav from '@/components/Nav';
import RouteAnnouncer from '@/components/RouteAnnouncer';

export const metadata: Metadata = {
  title: { default: 'El Sauce', template: '%s — El Sauce' },
  description: 'Restaurante El Sauce — cocina mediterránea de autor en Buenos Aires.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        {/* Anuncia cambios de ruta al screen reader — Next.js App Router no lo hace por defecto */}
        <RouteAnnouncer />

        <a href="#main-content" className="skip-link">Saltar al contenido principal</a>

        <header className="site-header" role="banner">
          <div className="header-inner">
            <Link href="/" className="site-logo" aria-label="El Sauce — ir al inicio">El Sauce</Link>
            <Nav />
          </div>
        </header>

        <main id="main-content" className="container">
          {children}
        </main>

        <footer className="site-footer" role="contentinfo">
          <p>© 2024 Restaurante El Sauce · Av. Libertador 4200, Buenos Aires ·{' '}
            <Link href="/contact">Contacto</Link>
          </p>
        </footer>
      </body>
    </html>
  );
}
