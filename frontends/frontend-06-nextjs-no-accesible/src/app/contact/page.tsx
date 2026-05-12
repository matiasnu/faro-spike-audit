import BadContactForm from '@/components/BadContactForm';

export default function ContactPage() {
  return (
    <>
      <h1>Contacto</h1>
      <p style={{ fontSize: 12, color: '#ccc', marginBottom: 15 }}>Completá el formulario y te respondemos.</p>
      <BadContactForm />
      <div style={{ marginTop: 25 }}>
        <h2 style={{ fontSize: 14, color: '#aaa' }}>Encontranos</h2>
        <p style={{ fontSize: 12, color: '#aaa', marginTop: 6 }}>Av. Libertador 4200, Buenos Aires</p>
        <p style={{ fontSize: 12 }}>
          <a href="mailto:hola@elsauce.com.ar" style={{ color: '#bbb' }}>click aquí</a> para escribirnos.
        </p>
      </div>
    </>
  );
}
