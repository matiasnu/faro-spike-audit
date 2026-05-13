import { Component, inject, signal } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-reservation',
  imports: [ReactiveFormsModule],
  templateUrl: './reservation.html',
})
export class ReservationComponent {
  private fb = inject(FormBuilder);
  submitted = signal(false);

  form = this.fb.group({
    name:    ['', Validators.required],
    email:   ['', [Validators.required, Validators.email]],
    phone:   ['', Validators.required],
    date:    ['', Validators.required],
    time:    ['', Validators.required],
    guests:  ['', [Validators.required, Validators.min(1), Validators.max(20)]],
    occasion:[''],
    dietary: [''],
  });

  isInvalid(field: string): boolean {
    const ctrl = this.form.get(field);
    return !!(ctrl && ctrl.invalid && ctrl.touched);
  }

  errorMsg(field: string): string {
    const ctrl = this.form.get(field);
    if (!ctrl || !ctrl.errors || !ctrl.touched) return '';
    if (ctrl.errors['required']) return 'Este campo es obligatorio.';
    if (ctrl.errors['email']) return 'Ingresá un correo electrónico válido.';
    if (ctrl.errors['min']) return 'El mínimo es 1 persona.';
    if (ctrl.errors['max']) return 'Para grupos de más de 20, contactanos directamente.';
    return '';
  }

  onSubmit(): void {
    this.form.markAllAsTouched();
    if (this.form.invalid) {
      const firstInvalid = document.querySelector('[aria-invalid="true"]') as HTMLElement;
      firstInvalid?.focus();
      return;
    }
    this.submitted.set(true);
    this.form.reset();
  }
}
