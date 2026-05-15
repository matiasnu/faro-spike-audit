import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./pages/home/home').then(m => m.HomeComponent), title: 'Inicio' },
  { path: 'about', loadComponent: () => import('./pages/about/about').then(m => m.AboutComponent), title: 'Nosotros' },
  { path: 'menu', loadComponent: () => import('./pages/menu/menu').then(m => m.MenuComponent), title: 'Menú' },
  { path: 'reservation', loadComponent: () => import('./pages/reservation/reservation').then(m => m.ReservationComponent), title: 'Reservas' },
  { path: 'contact', loadComponent: () => import('./pages/contact/contact').then(m => m.ContactComponent), title: 'Contacto' },
  { path: '**', redirectTo: '' },
];
