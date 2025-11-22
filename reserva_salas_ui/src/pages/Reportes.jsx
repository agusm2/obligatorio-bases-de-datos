import Button from "react-bootstrap/Button";
import { useNavigate } from "react-router-dom";

export default function Reportes() {
  const navigate = useNavigate();

  return (
    <div>
      <h1>Reportes</h1>
      <h5>Salas más reservadas</h5>
      <h5>Turnos más demandados</h5>
      <h5>Pormedio de participantes por sala</h5>
      <h5>Cantidad de reservas por carrera y facultad</h5>
      <h5>Porcentaje de ocupación de salas por edificios</h5>
      <h5>
        Cantidad de reservas y asistencias de profesores y alumnos (grado y
        posgrado)
      </h5>
      <h5>
        Cantidad de sacniones para profesores y alumnos (grado y posgrado)
      </h5>
      <h5>
        Porcentaje de reservas efectivamente utilizadas vs. canceladas/no
        asistidas
      </h5>
      <h5>Cantidad de participantes sancionados más de una vez</h5>
      <h5>Usuarios que más cancelan o no asisten a sus reservas</h5>
      <h5>Salas con menor uso</h5>

      <Button
        style={{ width: 100 }}
        variant="outline-primary"
        onClick={() => navigate("/admin")}
      >
        Inicio
      </Button>
    </div>
  );
}
