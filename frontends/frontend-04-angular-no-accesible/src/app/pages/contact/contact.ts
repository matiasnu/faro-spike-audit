import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-contact',
  imports: [FormsModule],
  templateUrl: './contact.html',
})
export class ContactComponent {
  name = '';
  email = '';
  message = '';
  hasErrors = false;

  onSubmit(): void {
    if (!this.name || !this.email || !this.message) {
      this.hasErrors = true;
      // Solo agrega clase visual — sin texto de error, sin aria-invalid, sin foco
      return;
    }
    // alert() en vez de feedback en DOM
    alert('Formulario enviado.');
    this.name = '';
    this.email = '';
    this.message = '';
    this.hasErrors = false;
  }
}
