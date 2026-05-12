// Server Component
import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = { title: 'Nosotros' };

const team = [
  { name: 'Marco Giordano', role: 'Chef ejecutivo y fundador', since: '1998' },
  { name: 'Valentina Giordano', role: 'Directora de sala y socia', since: '1998' },
  { name: 'Lucía Fernández', role: 'Sous chef', since: '2015' },
  { name: 'Tomás Rivas', role: 'Sommelier', since: '2019' },
  { name: 'Carla Medina', role: 'Pastelera', since: '2021' },
];

export default function AboutPage() {
  return (
    <>
      <nav className="breadcrumb" aria-label="Ruta de navegación">
        <ol>
          <li><Link href="/">Inicio</Link></li>
          <li><span aria-current="page">Nosotros</span></li>
        </ol>
      </nav>

      <h1>Nuestra historia</h1>

      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=700"
        alt="Interior del restaurante con mesas de madera, velas encendidas y luz cálida"
        width={700} height={400} style={{ width: '100%', borderRadius: 4, margin: '1.5rem 0' }} />

      <p>El Sauce nació en 1998 de la mano de la familia Giordano, que trajo consigo recetas, técnicas y el amor por la mesa compartida.</p>

      <section aria-labelledby="valores-heading" style={{ marginTop: '2rem' }}>
        <h2 id="valores-heading">Nuestros valores</h2>
        <div className="cards-grid">
          {[
            { title: 'Producto de estación', desc: 'El menú cambia con las estaciones. Respetamos ciclos y sabores naturales.' },
            { title: 'Kilómetro cero', desc: 'La mayoría de nuestros ingredientes vienen de un radio de 150 km.' },
            { title: 'Cero desperdicio', desc: 'Lo que no va al plato va al caldo. Lo que no va al caldo va al compost.' },
          ].map(v => (
            <article key={v.title} className="card">
              <div className="card-body">
                <h3>{v.title}</h3>
                <p>{v.desc}</p>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section aria-labelledby="equipo-heading">
        <h2 id="equipo-heading">El equipo</h2>
        <table style={{ marginTop: '1rem' }}>
          <caption>Equipo principal de El Sauce</caption>
          <thead>
            <tr>
              <th scope="col">Nombre</th>
              <th scope="col">Rol</th>
              <th scope="col">Desde</th>
            </tr>
          </thead>
          <tbody>
            {team.map(m => (
              <tr key={m.name}>
                <td>{m.name}</td>
                <td>{m.role}</td>
                <td>{m.since}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </>
  );
}
