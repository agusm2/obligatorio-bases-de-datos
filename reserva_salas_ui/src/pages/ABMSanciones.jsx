import { useNavigate } from "react-router-dom";
import Table from "react-bootstrap/Table";
import Button from "react-bootstrap/Button";

import pencilImg from "../assets/pencil-solid-full.svg";
import trashImg from "../assets/trash-solid-full.svg";

export default function ABMSanciones() {
  const navigate = useNavigate();

  return (
    <>
      <h2>Sanciones</h2>
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
              <th>CI</th>
              <th>Nombre</th>
              <th>Apellido</th>
              <th>Fecha inicio</th>
              <th>Fecha fin</th>
              <th style={{ textAlign: "center" }}>Editar/Eliminar</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1234567-8</td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td
                style={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  gap: "10px",
                }}
              >
                <button style={{ borderRadius: 5 }}>
                  <img
                    src={pencilImg}
                    style={{
                      width: "50px",
                      height: "20px",
                    }}
                  />
                </button>
                <button style={{ borderRadius: 5 }}>
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
            <tr>
              <td>1234567-8</td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td
                style={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  gap: "10px",
                }}
              >
                <button style={{ borderRadius: 5 }}>
                  <img
                    src={pencilImg}
                    style={{
                      width: "50px",
                      height: "20px",
                    }}
                  />
                </button>
                <button style={{ borderRadius: 5 }}>
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
    </>
  );
}
