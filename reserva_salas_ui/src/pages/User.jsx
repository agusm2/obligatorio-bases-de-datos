import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { useAuth } from "../contexts/AuthContext";

export default function User() {
  const navigate = useNavigate();

  const [sala, setSala] = useState(null);
  const [salas, setSalas] = useState([]);
  const [capacidad, setCapacidad] = useState(1);
  const [fecha, setFecha] = useState("");
  const [turnoId, setTurnoId] = useState("");
  const [turnos, setTurnos] = useState([]);

  const [showReservas, setShowReservas] = useState(false);
  const [showParticipantes, setShowParticipantes] = useState(false);

  const handleCloseReservas = () => setShowReservas(false);
  const handleShowReservas = () => setShowReservas(true);

  const { logout, user } = useAuth();

  const handleSubmit = async (e) => {
    //Acá valido datos y hago el POST si esta todo OK
  };

  function handleLogout() {
    logout();
    navigate("/");
  }

  async function getSalas() {
    const res = await fetch("http://localhost:5000/classroom/");
    const data = await res.json();
    setSalas(data);
  }

  useEffect(() => {
    getSalas();
  }, []);

  useEffect(() => {
    if (!sala || !fecha) {
      setTurnos([]);
      setTurnoId("");
      return;
    }

    const getTurnos = async () => {
      try {
        const res = await fetch(
          `http://localhost:5000/classroom/${sala.name}/${sala.building}/available?date=${fecha}`
        );
        if (!res.ok) {
          console.log("Error al obtener turnos disponibles");
          setTurnos([]);
          return;
        }

        const data = await res.json();
        setTurnos(data);
        setTurnoId("");
      } catch (error) {
        console.error("Error al obtener turnos");
        setTurnos([]);
      }
    };

    getTurnos();
  }, [sala, fecha]);

  return (
    <>
      <h1 style={{ textAlign: "center", marginTop: 20 }}>Bienvenido {user}</h1>
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
              value={sala?.nombre_sala || ""}
              onChange={(e) => {
                const selected = salas.find(
                  (x) => x.nombre_sala === e.target.value
                );
                setSala(selected || null);
                if (selected && capacidad > selected.capacidad) {
                  setCapacidad(selected.capacidad);
                }
              }}
              name="sala"
            >
              <option value="">Seleccione...</option>

              {salas.map((s) => (
                <option key={s.nombre_sala} value={s.nombre_sala}>
                  {s.nombre_sala}
                </option>
              ))}
            </Form.Select>
          </Form.Group>
          <Form.Group controlId="participantes" className="mb-3">
            <Form.Label>Participantes</Form.Label>
            <Form.Control
              type="number"
              value={capacidad}
              onChange={(e) => setCapacidad(Number(e.target.value))}
              min={1}
              max={sala?.capacidad || 1}
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
              value={turnoId}
              onChange={(e) => setTurnoId(e.target.value)}
              name="horario"
            >
              <option value="">
                {!sala || !fecha
                  ? "Seleccione sala y fecha primero"
                  : turnos.length === 0
                  ? "No hay turnos disponibles"
                  : "Seleccione..."}
              </option>
              {turnos.map((t) => (
                <option key={t.id_turno} value={t.id_turno}>
                  {t.hora_inicio} - {t.hora_fin}
                </option>
              ))}
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
