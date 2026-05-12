// FRONTEND-04 — INTENCIONALMENTE NO ACCESIBLE
// Problemas Angular-específicos:
// [Visual total]   Sin LiveAnnouncer — los cambios de ruta no se anuncian al screen reader
// [Motora severa]  Sin focus management — el foco queda en el link que se clickeó
// [Visual total]   Sin TitleStrategy — el <title> no cambia entre rutas
import { Component } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {}
