'use client';

import { useState } from 'react';

type Filter = 'all' | 'vegan' | 'gf';

interface Dish { id: string; name: string; desc: string; price: string; tags: string[]; }
interface Section { heading: string; dishes: Dish[]; }

const sections: Section[] = [
  {
    heading: 'Entradas',
    dishes: [
      { id: 'bruschetta', name: 'Bruschetta al pomodoro', desc: 'Pan de masa madre, tomate cherry, albahaca y aceite de oliva.', price: '$2.800', tags: ['vegan'] },
      { id: 'carpaccio', name: 'Carpaccio de res', desc: 'Lomo crudo, rúcula, parmesano y alcaparras.', price: '$3.600', tags: ['gf'] },
      { id: 'sopa', name: 'Sopa de tomate y albahaca', desc: 'Tomates asados con albahaca y crutones.', price: '$2.400', tags: ['vegan'] },
    ],
  },
  {
    heading: 'Platos principales',
    dishes: [
      { id: 'risotto', name: 'Risotto de porcini', desc: 'Arroz arbóreo, hongos porcini, parmesano y aceite de trufa.', price: '$5.800', tags: ['gf'] },
      { id: 'salmon', name: 'Salmón a la plancha', desc: 'Salmón atlántico con espárragos y salsa de limón.', price: '$6.500', tags: ['gf'] },
      { id: 'pasta', name: 'Pasta al pesto genovés', desc: 'Linguine artesanal con pesto de albahaca y piñones.', price: '$4.900', tags: ['vegan'] },
    ],
  },
  {
    heading: 'Postres',
    dishes: [
      { id: 'tiramisu', name: 'Tiramisú casero', desc: 'Bizcochos, mascarpone, café espresso y cacao.', price: '$2.600', tags: [] },
      { id: 'pannacotta', name: 'Panna cotta de vainilla', desc: 'Crema cocida con vainilla y coulis de frutos rojos.', price: '$2.200', tags: ['gf'] },
      { id: 'sorbete', name: 'Sorbete de limón y jengibre', desc: 'Sorbete artesanal con limón y jengibre fresco.', price: '$1.800', tags: ['vegan', 'gf'] },
    ],
  },
];

export default function MenuFilters() {
  const [filter, setFilter] = useState<Filter>('all');
  const [announcement, setAnnouncement] = useState('');

  function applyFilter(f: Filter) {
    setFilter(f);
    const count = sections.flatMap(s => s.dishes).filter(d => f === 'all' || d.tags.includes(f)).length;
    const label = f === 'all' ? 'todos los platos' : f === 'vegan' ? 'platos veganos' : 'platos sin gluten';
    setAnnouncement(`Mostrando ${label}: ${count} resultado${count !== 1 ? 's' : ''}`);
  }

  const filteredSections = sections.map(s => ({
    ...s,
    dishes: filter === 'all' ? s.dishes : s.dishes.filter(d => d.tags.includes(filter)),
  })).filter(s => s.dishes.length > 0);

  return (
    <>
      <div aria-live="polite" aria-atomic="true"
        style={{ position: 'absolute', width: 1, height: 1, overflow: 'hidden', clip: 'rect(0,0,0,0)' }}>
        {announcement}
      </div>

      <div role="group" aria-label="Filtrar por restricción alimentaria" className="filter-group">
        {(['all', 'vegan', 'gf'] as Filter[]).map(f => (
          <button key={f} className="btn btn-secondary"
            aria-pressed={filter === f}
            onClick={() => applyFilter(f)}>
            {f === 'all' ? 'Todos' : f === 'vegan' ? 'Veganos' : 'Sin gluten'}
          </button>
        ))}
      </div>

      {filteredSections.map(section => (
        <section key={section.heading} aria-labelledby={`section-${section.heading.toLowerCase().replace(' ', '-')}`} style={{ marginBottom: '2.5rem' }}>
          <h2 id={`section-${section.heading.toLowerCase().replace(' ', '-')}`}>{section.heading}</h2>
          <ul role="list" style={{ listStyle: 'none', marginTop: '1rem', display: 'grid', gap: '0.75rem' }}>
            {section.dishes.map(dish => (
              <li key={dish.id} id={dish.id} className="menu-item">
                <div>
                  <strong style={{ fontSize: '1.05rem' }}>{dish.name}</strong>
                  <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', marginTop: '0.25rem' }}>{dish.desc}</p>
                  {dish.tags.length > 0 && (
                    <p style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)', marginTop: '0.25rem' }}>
                      {dish.tags.map(t => t === 'vegan' ? 'Vegano' : 'Sin gluten').join(' · ')}
                    </p>
                  )}
                </div>
                <span className="menu-item-price" aria-label={`Precio: ${dish.price}`}>{dish.price}</span>
              </li>
            ))}
          </ul>
        </section>
      ))}
    </>
  );
}
