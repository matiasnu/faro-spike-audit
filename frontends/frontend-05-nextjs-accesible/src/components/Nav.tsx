'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const links = [
  { href: '/', label: 'Inicio' },
  { href: '/about', label: 'Nosotros' },
  { href: '/menu', label: 'Menú' },
  { href: '/reservation', label: 'Reservas' },
  { href: '/contact', label: 'Contacto' },
];

export default function Nav() {
  const pathname = usePathname();

  return (
    <nav className="main-nav" aria-label="Navegación principal">
      <ul role="list">
        {links.map(({ href, label }) => {
          const isActive = href === '/' ? pathname === '/' : pathname.startsWith(href);
          return (
            <li key={href}>
              <Link href={href} aria-current={isActive ? 'page' : undefined}>
                {label}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
