import { Component } from '@angular/core';

interface Dish { id: string; name: string; desc: string; price: string; tags: string[]; }

@Component({
  selector: 'app-menu',
  templateUrl: './menu.html',
})
export class MenuComponent {
  activeFilter = 'all';

  dishes: Dish[] = [
    { id: 'bruschetta', name: 'Bruschetta al pomodoro', desc: 'Pan de masa madre, tomate cherry y albahaca.', price: '$2.800', tags: ['vegan'] },
    { id: 'carpaccio', name: 'Carpaccio de res', desc: 'Lomo crudo, rúcula, parmesano y alcaparras.', price: '$3.600', tags: ['gf'] },
    { id: 'risotto', name: 'Risotto de porcini', desc: 'Arroz arbóreo, hongos porcini y trufa.', price: '$5.800', tags: ['gf'] },
    { id: 'salmon', name: 'Salmón a la plancha', desc: 'Salmón atlántico con espárragos y limón.', price: '$6.500', tags: ['gf'] },
    { id: 'pasta', name: 'Pasta al pesto genovés', desc: 'Linguine con pesto de albahaca y piñones.', price: '$4.900', tags: ['vegan'] },
    { id: 'tiramisu', name: 'Tiramisú casero', desc: 'Mascarpone, café espresso y cacao.', price: '$2.600', tags: [] },
  ];

  get filtered(): Dish[] {
    if (this.activeFilter === 'all') return this.dishes;
    return this.dishes.filter(d => d.tags.includes(this.activeFilter));
  }

  setFilter(f: string): void {
    this.activeFilter = f;
    // Sin LiveAnnouncer — el cambio no se anuncia
    // Sin aria-pressed actualizado
  }
}
