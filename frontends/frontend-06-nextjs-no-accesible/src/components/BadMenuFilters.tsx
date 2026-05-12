'use client';
// [Visual total]   Items como <div>, sin ul/li ni semántica de lista
// [Daltonismo]     Precios solo en color verde, sin aria-label
// [Visual total]   Filtros como <span> sin role=button, sin tabindex
// [Visual total]   Sin aria-pressed en filtros
// [Visual total]   Sin anuncio aria-live al filtrar
import { useState } from 'react';

const dishes = [
  { id: 'bruschetta', name: 'Bruschetta al pomodoro', desc: 'Pan de masa madre, tomate cherry y albahaca.', price: '$2.800', tags: ['vegan'] },
  { id: 'carpaccio', name: 'Carpaccio de res', desc: 'Lomo crudo, rúcula, parmesano.', price: '$3.600', tags: ['gf'] },
  { id: 'risotto', name: 'Risotto de porcini', desc: 'Arroz arbóreo, porcini y trufa.', price: '$5.800', tags: ['gf'] },
  { id: 'salmon', name: 'Salmón a la plancha', desc: 'Salmón atlántico con espárragos.', price: '$6.500', tags: ['gf'] },
  { id: 'pasta', name: 'Pasta al pesto genovés', desc: 'Linguine con pesto de albahaca.', price: '$4.900', tags: ['vegan'] },
  { id: 'tiramisu', name: 'Tiramisú casero', desc: 'Mascarpone, café y cacao.', price: '$2.600', tags: [] },
];

export default function BadMenuFilters() {
  const [filter, setFilter] = useState('all');

  const filtered = filter === 'all' ? dishes : dishes.filter(d => d.tags.includes(filter));

  return (
    <>
      <div style={{ margin: '12px 0' }}>
        <span className={`filter-tag${filter === 'all' ? ' active' : ''}`} onClick={() => setFilter('all')}>Todos</span>
        <span className={`filter-tag${filter === 'vegan' ? ' active' : ''}`} onClick={() => setFilter('vegan')}>🌱</span>
        <span className={`filter-tag${filter === 'gf' ? ' active' : ''}`} onClick={() => setFilter('gf')}>🌾</span>
      </div>
      {filtered.map(dish => (
        <div key={dish.id} className="menu-div-item" id={dish.id}>
          <div>
            <div style={{ fontWeight: 'bold', fontSize: 13, color: '#aaa' }}>{dish.name}</div>
            <div style={{ fontSize: 11, color: '#ccc', marginTop: 3 }}>{dish.desc}</div>
            {dish.tags.length > 0 && (
              <div style={{ fontSize: 10, color: '#bbb', marginTop: 4 }}>
                {dish.tags.map(t => <span key={t}>{t === 'vegan' ? '🌱' : '🌾'}</span>)}
              </div>
            )}
          </div>
          <div className="price-green">{dish.price}</div>
        </div>
      ))}
    </>
  );
}
