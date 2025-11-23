import { Link, useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";

import userImg from "../assets/user-solid-full.svg";
import buildingImg from "../assets/building-solid-full.svg";
import banImg from "../assets/ban-solid-full.svg";
import calendarImg from "../assets/calendar-check-solid-full.svg";
import { useAuth } from "../contexts/AuthContext";

export default function Admin() {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/");
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
      <h2 style={{ marginBottom: 40 }}>Bienvenido {user?.correo}</h2>
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
      <div>
        <Button
          variant="outline-danger"
          onClick={() => handleLogout()}
          style={{ marginTop: 30, marginRight: 20 }}
        >
          Cerrar Sesión
        </Button>
        <Button
          variant="outline-primary"
          onClick={() => navigate("/admin/reportes")}
          style={{ marginTop: 30 }}
        >
          Reportes
        </Button>
      </div>
    </div>
  );
}
