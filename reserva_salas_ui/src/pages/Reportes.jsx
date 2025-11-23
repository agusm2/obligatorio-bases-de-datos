import { useEffect, useState } from "react";
import Button from "react-bootstrap/Button";
import { useNavigate } from "react-router-dom";

export default function Reportes() {
  const navigate = useNavigate();

  const [mostReserved, setMostReserved] = useState(null);
  const [avg, setAvg] = useState(null);
  const [sanctions, setSanctions] = useState([]);
  const [leastUsedRooms, setLeastUsedRooms] = useState([]);
  const [usadasVsCanceladas, setUsadasVsCanceladas] = useState(null);
  const [reservationsAttendance, setReservationsAttendance] = useState([]);
  const [occupationByBuilding, setOccupationByBuilding] = useState([]);
  const [reservationsByProgram, setReservationsByProgram] = useState([]);
  const [participantsMultipleSanctions, setParticipantsMultipleSanctions] =
    useState([]);
  const [usersMostNoShow, setUsersMostNoShow] = useState([]);
  const [mostDemandedTurns, setMostDemandedTurns] = useState([]);

  function capitalize(str) {
    if (!str) return "";
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  function formatHour(timeStr) {
    const [h, m] = timeStr.split(":");
    const hh = h.padStart(2, "0");
    return `${hh}:${m}`;
  }

  async function getMostReserved() {
    const res = await fetch(
      "http://localhost:5000/dashboard/most_reserved_rooms"
    );
    const data = await res.json();
    setMostReserved(data[0] || null);
  }

  async function avgParticipants() {
    const res = await fetch(
      "http://localhost:5000/dashboard/avg_participants_per_room"
    );
    const data = await res.json();
    setAvg(data[0] || null);
  }

  async function getSanctions() {
    const res = await fetch(
      "http://localhost:5000/dashboard/sanctions_by_role_and_type"
    );
    const data = await res.json();
    setSanctions(data);
  }

  async function getLeastUsed() {
    const res = await fetch("http://localhost:5000/dashboard/least_used_rooms");
    const data = await res.json();
    setLeastUsedRooms(data);
  }

  async function getUsadasVsCanceladas() {
    const res = await fetch(
      "http://localhost:5000/dashboard/usage_vs_cancelled"
    );
    const data = await res.json();
    setUsadasVsCanceladas(data[0] || null);
  }

  async function getReservationsAndAttendance() {
    const res = await fetch(
      "http://localhost:5000/dashboard/reservations_and_attendance_by_role_and_type"
    );
    const data = await res.json();
    setReservationsAttendance(data);
  }

  async function getOccupationByBuilding() {
    const res = await fetch(
      "http://localhost:5000/dashboard/occupation_percentage_by_building"
    );
    const data = await res.json();
    setOccupationByBuilding(data); // es un ARRAY
  }

  async function getReservationsByProgram() {
    const res = await fetch(
      "http://localhost:5000/dashboard/reservations_by_program_and_faculty"
    );
    const data = await res.json();
    setReservationsByProgram(data);
  }

  async function getParticipantsWithMultipleSanctions() {
    const res = await fetch(
      "http://localhost:5000/dashboard/participants_with_multiple_sanctions"
    );
    const data = await res.json();
    setParticipantsMultipleSanctions(data);
  }

  async function getUsersMostNoShowOrCancel() {
    const res = await fetch(
      "http://localhost:5000/dashboard/users_most_no_show_or_cancel"
    );
    const data = await res.json();
    setUsersMostNoShow(data);
  }

  async function getMostDemandedTurns() {
    const res = await fetch(
      "http://localhost:5000/dashboard/most_demanded_turns"
    );
    const data = await res.json();
    setMostDemandedTurns(data); // es un array
  }

  useEffect(() => {
    getMostReserved();
    avgParticipants();
    getSanctions();
    getLeastUsed();
    getUsadasVsCanceladas();
    getReservationsAndAttendance();
    getOccupationByBuilding();
    getReservationsByProgram();
    getParticipantsWithMultipleSanctions();
    getUsersMostNoShowOrCancel();
    getMostDemandedTurns();
  }, []);

  return (
    <div style={{ marginLeft: 20 }}>
      <h1 style={{ marginTop: 20 }}>Reportes</h1>
      <h5 style={{ marginTop: 30 }}>Salas más reservadas</h5>
      <p>
        * La sala más reservada es {mostReserved && mostReserved.nombre_sala}{" "}
        con {mostReserved && mostReserved.cantidad_reservas} reservas.
      </p>
      <h5>Turnos más demandados</h5>

      {mostDemandedTurns.length > 0 ? (
        mostDemandedTurns.map((t, i) => (
          <p key={i}>
            * {formatHour(t.hora_inicio)} - {formatHour(t.hora_fin)}: (
            {t.cantidad_reservas} reservas)
          </p>
        ))
      ) : (
        <p>* Sin datos</p>
      )}

      <h5>Pormedio de participantes por sala</h5>
      <p>
        * Promedio de participantes por sala:{" "}
        {avg && parseFloat(avg.promedio_participantes)}
      </p>
      <h5>Cantidad de reservas por carrera y facultad</h5>

      {reservationsByProgram.length > 0 ? (
        reservationsByProgram.map((item, i) => (
          <p key={i}>
            * {item.carrera} — {item.facultad}: {item.cant_reservas} reservas
          </p>
        ))
      ) : (
        <p>* Sin datos</p>
      )}

      <h5>Porcentaje de ocupación de salas por edificios</h5>

      {occupationByBuilding.length > 0 ? (
        occupationByBuilding.map((item, i) => (
          <p key={i}>
            * Edificio {capitalize(item.edificio)}:{" "}
            {parseFloat(item.porcentaje)}%
          </p>
        ))
      ) : (
        <p>* Sin datos</p>
      )}

      <h5>
        Cantidad de reservas y asistencias de profesores y alumnos (grado y
        posgrado)
      </h5>

      {reservationsAttendance.length > 0 ? (
        reservationsAttendance.map((item, i) => (
          <p key={i}>
            * {capitalize(item.rol)} ({capitalize(item.tipo)}):{" "}
            {item.cant_reservas} reservas, {item.asistencia} asistencias.
          </p>
        ))
      ) : (
        <p>* Sin datos</p>
      )}

      <h5>
        Cantidad de sanciones para profesores y alumnos (grado y posgrado)
      </h5>

      {sanctions.length > 0 ? (
        sanctions.map((item, i) => (
          <p key={i}>
            * {capitalize(item.rol)} ({item.tipo}) tiene {item.cant_sanciones}{" "}
            sanciones
          </p>
        ))
      ) : (
        <p>* Sin datos</p>
      )}
      <h5>
        Porcentaje de reservas efectivamente utilizadas vs. canceladas/no
        asistidas
      </h5>

      {usadasVsCanceladas ? (
        <p>
          * {capitalize(usadasVsCanceladas.categoria)} —{" "}
          {parseFloat(usadasVsCanceladas.porcentaje)}%
        </p>
      ) : (
        <p>* Sin datos</p>
      )}

      <h5>Cantidad de participantes sancionados más de una vez</h5>

      {participantsMultipleSanctions.length > 0 ? (
        participantsMultipleSanctions.map((item, i) => (
          <p key={i}>
            * {item.nombre} {item.apellido} — {item.ci} — {item.cant_sanciones}{" "}
            sanciones
          </p>
        ))
      ) : (
        <p>* No hay participantes con múltiples sanciones</p>
      )}

      <h5>Usuarios que más cancelan o no asisten a sus reservas</h5>
      {usersMostNoShow.length > 0 ? (
        usersMostNoShow.map((u, i) => (
          <p key={i}>
            * {u.nombre} {u.apellido} — {u.ci} — {u.cant_no_show}{" "}
            ausencias/cancelaciones
          </p>
        ))
      ) : (
        <p>* No hay usuarios con cancelaciones o inasistencias destacadas</p>
      )}

      <h5>Salas con menor uso</h5>
      {leastUsedRooms.length > 0 ? (
        leastUsedRooms.map((item, i) => (
          <p key={i}>
            * {item.nombre_sala} ({item.edificio}) — {item.cantidad_reservas}{" "}
            reservas
          </p>
        ))
      ) : (
        <p>* Sin datos</p>
      )}
      <div style={{ textAlign: "center" }}>
        <Button
          style={{ width: 100, height: 50, marginBottom: 30 }}
          variant="outline-primary"
          onClick={() => navigate("/admin")}
        >
          Inicio
        </Button>
      </div>
    </div>
  );
}
