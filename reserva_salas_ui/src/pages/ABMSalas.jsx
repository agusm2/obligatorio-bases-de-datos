import { useNavigate } from "react-router-dom";
import Table from "react-bootstrap/Table";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";

import pencilImg from "../assets/pencil-solid-full.svg";
import trashImg from "../assets/trash-solid-full.svg";
import { useEffect, useState } from "react";

export default function ABMSalas() {
  const navigate = useNavigate();
  const [salas, setSalas] = useState([]);
  const [show, setShow] = useState(false);
  const [showEdit, setShowEdit] = useState(false);
  const [editData, setEditData] = useState({
    name: "",
    building: "",
    room_type: "",
    capacity: "",
  });
  const [formData, setFormData] = useState({
    name: "",
    building: "",
    room_type: "",
    capacity: "",
  });

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  function handleChange(e) {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  }

  function handleEditChange(e) {
    setEditData({
      ...editData,
      [e.target.name]: e.target.value,
    });
  }

  function handleShowEdit(sala) {
    setEditData({
      name: sala.nombre_sala,
      building: sala.edificio,
      room_type: sala.tipo_sala,
      capacity: sala.capacidad,
    });

    setShowEdit(true);
  }

  function limpiarForm() {
    setFormData({
      name: "",
      building: "",
      room_type: "",
      capacity: "",
    });
  }

  async function getSalas() {
    const res = await fetch("http://localhost:5000/classroom/");
    const data = await res.json();
    setSalas(data);
  }

  async function updateSala() {
    try {
      const res = await fetch(
        `http://localhost:5000/classroom/${editData.name}/${editData.building}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            capacity: Number(editData.capacity),
            room_type: editData.room_type,
          }),
        }
      );

      if (!res.ok) {
        throw new Error("Error al modificar la sala");
      }

      await res.json();

      setShowEdit(false);
      getSalas();
    } catch (err) {
      console.error(err);
    }
  }

  async function createSala() {
    try {
      const res = await fetch("http://localhost:5000/classroom/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: formData.name,
          building: formData.building,
          capacity: Number(formData.capacity),
          room_type: formData.room_type,
        }),
      });

      if (!res.ok) {
        alert("Error al crear sala");
        return;
      }

      alert("Sala creada");
      limpiarForm();
      handleClose();
      getSalas();
    } catch (err) {
      console.error(err);
    }
  }

  async function eliminarSala(name, building) {
    const res = await fetch(
      `http://localhost:5000/classroom/${name}/${building}`,
      {
        method: "DELETE",
      }
    );
    if (!res.ok) {
      throw new Error("Error al eliminar la sala");
    }
    getSalas();
    return true;
  }

  useEffect(() => {
    getSalas();
  }, []);

  return (
    <>
      <h2 style={{textAlign: "center", marginTop: 30}}>Salas</h2>
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
              <th>Nombre</th>
              <th>Edificio</th>
              <th>Capacidad</th>
              <th>Tipo</th>
              <th style={{ textAlign: "center" }}>Editar/Eliminar</th>
            </tr>
          </thead>
          <tbody>
            {salas.map((s) => (
              <tr key={s.nombre_sala}>
                <td>{s.nombre_sala}</td>
                <td>{s.edificio}</td>
                <td>{s.capacidad}</td>
                <td style={{ textTransform: "capitalize" }}>{s.tipo_sala}</td>
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
                    onClick={() => handleShowEdit(s)}
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
                    onClick={() => eliminarSala(s.nombre_sala, s.edificio)}
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

        <Button variant="outline-success" onClick={handleShow}>
          Nueva sala
        </Button>
      </div>

      <Modal show={showEdit} onHide={() => setShowEdit(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Modificar sala</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <Form>
            <Form.Group>
              <Form.Label>Actualizar capacidad</Form.Label>
              <Form.Control
                type="number"
                name="capacity"
                value={editData.capacity}
                onChange={handleEditChange}
              />
            </Form.Group>
            <Form.Group>
              <Form.Label>Actualizar tipo de sala</Form.Label>
              <Form.Control
                type="text"
                name="room_type"
                value={editData.room_type}
                onChange={handleEditChange}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer className="d-flex justify-content-center">
          <Button variant="primary" onClick={updateSala}>
            Modificar sala
          </Button>
        </Modal.Footer>
      </Modal>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Crear sala</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Nombre sala</Form.Label>
              <Form.Control
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Edificio</Form.Label>
              <Form.Control
                type="text"
                name="building"
                value={formData.building}
                onChange={handleChange}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Capacidad</Form.Label>
              <Form.Control
                type="number"
                name="capacity"
                value={formData.capacity}
                onChange={handleChange}
              />
            </Form.Group>

            <Form.Group>
              <Form.Label>Tipo</Form.Label>
              <Form.Control
                type="text"
                name="room_type"
                value={formData.room_type}
                onChange={handleChange}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer className="d-flex justify-content-center">
          <Button variant="primary" onClick={createSala}>
            Crear sala
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
