import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-home',
  imports: [RouterLink],
  templateUrl: './home.html',
})
export class HomeComponent {
  readonly schedule = [
    { day: 'Lunes a viernes', lunch: '12:00 – 15:30', dinner: '20:00 – 23:30' },
    { day: 'Sábados', lunch: '12:00 – 16:00', dinner: '20:00 – 00:00' },
    { day: 'Domingos y feriados', lunch: '12:00 – 16:00', dinner: 'Cerrado' },
  ];
}
