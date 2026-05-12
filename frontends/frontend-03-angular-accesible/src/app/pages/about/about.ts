import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-about',
  imports: [RouterLink],
  templateUrl: './about.html',
})
export class AboutComponent {
  readonly team = [
    { name: 'Marco Giordano', role: 'Chef ejecutivo y fundador', since: '1998' },
    { name: 'Valentina Giordano', role: 'Directora de sala y socia', since: '1998' },
    { name: 'Lucía Fernández', role: 'Sous chef', since: '2015' },
    { name: 'Tomás Rivas', role: 'Sommelier', since: '2019' },
    { name: 'Carla Medina', role: 'Pastelera', since: '2021' },
  ];
}
