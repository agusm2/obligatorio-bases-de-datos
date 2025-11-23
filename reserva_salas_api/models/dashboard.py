import mysql.connector
from database.db import get_db_connection


class Dashboard:
    """Clase con consultas SQL usadas por el dashboard. Cada método devuelve una lista
    de diccionarios o un dict según corresponda.
    """

    @classmethod
    def most_reserved_rooms(cls):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                """
                SELECT s.nombre_sala, s.edificio, COUNT(*) AS cantidad_reservas
                FROM Sala s
                JOIN reserva r ON s.nombre_sala = r.nombre_sala AND s.edificio = r.edificio
                GROUP BY s.nombre_sala, s.edificio
                ORDER BY cantidad_reservas DESC
                """
            )
            rows = cur.fetchall()
            return rows or []
        finally:
            cur.close()
            conn.close()

    @classmethod
    def most_demanded_turns(cls):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                """
                SELECT t.hora_inicio, t.hora_fin, COUNT(r.id_reserva) AS cantidad_reservas
                FROM turno t
                JOIN reserva r ON t.id_turno = r.id_turno
                GROUP BY t.hora_inicio, t.hora_fin
                ORDER BY cantidad_reservas DESC
                """
            )
            return cur.fetchall() or []
        finally:
            cur.close()
            conn.close()

    @classmethod
    def avg_participants_per_room(cls):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                """
                SELECT reservas.nombre_sala, reservas.edificio, AVG(reservas.num_participantes) AS promedio_participantes
                FROM (
                  SELECT r.id_reserva, r.nombre_sala, r.edificio, COUNT(rp.ci_participante) AS num_participantes
                  FROM reserva r
                  JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
                  GROUP BY r.id_reserva, r.nombre_sala, r.edificio
                ) AS reservas
                GROUP BY reservas.nombre_sala, reservas.edificio
                ORDER BY promedio_participantes DESC
                """
            )
            return cur.fetchall() or []
        finally:
            cur.close()
            conn.close()

    @classmethod
    def reservations_by_program_and_faculty(cls):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                """
                SELECT f.nombre AS facultad, ppa.nombre_programa AS carrera, COUNT(DISTINCT r.id_reserva) AS cant_reservas
                FROM reserva_participante rp
                JOIN reserva r ON r.id_reserva = rp.id_reserva
                JOIN participante_programa_academico ppa ON ppa.ci_participante = rp.ci_participante
                JOIN programa_academico pa ON pa.nombre_programa = ppa.nombre_programa
                JOIN facultad f ON f.id_facultad = pa.id_facultad
                GROUP BY f.nombre, ppa.nombre_programa
                ORDER BY f.nombre, cant_reservas DESC
                """
            )
            return cur.fetchall() or []
        finally:
            cur.close()
            conn.close()

    @classmethod
    def occupation_percentage_by_building(cls):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                """
                SELECT r.edificio AS edificio,
                       SUM(r.estado = 'activa') * 100.0 / COUNT(*) AS porcentaje
                FROM reserva r
                JOIN edificio e ON e.nombre_edificio = r.edificio
                GROUP BY r.edificio
                """
            )
            return cur.fetchall() or []
        finally:
            cur.close()
            conn.close()

    @classmethod
    def reservations_and_attendance_by_role_and_type(cls):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                """
                SELECT ppa.rol AS rol, pa.tipo AS tipo,
                       COUNT(DISTINCT r.id_reserva) AS cant_reservas,
                       SUM(IF(rp.asistencia = TRUE, 1, 0)) AS asistencia
                FROM reserva_participante rp
                JOIN reserva r ON r.id_reserva = rp.id_reserva
                JOIN participante_programa_academico ppa ON ppa.ci_participante = rp.ci_participante
                JOIN programa_academico pa ON pa.nombre_programa = ppa.nombre_programa
                GROUP BY ppa.rol, pa.tipo
                ORDER BY pa.tipo, ppa.rol
                """
            )
            return cur.fetchall() or []
        finally:
            cur.close()
            conn.close()

    @classmethod
    def sanctions_by_role_and_type(cls):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                """
                SELECT ppa.rol AS rol, pa.tipo AS tipo, COUNT(DISTINCT san.ci_participante) AS cant_sanciones
                FROM sancion_participante san
                JOIN participante_programa_academico ppa ON ppa.ci_participante = san.ci_participante
                JOIN programa_academico pa ON pa.nombre_programa = ppa.nombre_programa
                GROUP BY ppa.rol, pa.tipo
                ORDER BY pa.tipo, ppa.rol
                """
            )
            return cur.fetchall() or []
        finally:
            cur.close()
            conn.close()

    @classmethod
    def usage_vs_cancelled(cls):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                """
                SELECT IF(estado IN ('cancelada', 'sin asistencia'), 'canceladas/no_asistidas', 'utilizadas') AS categoria,
                       COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reserva) AS porcentaje
                FROM reserva
                GROUP BY categoria
                """
            )
            return cur.fetchall() or []
        finally:
            cur.close()
            conn.close()

    # Consultas sugeridas adicionales
    @classmethod
    def participants_with_multiple_sanctions(cls):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                """
                SELECT ci_participante, COUNT(*) AS cantidad_sanciones
                FROM sancion_participante
                GROUP BY ci_participante
                HAVING COUNT(*) > 1
                """
            )
            return cur.fetchall() or []
        finally:
            cur.close()
            conn.close()

    @classmethod
    def users_most_no_show_or_cancel(cls):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                """
                SELECT rp.ci_participante, COUNT(*) AS reservas_no_utilizadas
                FROM reserva_participante rp
                JOIN reserva r ON rp.id_reserva = r.id_reserva
                WHERE r.estado IN ('cancelada', 'sin asistencia')
                GROUP BY rp.ci_participante
                ORDER BY reservas_no_utilizadas DESC
                """
            )
            return cur.fetchall() or []
        finally:
            cur.close()
            conn.close()

    @classmethod
    def least_used_rooms(cls):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                """
                SELECT s.nombre_sala, s.edificio, COUNT(r.id_reserva) AS cantidad_reservas
                FROM sala s
                LEFT JOIN reserva r ON s.nombre_sala = r.nombre_sala AND s.edificio = r.edificio
                GROUP BY s.nombre_sala, s.edificio
                ORDER BY cantidad_reservas ASC
                """
            )
            return cur.fetchall() or []
        finally:
            cur.close()
            conn.close()
