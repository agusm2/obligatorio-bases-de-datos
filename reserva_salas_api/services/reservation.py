from models.reservation import Reservation
from models.classroom import Classroom
from models.participant import Participant
from database.db import get_db_connection
from datetime import datetime, timedelta
import mysql.connector


def tiene_excepcion(ci, tipo_sala):
    """
    Devuelve True si para ESTA sala se aplican las excepciones:
    - docente en sala exclusiva docentes
    - docente o alumno de posgrado en sala exclusiva posgrado
    """
    programas = Participant.get_programs(
        ci
    )  # [{'nombre_programa', 'tipo', 'rol'}, ...]

    es_docente = any(p["rol"].lower() == "docente" for p in programas)
    es_posgrado = any(
        p["rol"].lower() == "alumno" and p["tipo"].lower() == "posgrado"
        for p in programas
    )

    if tipo_sala == "docente" and es_docente:
        return True
    if tipo_sala == "posgrado" and (es_docente or es_posgrado):
        return True

    return False


def horas_ocupadas_dia(ci, fecha):
    """Cantidad de reservas ACTIVAS de un participante en un día (todas las salas/edificios)."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM Reserva r
            JOIN Reserva_participante rp ON r.id_reserva = rp.id_reserva
            WHERE rp.ci_participante = %s
              AND r.fecha = %s
              AND r.estado = 'activa'
            """,
            (ci, fecha),
        )
        (cant,) = cur.fetchone()
        return cant
    finally:
        cur.close()
        conn.close()


def reservas_semana(ci, fecha):
    """Cantidad de reservas ACTIVAS de un participante en la semana de esa fecha."""
    f = datetime.strptime(fecha, "%Y-%m-%d").date()
    inicio = f - timedelta(days=f.weekday())  # lunes
    fin = inicio + timedelta(days=6)  # domingo

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT COUNT(DISTINCT r.id_reserva)
            FROM Reserva r
            JOIN Reserva_participante rp ON r.id_reserva = rp.id_reserva
            WHERE rp.ci_participante = %s
              AND r.estado = 'activa'
              AND r.fecha BETWEEN %s AND %s
            """,
            (ci, inicio, fin),
        )
        (cant,) = cur.fetchone()
        return cant
    finally:
        cur.close()
        conn.close()


def validar_participante(ci, fecha, tipo_sala):
    """
    Aplica reglas:
    - Máx 2 reservas activas en ese día (2h)
    - Máx 3 reservas activas en la semana
    Excepto si tiene excepción por tipo de sala.
    """
    # 1) excepción
    if tiene_excepcion(ci, tipo_sala):
        return

    # 2) límite diario
    if horas_ocupadas_dia(ci, fecha) >= 2:
        raise ValueError(
            f"El participante {ci} ya tiene 2 reservas activas en la fecha {fecha}"
        )

    # 3) límite semanal
    if reservas_semana(ci, fecha) >= 3:
        raise ValueError(
            f"El participante {ci} ya tiene 3 reservas activas en la semana de {fecha}"
        )


def get_all(limit=100, offset=0):
    items = Reservation.list_all(limit=limit, offset=offset)
    return [r.to_dict() for r in items]


def get_by_id(id_reserva):
    obj = Reservation.get_by_id(id_reserva)
    if not obj:
        return None
    d = obj.to_dict()
    d["participants"] = obj.list_participants()
    return d


def create(data):
    # data expects: nombre_sala, edificio, fecha (YYYY-MM-DD), id_turno
    nombre_sala = data.get("classroom_name")
    edificio = data.get("building")
    fecha = data.get("date")
    id_turno = data.get("id_turn")

    # Basic validation: classroom exists
    classroom = Classroom.get_by_pk(nombre_sala, edificio)
    if not classroom:
        raise ValueError("Classroom does not exist")

    # tipo_sala: 'libre' | 'posgrado' | 'docente'
    tipo_sala = classroom.room_type

    # aceptar lista opcional de participantes (cedulas) en el payload: data['participants']
    participants = data.get("participants") or []

    # 🔥 VALIDACIÓN DE REGLAS (2h/día, 3/semana, con excepciones)
    for ci in participants:
        validar_participante(ci, fecha, tipo_sala)

    # Si pasó todas las validaciones, crear la reserva
    obj = Reservation.create(
        nombre_sala=nombre_sala,
        edificio=edificio,
        fecha=fecha,
        id_turno=id_turno,
        participants=participants,
    )
    return obj.to_dict()


def update(id_reserva, data):
    obj = Reservation.get_by_id(id_reserva)
    if not obj:
        return None
    obj.update(
        nombre_sala=data.get("nombre_sala"),
        edificio=data.get("edificio"),
        fecha=data.get("fecha"),
        id_turno=data.get("id_turno"),
        estado=data.get("estado"),
        participants=data.get("participants"),
    )
    return obj.to_dict()


def delete(id_reserva):
    obj = Reservation.get_by_id(id_reserva)
    if not obj:
        return None
    obj.delete()
    return {"message": "Deleted"}


def add_participant(id_reserva, ci):
    obj = Reservation.get_by_id(id_reserva)
    if not obj:
        return None
    # check participant exists
    p = Participant.get_by_pk(ci)
    if not p:
        raise ValueError("Participant does not exist")

    # check capacity
    classroom = Classroom.get_by_pk(obj.nombre_sala, obj.edificio)
    if classroom and classroom.capacity is not None:
        parts = obj.list_participants()
        if len(parts) >= classroom.capacity:
            raise ValueError("Capacity exceeded")

    try:
        obj.add_participant(ci_participante=ci)
    except mysql.connector.IntegrityError:
        return None
    return {"message": "Participant added"}


def remove_participant(id_reserva, ci):
    obj = Reservation.get_by_id(id_reserva)
    if not obj:
        return None
    obj.remove_participant(ci)
    return {"message": "Participant removed"}


def list_participants(id_reserva):
    obj = Reservation.get_by_id(id_reserva)
    if not obj:
        return None
    return obj.list_participants()


def update_asistencia(id_reserva, ci_participante, asistencia):
    return Reservation.update_asistencia(id_reserva, ci_participante, asistencia)


def get_by_participant(ci):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """
            SELECT r.id_reserva, r.nombre_sala, r.edificio, r.fecha, r.id_turno, r.estado
            FROM Reserva r
            JOIN Reserva_participante rp ON r.id_reserva = rp.id_reserva
            WHERE rp.ci_participante = %s
              AND r.estado = 'activa'
            ORDER BY r.fecha ASC, r.id_turno ASC
            """,
            (ci,),
        )
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()
