// Server Component — renderizado en el servidor
import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = { title: 'Inicio' };

const schedule = [
  { day: 'Lunes a viernes', lunch: '12:00 – 15:30', dinner: '20:00 – 23:30' },
  { day: 'Sábados', lunch: '12:00 – 16:00', dinner: '20:00 – 00:00' },
  { day: 'Domingos y feriados', lunch: '12:00 – 16:00', dinner: 'Cerrado' },
];

export default function HomePage() {
  return (
    <>
      <section className="hero" aria-labelledby="hero-heading">
        <h1 id="hero-heading">Bienvenidos a El Sauce</h1>
        <p>Cocina mediterránea de autor, con ingredientes de estación y productores locales.</p>
        <Link href="/reservation" className="btn btn-primary">Reservar una mesa</Link>
        {' '}
        <Link href="/menu" className="btn btn-secondary">Ver nuestro menú</Link>
      </section>

      <section aria-labelledby="destacados-heading">
        <h2 id="destacados-heading">Platos destacados</h2>
        <div className="cards-grid">
          {[
            { src: 'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=600', alt: 'Risotto de hongos porcini con parmesano y aceite de trufa', title: 'Risotto de porcini', desc: 'Arroz arbóreo cremoso con hongos porcini, parmesano y aceite de trufa blanca.', href: '/menu#risotto' },
            { src: 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=600', alt: 'Salmón a la plancha con espárragos verdes y limón', title: 'Salmón a la plancha', desc: 'Filete de salmón atlántico con espárragos de temporada y salsa de limón.', href: '/menu#salmon' },
            { src: 'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=600', alt: 'Tiramisú casero con cacao en polvo y bizcochos de champán', title: 'Tiramisú casero', desc: 'La receta clásica con mascarpone, café espresso y cacao amargo de origen.', href: '/menu#tiramisu' },
          ].map(card => (
            <article key={card.title} className="card">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={card.src} alt={card.alt} width={600} height={180} />
              <div className="card-body">
                <h3>{card.title}</h3>
                <p>{card.desc}</p>
                <Link href={card.href} className="btn btn-secondary">Ver en el menú</Link>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section aria-labelledby="horarios-heading">
        <h2 id="horarios-heading">Horarios de atención</h2>
        <table>
          <caption>Días y horarios del restaurante</caption>
          <thead>
            <tr>
              <th scope="col">Día</th>
              <th scope="col">Almuerzo</th>
              <th scope="col">Cena</th>
            </tr>
          </thead>
          <tbody>
            {schedule.map(row => (
              <tr key={row.day}>
                <td>{row.day}</td>
                <td>{row.lunch}</td>
                <td>{row.dinner}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </>
  );
}
