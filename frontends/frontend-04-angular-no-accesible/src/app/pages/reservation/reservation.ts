import { Component, signal, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-reservation',
  imports: [FormsModule],
  templateUrl: './reservation.html',
})
export class ReservationComponent implements OnInit {
  currentStep = signal(1);
  selectedDate = '';
  selectedTime = '';

  // Timeout silencioso — destruye el formulario sin avisar
  ngOnInit(): void {
    setTimeout(() => {
      this.currentStep.set(99);
      // No avisa, no anuncia con aria-live, no ofrece extender
    }, 30000);
  }

  nextStep(): void {
    this.currentStep.update(s => s + 1);
    // Sin aria-live, sin movimiento de foco, sin anuncio de cambio de paso
  }

  prevStep(): void {
    this.currentStep.update(s => s - 1);
  }

  selectTime(t: string): void {
    this.selectedTime = t;
    // No anuncia el valor seleccionado al screen reader
  }

  submit(): void {
    alert('Reserva enviada.');
  }
}
