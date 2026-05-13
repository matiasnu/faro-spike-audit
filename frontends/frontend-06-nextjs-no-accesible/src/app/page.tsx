// FRONTEND-06 — INTENCIONALMENTE NO ACCESIBLE
// [Visual total]   Sin generateMetadata — <title> no cambia
// [Fotosensibilidad] Banner parpadeante sin control
// [Visual total]   Imágenes sin alt o con alt genérico
// [Visual total]   Links "click aquí", "ver más" sin contexto
// [Visual total]   Jerarquía rota: h4 sin h1/h2/h3 previo
// [Visual total]   Tabla sin th, sin caption, sin scope
// [Visual total]   iframe sin title
import Link from 'next/link';

export default function HomePage() {
  return (
    <>
      <div className="flash-banner">¡OFERTA ESPECIAL! 20% de descuento todos los martes</div>

      <div style={{ textAlign: 'center', padding: '30px 20px', background: '#f0f7fc', marginBottom: 20 }}>
        <h4 style={{ fontSize: 24, color: '#7fb3d3', marginBottom: 8 }}>Bienvenidos a El Sauce</h4>
        <p style={{ color: '#bbb', fontSize: 13, marginBottom: 12 }}>Cocina mediterránea de autor.</p>
        <Link href="/reservation" className="btn">Click aquí</Link>
        {' '}
        <Link href="/menu" className="btn">Ver más</Link>
      </div>

      <h4 style={{ color: '#aaa', marginBottom: 12 }}>Platos destacados</h4>
      <div className="cards-grid">
        <div className="card">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=600" />
          <div className="card-body">
            <h2>Risotto de porcini</h2>
            <p>Arroz cremoso con hongos y trufa.</p>
            <Link href="/menu" className="btn btn-sm">click aquí</Link>
          </div>
        </div>
        <div className="card">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=600" alt="foto" />
          <div className="card-body">
            <h2>Salmón a la plancha</h2>
            <p>Salmón con espárragos y limón.</p>
            <Link href="/menu" className="btn btn-sm">ver más</Link>
          </div>
        </div>
        <div className="card">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=600" alt="" />
          <div className="card-body">
            <h2>Tiramisú casero</h2>
            <p>Mascarpone, café y cacao.</p>
            <Link href="/menu" className="btn btn-sm">leer más</Link>
          </div>
        </div>
      </div>

      <h4 style={{ color: '#aaa', marginBottom: 8 }}>Horarios</h4>
      <table>
        <tr><td>Día</td><td>Almuerzo</td><td>Cena</td></tr>
        <tr><td>Lunes a viernes</td><td>12:00 – 15:30</td><td>20:00 – 23:30</td></tr>
        <tr><td>Sábados</td><td>12:00 – 16:00</td><td>20:00 – 00:00</td></tr>
        <tr><td>Domingos</td><td>12:00 – 16:00</td><td>Cerrado</td></tr>
      </table>

      <iframe src="about:blank" style={{ border: 'none', width: '100%', height: 200, background: '#f0f0f0' }} />
    </>
  );
}
