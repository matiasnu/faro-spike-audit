import { Component, signal, computed, inject } from '@angular/core';
import { LiveAnnouncer } from '@angular/cdk/a11y';

type Filter = 'all' | 'vegan' | 'gf';

interface Dish {
  id: string;
  name: string;
  desc: string;
  price: string;
  tags: string[];
}

interface Section {
  heading: string;
  headingId: string;
  dishes: Dish[];
}

@Component({
  selector: 'app-menu',
  templateUrl: './menu.html',
})
export class MenuComponent {
  private announcer = inject(LiveAnnouncer);

  activeFilter = signal<Filter>('all');

  readonly sections: Section[] = [
    {
      heading: 'Entradas',
      headingId: 'section-entradas',
      dishes: [
        { id: 'bruschetta', name: 'Bruschetta al pomodoro', desc: 'Pan de masa madre, tomate cherry, albahaca y aceite de oliva.', price: '$2.800', tags: ['vegan'] },
        { id: 'carpaccio', name: 'Carpaccio de res', desc: 'Lomo crudo, rúcula, parmesano y alcaparras.', price: '$3.600', tags: ['gf'] },
        { id: 'sopa', name: 'Sopa de tomate y albahaca', desc: 'Tomates asados con albahaca y crutones.', price: '$2.400', tags: ['vegan'] },
      ],
    },
    {
      heading: 'Platos principales',
      headingId: 'section-principales',
      dishes: [
        { id: 'risotto', name: 'Risotto de porcini', desc: 'Arroz arbóreo, hongos porcini, parmesano y aceite de trufa.', price: '$5.800', tags: ['gf'] },
        { id: 'salmon', name: 'Salmón a la plancha', desc: 'Salmón atlántico con espárragos y salsa de limón.', price: '$6.500', tags: ['gf'] },
        { id: 'pasta', name: 'Pasta al pesto genovés', desc: 'Linguine artesanal con pesto de albahaca y piñones.', price: '$4.900', tags: ['vegan'] },
      ],
    },
    {
      heading: 'Postres',
      headingId: 'section-postres',
      dishes: [
        { id: 'tiramisu', name: 'Tiramisú casero', desc: 'Bizcochos, mascarpone, café espresso y cacao.', price: '$2.600', tags: [] },
        { id: 'pannacotta', name: 'Panna cotta de vainilla', desc: 'Crema cocida con vainilla y coulis de frutos rojos.', price: '$2.200', tags: ['gf'] },
        { id: 'sorbete', name: 'Sorbete de limón y jengibre', desc: 'Sorbete artesanal con limón y jengibre fresco.', price: '$1.800', tags: ['vegan', 'gf'] },
      ],
    },
  ];

  filteredSections = computed(() => {
    const f = this.activeFilter();
    return this.sections.map(s => ({
      ...s,
      dishes: f === 'all' ? s.dishes : s.dishes.filter(d => d.tags.includes(f)),
    })).filter(s => s.dishes.length > 0);
  });

  setFilter(f: Filter): void {
    this.activeFilter.set(f);
    const label = f === 'all' ? 'todos los platos' : f === 'vegan' ? 'platos veganos' : 'platos sin gluten';
    const count = this.filteredSections().reduce((acc, s) => acc + s.dishes.length, 0);
    this.announcer.announce(`Mostrando ${label}: ${count} resultado${count !== 1 ? 's' : ''}`);
  }

  tagLabel(tag: string): string {
    return tag === 'vegan' ? 'Vegano' : 'Sin gluten';
  }
}
