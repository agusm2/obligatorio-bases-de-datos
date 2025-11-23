import { useNavigate } from "react-router-dom";
import Table from "react-bootstrap/Table";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";

import pencilImg from "../assets/pencil-solid-full.svg";
import trashImg from "../assets/trash-solid-full.svg";

import { useEffect, useState } from "react";

export default function ABMParticipantes() {
  const navigate = useNavigate();
  const [participantes, setParticipantes] = useState([]);
  const [show, setShow] = useState(false);
  const [showEdit, setShowEdit] = useState(false);
  const [reservas, setReservas] = useState([]);
  const [programas, setProgramas] = useState([]);
  const [editData, setEditData] = useState({
    ci: "",
    nombre: "",
    apellido: "",
    email: "",
  });
  const [formData, setFormData] = useState({
    ci: "",
    name: "",
    surname: "",
    email: "",
    password: "",
    programa: "",
    rol: "",
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

  function handleShowEdit(participante) {
    setEditData({
      ci: participante.ci,
      nombre: participante.nombre,
      apellido: participante.apellido,
      email: participante.email,
    });

    setShowEdit(true);
  }

  function limpiarForm() {
    setFormData({
      ci: "",
      name: "",
      surname: "",
      email: "",
      password: "",
      programa: "",
      rol: "",
    });
  }

  function tieneReservaActiva(ci) {
    return reservas.some(
      (r) =>
        r.estado === "activa" &&
        r.participants.some((part) => part.ci_participante === ci)
    );
  }

  async function getReservas() {
    const res = await fetch("http://localhost:5000/reservation/");
    const data = await res.json();
    setReservas(data);
  }

  async function getParticipantes() {
    const res = await fetch("http://localhost:5000/participant/");
    const data = await res.json();
    setParticipantes(data);
  }

  async function updateParticipante(ci, nuevoMail) {
    const res = await fetch(`http://localhost:5000/participant/${ci}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email: nuevoMail }),
    });

    if (!res.ok) {
      throw new Error("Error al actualizar participante");
    }

    return await res.json();
  }

  async function createParticipante() {
    const payload = {
      ci: formData.ci,
      name: formData.name,
      surname: formData.surname,
      email: formData.email,
      password: formData.password,
      programas: [
        {
          nombre_programa: formData.programa,
          rol: formData.rol,
        },
      ],
    };

    try {
      const res = await fetch("http://localhost:5000/participant/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        alert("Error creando participante");
        return;
      }

      alert("Participante creado");
      limpiarForm();
      handleClose();
      getParticipantes();
    } catch (err) {
      console.error(err);
      alert("Error inesperado");
    }
  }

  async function eliminarParticipante(ci) {
    const res = await fetch(`http://localhost:5000/participant/${ci}`, {
      method: "DELETE",
    });
    if (!res.ok) {
      throw new Error("Error eliminando participante");
    }

    return true;
  }

  async function handleUpdateClick() {
    try {
      await updateParticipante(editData.ci, editData.email);
      setShowEdit(false);
      getParticipantes();
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    getParticipantes();
    getReservas();
  }, []);

  return (
    <>
      <h2 style={{ textAlign: "center", marginTop: 30 }}>Participantes</h2>
      <div style={{ width: "60%", margin: "0 auto", padding: 0 }}>
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
              <th>C.I</th>
              <th>Nombre</th>
              <th>Apellido</th>
              <th>Mail</th>
              <th>Programa</th>
              <th>Tipo</th>
              <th>Rol</th>
              <th style={{ textAlign: "center" }}>Editar/Eliminar</th>
            </tr>
          </thead>
          <tbody>
            {participantes.map((p) => (
              <tr key={p.ci}>
                <td>{p.ci}</td>
                <td>{p.nombre}</td>
                <td>{p.apellido}</td>
                <td>{p.email}</td>
                <td>
                  {p.programas && p.programas.length > 0
                    ? p.programas[0].nombre_programa
                    : "-"}
                </td>
                <td>
                  {p.programas && p.programas.length > 0
                    ? p.programas[0].tipo
                    : "-"}
                </td>
                <td>
                  {p.programas && p.programas.length > 0
                    ? p.programas[0].rol
                    : "-"}
                </td>
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
                    onClick={() => handleShowEdit(p)}
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
                    onClick={() => {
                      if (tieneReservaActiva(p.ci)) {
                        alert(
                          "No se puede eliminar un participantes con reservas activas"
                        );
                        return;
                      }

                      eliminarParticipante(p.ci)
                        .then(() => {
                          getParticipantes();
                          getReservas();
                        })
                        .catch((err) => console.error(err));
                    }}
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
          style={{ width: 100 }}
          variant="outline-primary"
          onClick={() => navigate("/admin")}
        >
          Inicio
        </Button>

        <Button variant="outline-success" onClick={handleShow}>
          Nuevo participante
        </Button>
      </div>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Crear participante</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>C.I.</Form.Label>
              <Form.Control
                type="text"
                name="ci"
                value={formData.ci}
                onChange={handleChange}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Nombre</Form.Label>
              <Form.Control
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Apellido</Form.Label>
              <Form.Control
                type="text"
                name="surname"
                value={formData.surname}
                onChange={handleChange}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Mail</Form.Label>
              <Form.Control
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Contraseña</Form.Label>
              <Form.Control
                type="text"
                name="password"
                value={formData.password}
                onChange={handleChange}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Programa académico</Form.Label>
              <Form.Select
                name="programa"
                value={formData.programa}
                onChange={handleChange}
              >
                <option value="">Seleccione un programa...</option>
                <option value="Ingeniería informática">
                  Ingeniería informática
                </option>
                <option value="Científico">Científico</option>
                <option value="Experto en ciberseguridad">
                  Experto en ciberseguridad
                </option>
              </Form.Select>
            </Form.Group>

            <Form.Group>
              <Form.Label>Rol</Form.Label>
              <Form.Select
                name="rol"
                value={formData.rol}
                onChange={handleChange}
              >
                <option value="">Seleccione un rol...</option>
                <option value="alumno">Alumno</option>
                <option value="docente">Docente</option>
              </Form.Select>
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer className="d-flex justify-content-center">
          <Button variant="primary" onClick={createParticipante}>
            Crear Participante
          </Button>
        </Modal.Footer>
      </Modal>

      <Modal show={showEdit} onHide={() => setShowEdit(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Modificar participante</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <Form>
            <Form.Group>
              <Form.Label>Ingrese nuevo mail</Form.Label>
              <Form.Control
                type="email"
                name="email"
                value={editData.email}
                onChange={handleEditChange}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer className="d-flex justify-content-center">
          <Button variant="primary" onClick={handleUpdateClick}>
            Modificar participante
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
