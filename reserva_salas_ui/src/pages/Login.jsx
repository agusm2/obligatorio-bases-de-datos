import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

export default function Login() {
  const handleLogin = async (e) => {
    e.preventDefault();

    const user = e.target.user.value;
    const passwd = e.target.password.value;
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
              placeholder="Ingrese su usuario..."
            />
          </Form.Group>
          <Form.Group controlId="password" className="mb-3">
            <Form.Label>Contraseña</Form.Label>
            <Form.Control
              type="password"
              name="password"
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
