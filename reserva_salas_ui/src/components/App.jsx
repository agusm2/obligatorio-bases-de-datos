import { BrowserRouter, Route, Routes } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

import { AuthProvider } from "../contexts/AuthContext";

import Login from "../pages/Login";
import Admin from "../pages/Admin";
import User from "../pages/User";
import ABMParticipantes from "../pages/ABMParticipantes";
import ABMSalas from "../pages/ABMSalas";
import ABMReservas from "../pages/ABMReservas";
import ABMSanciones from "../pages/ABMSanciones";
import ProtectedRoute from "./ProtectedRoute";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />

          <Route
            path="/admin"
            element={
              /* <ProtectedRoute role="admin"> */
                <Admin />
              /* </ProtectedRoute> */
            }
          />

          <Route
            path="/admin/participantes"
            element={
              /* <ProtectedRoute role="admin"> */
                <ABMParticipantes />
              /* </ProtectedRoute> */
            }
          />

          <Route
            path="/admin/salas"
            element={
              /* <ProtectedRoute role="admin"> */
                <ABMSalas />
              /* </ProtectedRoute> */
            }
          />

          <Route
            path="/admin/reservas"
            element={
              /* <ProtectedRoute role="admin"> */
                <ABMReservas />
              /* </ProtectedRoute> */
            }
          />

          <Route
            path="/admin/sanciones"
            element={
              /* <ProtectedRoute role="admin"> */
                <ABMSanciones />
              /* </ProtectedRoute> */
            }
          />

          <Route
            path="/user"
            element={
              /* <ProtectedRoute role="usuario"> */
                <User />
              /* </ProtectedRoute> */
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
