import { useNavigate } from "react-router-dom";
import Table from "react-bootstrap/Table";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";

import pencilImg from "../assets/pencil-solid-full.svg";
import trashImg from "../assets/trash-solid-full.svg";
import usersImg from "../assets/users-solid-full.svg";
import { useEffect, useState } from "react";

export default function ABMReservas() {
  const navigate = useNavigate();
  const [reservas, setReservas] = useState([]);

  const [showEdit, setShowEdit] = useState(false);
  const [showParticipantes, setShowParticipantes] = useState(false);

  const [reservaSeleccionada, setReservaSeleccionada] = useState(null);

  const [editData, setEditData] = useState({
    id_reserva: "",
    nombre_sala: "",
    edificio: "",
    fecha: "",
    estado: "",
  });

  function handleEditChange(e) {
    setEditData({
      ...editData,
      [e.target.name]: e.target.value,
    });
  }

  const handleCloseEdit = () => setShowEdit(false);
  const handleShowEdit = (reserva) => {
    setEditData({
      id_reserva: reserva.id_reserva,
      nombre_sala: reserva.nombre_sala,
      edificio: reserva.edificio,
      fecha: reserva.fecha,
      estado: reserva.estado,
    });
    setShowEdit(true);
  };
  const handleCloseParticipantes = () => {
    setShowParticipantes(false);
    setReservaSeleccionada(null);
  };
  const handleShowParticipantes = (reserva) => {
    setReservaSeleccionada(reserva);
    setShowParticipantes(true);
  };

  async function getReservas() {
    const res = await fetch("http://localhost:5000/reservation/");
    const data = await res.json();
    setReservas(data);
  }

  async function updateReserva() {
    try {
      const res = await fetch(
        `http://localhost:5000/reservation/${editData.id_reserva}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            estado: editData.estado,
          }),
        }
      );

      if (!res.ok) {
        throw new Error("Error al modificar reserva");
      }

      await res.json();

      setShowEdit(false);
      getReservas();
    } catch (err) {
      console.error(err);
    }
  }

  async function eliminarReserva(id_reserva) {
    const res = await fetch(`http://localhost:5000/reservation/${id_reserva}`, {
      method: "DELETE",
    });
    if (!res.ok) {
      throw new Error("Error al eliminar reserva");
    }
    getReservas();
    return true;
  }

  async function modificarAsistencia(
    id_reserva,
    ci_participante,
    asistenciaActual
  ) {
    try {
      const nuevaAsistencia = !asistenciaActual;

      const res = await fetch(
        `http://localhost:5000/reservation/${id_reserva}/participants/${ci_participante}/asistencia`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ asistencia: nuevaAsistencia }),
        }
      );

      if (!res.ok) {
        throw new Error("Error al modificar asistencia");
      }
      await getReservas();

      setReservaSeleccionada((prev) => ({
        ...prev,
        participants: prev.participants.map((p) =>
          p.ci_participante === ci_participante
            ? { ...p, asistencia: nuevaAsistencia }
            : p
        ),
      }));
    } catch (error) {
      console.error(error);
    }
  }

  async function sancionarParticipante(ci_participante) {
    try {
      const res = await fetch(
        `http://localhost:5000/participant/${ci_participante}/sancion`,
        { method: "POST" }
      );

      if (!res.ok) {
        throw new Error("Error al sancionar participante");
      }

      alert(
        `Participante con cédula ${ci_participante} sancionado correctamente`
      );

      await getReservas();
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    getReservas();
  }, []);

  return (
    <>
      <h2 style={{ textAlign: "center", marginTop: 30 }}>Reservas</h2>
      <div style={{ width: "50%", margin: "0 auto", padding: 0 }}>
        <Table
          striped
          bordered
          hover
          variant="dark"
          size="sm"
          className="rounded-3 overflow-hidden"
        >
          <thead>
            <tr>
              <th style={{ textAlign: "center" }}>Participante/s</th>
              <th>Nombre sala</th>
              <th>Edificio</th>
              <th>Fecha</th>
              <th>Estado</th>
              <th style={{ textAlign: "center" }}>Editar/Eliminar</th>
            </tr>
          </thead>
          <tbody>
            {reservas.map((r) => (
              <tr key={r.id_reserva}>
                <td
                  style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                  }}
                >
                  <button
                    style={{ borderRadius: 5 }}
                    onClick={() => handleShowParticipantes(r)}
                  >
                    <img
                      src={usersImg}
                      style={{
                        width: "50px",
                        height: "20px",
                      }}
                    />
                  </button>
                </td>
                <td>{r.nombre_sala}</td>
                <td>{r.edificio}</td>
                <td>{r.fecha}</td>
                <td>{r.estado}</td>
                <td
                  style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    gap: "10px",
                  }}
                >
                  <button
                    style={{ borderRadius: 5 }}
                    onClick={() => handleShowEdit(r)}
                  >
                    <img
                      src={pencilImg}
                      style={{
                        width: "50px",
                        height: "20px",
                      }}
                    />
                  </button>
                  <button
                    style={{ borderRadius: 5 }}
                    onClick={() => eliminarReserva(r.id_reserva)}
                  >
                    <img
                      src={trashImg}
                      style={{
                        width: "50px",
                        height: "20px",
                      }}
                    />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
      <div style={{ display: "flex", justifyContent: "center", gap: "10px" }}>
        <Button
          variant="outline-primary"
          style={{ width: 100 }}
          onClick={() => navigate("/admin")}
        >
          Inicio
        </Button>
      </div>

      <Modal show={showEdit} onHide={handleCloseEdit}>
        <Modal.Header closeButton>
          <Modal.Title>Modificar reserva</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group>
              <Form.Label>Actualizar estado</Form.Label>
              <Form.Select
                name="estado"
                value={editData.estado}
                onChange={handleEditChange}
              >
                <option value="">Seleccione un nuevo estado...</option>
                <option value="activa">Activa</option>
                <option value="cancelada">Cancelada</option>
                <option value="sin asistencia">Sin asistencia</option>
                <option value="finalizada">Finalizada</option>
              </Form.Select>
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer className="d-flex justify-content-center">
          <Button variant="primary" onClick={updateReserva}>
            Modificar reserva
          </Button>
        </Modal.Footer>
      </Modal>

      <Modal show={showParticipantes} onHide={handleCloseParticipantes}>
        <Modal.Header closeButton>
          <Modal.Title>Participante/s</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {reservaSeleccionada && reservaSeleccionada.participants ? (
            reservaSeleccionada.participants.map((p, index) => (
              <div key={p.ci_participante}>
                <h5>
                  <strong>Participante {index + 1}</strong>
                </h5>
                <div style={{ marginBottom: 5 }}>
                  <strong>Participante.</strong> {p.nombre} {p.apellido}
                </div>
                <strong>CI.</strong> {p.ci_participante}
                <div style={{ marginBottom: 10, marginTop: 5 }}>
                  <strong>Asistencia.</strong> {p.asistencia ? "✅" : "❌"}
                </div>
                <div>
                  <button
                    style={{ borderRadius: 5 }}
                    disabled={p.asistencia}
                    onClick={() => sancionarParticipante(p.ci_participante)}
                  >
                    Sancionar
                  </button>
                  <button
                    style={{ borderRadius: 5, marginLeft: 5 }}
                    onClick={() =>
                      modificarAsistencia(
                        reservaSeleccionada.id_reserva,
                        p.ci_participante,
                        p.asistencia
                      )
                    }
                  >
                    Modificar asistencia
                  </button>
                </div>
              </div>
            ))
          ) : (
            <p>No hay participantes para esta reserva.</p>
          )}
        </Modal.Body>
      </Modal>
    </>
  );
}
