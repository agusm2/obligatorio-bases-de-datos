import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { useAuth } from "../contexts/AuthContext";

export default function User() {
  const [sala, setSala] = useState("");
  const [capacidad, setCapacidad] = useState(1);
  const [fecha, setFecha] = useState("");
  const [horario, setHorario] = useState("");
  const navigate = useNavigate();
  const { logout, user } = useAuth();

  const handleSubmit = async (e) => {
    //Acá valido datos y hago el POST si esta todo OK
  };

  function handleLogout() {
    logout();
    navigate("/");
  }

  return (
    <>
      <h1 style={{ textAlign: "center", marginTop: 20 }}>Bienvenido USER</h1>
      {/* <h2 style={{ textAlign: "center", color: "red" }}>
        Usted esta sancionado hasta el DATE
      </h2> */}

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
        }}
      >

        <Form
          onSubmit={handleSubmit}
          style={{
            display: "flex",
            flexDirection: "column",
            width: "300px",
          }}
        >
          <Form.Group controlId="Sala" className="mb-3">
            <Form.Label>Sala</Form.Label>
            <Form.Select
              value={sala}
              onChange={(e) => setSala(e.target.value)}
              name="sala"
            >
              <option value="">Seleccione...</option>
              <option value="101">Sala 101</option>
              <option value="102">Sala 102</option>
              <option value="103">Sala 103</option>
            </Form.Select>
          </Form.Group>
          <Form.Group controlId="participantes" className="mb-3">
            <Form.Label>Participantes</Form.Label>
            <Form.Control
              type="number"
              value={capacidad}
              onChange={(e) => setCapacidad(Number(e.target.value))}
              min={1}
            />
          </Form.Group>
          <Form.Group controlId="fecha" className="mb-3">
            <Form.Label>Fecha</Form.Label>
            <Form.Control
              type="date"
              value={fecha}
              onChange={(e) => setFecha(e.target.value)}
              name="fecha"
            />
          </Form.Group>
          <Form.Group controlId="horario">
            <Form.Label>Horario</Form.Label>
            <Form.Select
              value={horario}
              onChange={(e) => setHorario(e.target.value)}
              name="horario"
            >
              <option value="">Seleccione...</option>
              <option value="8-9">8:00 AM - 9:00 AM</option>
              <option value="9-10">9:00 AM - 10:00 AM</option>
              <option value="10-11">10:00 AM - 11:00 AM</option>
            </Form.Select>
          </Form.Group>
          <Button variant="outline-primary" type="submit" className="mt-3">
            Reservar
          </Button>
        </Form>
      </div>

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          marginTop: 20,
          gap: 10,
        }}
      >
        <Button variant="outline-danger" onClick={handleLogout}>
          Cerrar sesión
        </Button>
        <Button variant="outline-success">Ver reservas activas</Button>
      </div>
    </>
  );
}

/* 
Si participantes es > 1 abro modal para llenar datos de todos los participantes adicionales al usuario
*/
/* 
Si user quiere ver las reservas, abro un modal con todas sus reservas, si no tiene le muestro un mensaje indicandole
*/
