// [Visual total]   Sin generateMetadata — mismo <title> que home
// [Visual total]   Imagen decorativa con alt de 200 palabras
// [Baja visión]    Texto en imagen SVG no seleccionable
// [Visual total]   Jerarquía rota h1 → h3 → h5
// [Visual total]   Tabla sin th, sin caption, sin scope
// [Daltonismo]     Color como único indicador de estado
export default function AboutPage() {
  return (
    <>
      <h1>Nuestra historia</h1>

      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=700"
        alt="Fotografía artística de alta resolución del interior del restaurante El Sauce tomada en el año 2023 durante la noche, mostrando mesas de madera oscura con manteles blancos, velas encendidas de color marfil en candelabros de bronce dorado, sillas tapizadas en cuero color camel, paredes de ladrillo visto pintadas en blanco envejecido, iluminación cálida de color ámbar proveniente de lámparas colgantes de estilo industrial con pantallas de vidrio esmerilado, y al fondo una barra de madera con estantes llenos de botellas de vino de diferentes regiones del mundo"
        style={{ width: '100%', marginBottom: 15 }} width={700} height={400}
      />

      {/* Texto en imagen SVG — no seleccionable, no escalable */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='600' height='80'%3E%3Crect width='600' height='80' fill='%23f0f7fc'/%3E%3Ctext x='20' y='35' font-family='Georgia' font-size='18' fill='%23555'%3E%22Desde 1998 llevamos la cocina italiana a la mesa.%22%3C/text%3E%3C/svg%3E"
        alt="" style={{ display: 'block', margin: '15px 0', width: '100%' }}
      />

      <p style={{ fontSize: 12, color: '#aaa' }}>El Sauce nació en 1998 de la mano de la familia Giordano.</p>

      <h3 style={{ color: '#aaa', margin: '20px 0 10px' }}>Nuestros valores</h3>
      <div className="cards-grid">
        {['Producto de estación', 'Kilómetro cero', 'Cero desperdicio'].map(v => (
          <div key={v} className="card">
            <div className="card-body">
              <h5>{v}</h5>
            </div>
          </div>
        ))}
      </div>

      <h3 style={{ color: '#aaa', marginBottom: 10 }}>El equipo</h3>
      <table>
        <tr><td>Nombre</td><td>Rol</td><td>Desde</td><td>Estado</td></tr>
        <tr><td>Marco Giordano</td><td>Chef ejecutivo</td><td>1998</td><td style={{ color: '#66bb6a' }}>●</td></tr>
        <tr><td>Valentina Giordano</td><td>Directora de sala</td><td>1998</td><td style={{ color: '#66bb6a' }}>●</td></tr>
        <tr><td>Lucía Fernández</td><td>Sous chef</td><td>2015</td><td style={{ color: '#66bb6a' }}>●</td></tr>
        <tr><td>Tomás Rivas</td><td>Sommelier</td><td>2019</td><td style={{ color: '#ef9a9a' }}>●</td></tr>
        <tr><td>Carla Medina</td><td>Pastelera</td><td>2021</td><td style={{ color: '#66bb6a' }}>●</td></tr>
      </table>
      <p style={{ fontSize: 11, color: '#ccc' }}>El color indica disponibilidad.</p>
    </>
  );
}
