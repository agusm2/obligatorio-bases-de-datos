import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
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
  const [ciUsuario, setCiUsuario] = useState("");

  const [showReservas, setShowReservas] = useState(false);
  const [showParticipantes, setShowParticipantes] = useState(false);

  const [reservas, setReservas] = useState([]);

  const [participantesExtra, setParticipantesExtra] = useState([]);

  const handleCloseReservas = () => setShowReservas(false);

  const handleCloseParticipantes = () => setShowParticipantes(false);

  const { logout, user } = useAuth();

  const formatDate = (date) => date.toISOString().split("T")[0];

  const today = new Date();
  const max = new Date();

  max.setDate(today.getDate() + 7);

  const minDate = formatDate(today);
  const maxDate = formatDate(max);

  const reservar = async () => {
    const participantesFinales = [ciUsuario, ...participantesExtra];

    const payload = {
      classroom_name: sala.nombre_sala,
      building: sala.edificio,
      date: fecha,
      id_turn: Number(turnoId),
      participants: participantesFinales,
    };

    try {
      const res = await fetch("http://localhost:5000/reservation/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        alert("Error al crear la reserva");
        return;
      }

      alert("Reserva creada correctamente");

      setParticipantesExtra([]);
      setSala(null);
      setFecha("");
      setTurnoId("");
      setCapacidad(1);
      setCiUsuario("");
      setShowParticipantes(false);
    } catch (err) {
      console.error(err);
      alert("Error inesperado");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!sala || !fecha || !turnoId || !ciUsuario) {
      alert("Se deben completar todos los campos");
      return;
    }

    if (capacidad > 1 && participantesExtra.length !== capacidad - 1) {
      setShowParticipantes(true);
      return;
    }

    await reservar();
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
          `http://localhost:5000/classroom/${sala.nombre_sala}/${sala.edificio}/available?date=${fecha}`
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

  async function cargarReservas() {
    const res = await fetch(
      `http://localhost:5000/reservation/participant/${user.ci}`
    );
    const data = await res.json();
    setReservas(data);
  }

  const programas = user?.programas || [];

  const esDocente = programas.some((p) => p.rol === "docente");
  const esAlumnoPosgrado = programas.some(
    (p) => p.rol === "alumno" && p.tipo === "posgrado"
  );

  const salasFiltradas = salas.filter((s) => {
    if (s.tipo_sala === "libre") return true;

    if (s.tipo_sala === "posgrado") {
      return esDocente || esAlumnoPosgrado;
    }

    if (s.tipo_sala === "docente") {
      return esDocente;
    }

    return false;
  });

  return (
    <>
      <h1 style={{ textAlign: "center", marginTop: 20 }}>
        Bienvenido {user?.correo}
      </h1>

      {user?.sancionado && (
        <h2 style={{ textAlign: "center", color: "red" }}>
          Usted está sancionado hasta el{" "}
          {new Date(user?.fecha_fin_sancion).toLocaleDateString()}
          
        </h2>
      )}

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
          <fieldset disabled={user?.sancionado}>
            <Form.Group controlId="Ci" className="mb-3">
              <Form.Label>C.I.</Form.Label>
              <Form.Control
                type="text"
                placeholder="Ingrese su cédula..."
                value={ciUsuario}
                onChange={(e) => setCiUsuario(e.target.value)}
              />
            </Form.Group>

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

                {salasFiltradas.map((s) => (
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
                min={minDate}
                max={maxDate}
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
            <div style={{ display: "flex", justifyContent: "center" }}>
              <Button
                variant="outline-primary"
                type="submit"
                className="mt-3"
                style={{ width: 300 }}
              >
                Reservar
              </Button>
            </div>
          </fieldset>
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
        <Button
          variant="outline-success"
          onClick={() => {
            cargarReservas();
            setShowReservas(true);
          }}
          disabled={user?.sancionado}
        >
          Ver reservas activas
        </Button>
      </div>

      <Modal show={showReservas} onHide={handleCloseReservas}>
        <Modal.Header closeButton>
          <Modal.Title>Reservas activas</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {reservas.length === 0 && <p>No hay reservas activas</p>}
          {reservas.map((r) => (
            <div key={r.id_reserva} style={{ marginBottom: "10px" }}>
              <strong>
                {r.nombre_sala} - {r.edificio}
              </strong>{" "}
              <br />
              Fecha: {new Date(r.fecha).toLocaleDateString()} <br />
              Turno: {r.id_turno}
            </div>
          ))}
        </Modal.Body>
      </Modal>

      <Modal show={showParticipantes} onHide={handleCloseParticipantes}>
        <Modal.Header closeButton>
          <Modal.Title>Ingrese participantes</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {[...Array(capacidad - 1)].map((_, i) => (
            <Form key={i} className="mb-3">
              <h5>Participante {i + 2}</h5>

              <Form.Group className="mb-2">
                <Form.Label>CI</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Cédula..."
                  onChange={(e) => {
                    const copia = [...participantesExtra];
                    copia[i] = e.target.value;
                    setParticipantesExtra(copia);
                  }}
                />
              </Form.Group>
            </Form>
          ))}
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="primary"
            onClick={async () => {
              if (
                participantesExtra.length !== capacidad - 1 ||
                participantesExtra.some((ci) => !ci || ci.trim() === "")
              ) {
                alert("Complete todas las cédulas de los participantes");
                return;
              }
              await reservar();
            }}
          >
            Reservar
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
