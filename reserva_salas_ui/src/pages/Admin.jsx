import { Link, useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";

import userImg from "../assets/user-solid-full.svg";
import buildingImg from "../assets/building-solid-full.svg";
import banImg from "../assets/ban-solid-full.svg";
import calendarImg from "../assets/calendar-check-solid-full.svg";

export default function Admin() {
  const navigate = useNavigate();

  function handleLogout() {
    navigate("/");
    //Función para cerrar sesión (ver de hacer una global y reutilizarla)
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginTop: 50,
      }}
    >
      <h2 style={{ marginBottom: 40 }}>Bienvenido ADMIN</h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "20px",
          width: "400px",
        }}
      >
        <button
          onClick={() => navigate("/admin/participantes")}
          style={{ background: "none", border: "none", cursor: "pointer" }}
        >
          <img src={userImg} width={150} />
          <p>Participantes</p>
        </button>

        <button
          onClick={() => navigate("/admin/salas")}
          style={{ background: "none", border: "none", cursor: "pointer" }}
        >
          <img src={buildingImg} width={150} />
          <p>Salas</p>
        </button>

        <button
          onClick={() => navigate("/admin/reservas")}
          style={{ background: "none", border: "none", cursor: "pointer" }}
        >
          <img src={calendarImg} width={150} />
          <p>Reservas</p>
        </button>

        <button
          onClick={() => navigate("/admin/sanciones")}
          style={{ background: "none", border: "none", cursor: "pointer" }}
        >
          <img src={banImg} width={150} />
          <p>Sanciones</p>
        </button>
      </div>
      <Button
        variant="outline-danger"
        onClick={() => handleLogout()}
        style={{ marginTop: 30 }}
      >
        Cerrar Sesión
      </Button>
    </div>
  );
}
