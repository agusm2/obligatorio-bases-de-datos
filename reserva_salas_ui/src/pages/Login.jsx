import { useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function Login() {
  const [user, setUser] = useState("");
  const [passwd, setPasswd] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    if(user.trim() === "" || passwd.trim() === "") {
      alert("Se deben llenar todos los campos");
      return;
    }

    const res = await fetch(`http://localhost:5000/${user}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user,
        passwd,
      }),
    });

    if (!res.ok) {
      alert("Usuario o contraseña incorrecto/s");
      return;
    }

    const data = await res.json();

    login(data);
    if (data.tipo_usuario === "admin") {
      navigate("/admin");
    } else {
      navigate("/user");
    }
  };

  return (
    <>
      <h2 style={{ textAlign: "center", marginTop: 50 }}>
        Gestión de Reservas de Salas de Estudio
      </h2>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Form
          onSubmit={handleLogin}
          style={{
            display: "flex",
            flexDirection: "column",
            width: "300px",
            marginTop: 40,
          }}
        >
          <Form.Group controlId="user" className="mb-3">
            <Form.Label>Usuario</Form.Label>
            <Form.Control
              type="text"
              name="user"
              onChange={(e) => setUser(e.target.value)}
              value={user}
              placeholder="Ingrese su usuario..."
            />
          </Form.Group>
          <Form.Group controlId="password" className="mb-3">
            <Form.Label>Contraseña</Form.Label>
            <Form.Control
              type="password"
              name="password"
              value={passwd}
              onChange={(e) => setPasswd(e.target.value)}
              placeholder="Ingrese su contraseña..."
            />
          </Form.Group>
          <Button variant="outline-primary" type="submit">
            Iniciar sesión
          </Button>
        </Form>
      </div>
    </>
  );
}
