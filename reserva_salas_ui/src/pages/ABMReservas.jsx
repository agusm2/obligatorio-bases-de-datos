import { useNavigate } from "react-router-dom";
import Table from "react-bootstrap/Table";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";

import pencilImg from "../assets/pencil-solid-full.svg";
import trashImg from "../assets/trash-solid-full.svg";
import { useEffect, useState } from "react";

export default function ABMReservas() {
  const navigate = useNavigate();
  const [reservas, setReservas] = useState([]);
  const [showEdit, setShowEdit] = useState(false);
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

  function handleShowEdit(reserva) {
    setEditData({
      id_reserva: reserva.id_reserva,
      nombre_sala: reserva.nombre_sala,
      edificio: reserva.edificio,
      fecha: reserva.fecha,
      estado: reserva.estado,
    });

    setShowEdit(true);
  }

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

  useEffect(() => {
    getReservas();
  }, []);

  return (
    <>
      <h2 style={{textAlign: "center", marginTop: 30}}>Reservas</h2>
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
              <th>Participante</th>
              <th>Nombre sala</th>
              <th>Edificio</th>
              <th>Fecha</th>
              <th>Estado</th>
              <th>Asistencia</th>
              <th style={{ textAlign: "center" }}>Editar/Eliminar</th>
            </tr>
          </thead>
          <tbody>
            {reservas.map((r) => (
              <tr key={r.id_reserva}>
                <td>{}</td>
                <td>{r.nombre_sala}</td>
                <td>{r.edificio}</td>
                <td>{r.fecha}</td>
                <td>{r.estado}</td>
                <td>{}</td>
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

      <Modal show={showEdit} onHide={() => setShowEdit(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Modificar reserva</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group>
              <Form.Label>Actualizar estado</Form.Label>
              <Form.Control
                type="text"
                name="estado"
                value={editData.estado}
                onChange={handleEditChange}
              />
            </Form.Group>
            <Form.Group>
              <Form.Label>Actualizar asistencia</Form.Label>
              <Form.Control
                type="text"
                name="asistencia"
                value="aca iria asistencia"
                onChange={handleEditChange}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer className="d-flex justify-content-center">
          <Button variant="primary" onClick={updateReserva}>
            Modificar reserva
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

//estado
//asistencia
//fecha??
