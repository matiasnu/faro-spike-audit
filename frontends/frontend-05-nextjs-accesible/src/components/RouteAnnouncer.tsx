'use client';

// Anuncia cambios de ruta al screen reader.
// En Next.js App Router no hay anunciador built-in — este componente lo suple.
import { usePathname } from 'next/navigation';
import { useEffect, useRef, useState } from 'react';

export default function RouteAnnouncer() {
  const pathname = usePathname();
  const [announcement, setAnnouncement] = useState('');
  const firstRender = useRef(true);

  useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      return;
    }
    // Espera a que el <title> se actualice antes de leerlo
    const timer = setTimeout(() => {
      const title = document.title || pathname;
      setAnnouncement(`Navegaste a: ${title}`);
    }, 100);

    return () => clearTimeout(timer);
  }, [pathname]);

  return (
    <div
      aria-live="assertive"
      aria-atomic="true"
      style={{ position: 'absolute', width: 1, height: 1, overflow: 'hidden', clip: 'rect(0,0,0,0)', whiteSpace: 'nowrap' }}
    >
      {announcement}
    </div>
  );
}
