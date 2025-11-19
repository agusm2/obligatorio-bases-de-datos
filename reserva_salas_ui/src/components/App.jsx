import { BrowserRouter, Route, Routes } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

import Login from "../pages/Login";
import Admin from "../pages/Admin";
import User from "../pages/User";
import ABMParticipantes from "../pages/ABMParticipantes";
import ABMSalas from "../pages/ABMSalas";
import ABMReservas from "../pages/ABMReservas";
import ABMSanciones from "../pages/ABMSanciones";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/admin" element={<Admin />} />
        <Route path="/user" element={<User />} />
        <Route path="/admin/participantes" element={<ABMParticipantes />} />
        <Route path="/admin/salas" element={<ABMSalas />} />
        <Route path="/admin/reservas" element={<ABMReservas />} />
        <Route path="/admin/sanciones" element={<ABMSanciones />} />
      </Routes>
    </BrowserRouter>
  );
}
