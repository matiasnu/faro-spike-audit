// FRONTEND-04 — INTENCIONALMENTE NO ACCESIBLE
// Sin TitleStrategy — el <title> nunca se actualiza al navegar
import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./pages/home/home').then(m => m.HomeComponent) },
  { path: 'about', loadComponent: () => import('./pages/about/about').then(m => m.AboutComponent) },
  { path: 'menu', loadComponent: () => import('./pages/menu/menu').then(m => m.MenuComponent) },
  { path: 'reservation', loadComponent: () => import('./pages/reservation/reservation').then(m => m.ReservationComponent) },
  { path: 'contact', loadComponent: () => import('./pages/contact/contact').then(m => m.ContactComponent) },
  { path: '**', redirectTo: '' },
];
