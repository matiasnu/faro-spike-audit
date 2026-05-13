// FRONTEND-06 — INTENCIONALMENTE NO ACCESIBLE
// [Visual total]   lang="en" incorrecto
// [Visual total]   Sin RouteAnnouncer — cambios de ruta silenciosos
// [Motora severa]  Sin skip link
// [Visual total]   Sin landmarks: div en lugar de header/main/nav/footer
// [Visual total]   Sin metadata.title por ruta
import './globals.css';
import Link from 'next/link';
import BadNav from '@/components/BadNav';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div style={{ background: '#7fb3d3', padding: '10px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Link href="/" style={{ color: '#d0e8f5', fontSize: 18, textDecoration: 'none' }}>El Sauce</Link>
          <BadNav />
        </div>

        <div className="container">
          {children}
        </div>

        <div style={{ background: '#eee', color: '#ccc', textAlign: 'center', padding: 15, fontSize: 11, marginTop: 40 }}>
          <p>© 2024 El Sauce · <Link href="/contact" style={{ color: '#bbb' }}>Contacto</Link></p>
        </div>
      </body>
    </html>
  );
}
