import mysql.connector
from datetime import date, datetime, time, timedelta
from database.db import get_db_connection


class Reservation:
    """Model for reservations. Database field names remain in Spanish.

    Fields used in DB: nombre_sala, edificio, fecha, id_turno, estado
    """
    ALLOWED_STATES = ('activa', 'cancelada', 'sin asistencia', 'finalizada')

    def __init__(self, id_reserva, nombre_sala, edificio, fecha, id_turno, estado='activa'):
        if not nombre_sala or not edificio or not fecha or not id_turno:
            raise ValueError('nombre_sala, edificio, fecha e id_turno son obligatorios')
        self.id_reserva = int(id_reserva) if id_reserva is not None else None
        # fecha can be a 'YYYY-MM-DD' string or a date
        if isinstance(fecha, str):
            self.fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        elif isinstance(fecha, date):
            self.fecha = fecha
        else:
            raise ValueError('fecha must be YYYY-MM-DD string or datetime.date')
        self.nombre_sala = str(nombre_sala)
        self.edificio = str(edificio)
        self.id_turno = int(id_turno)
        if estado not in Reservation.ALLOWED_STATES:
            raise ValueError('invalid estado')
        self.estado = estado

    def to_dict(self):
        data = {
            'id_reserva': self.id_reserva,
            'nombre_sala': self.nombre_sala,
            'edificio': self.edificio,
            'fecha': self.fecha.isoformat(),
            'id_turno': self.id_turno,
            'estado': self.estado
        }
        # Añadir participantes si están presentes en la instancia
        participants = getattr(self, 'participants', None)
        if participants is not None:
            data['participants'] = participants
        return data

    @classmethod
    def from_row(cls, row):
        if not row:
            return None
        if isinstance(row, dict):
            id_reserva = row.get('id_reserva')
            nombre = row.get('nombre_sala')
            edificio = row.get('edificio')
            fecha = row.get('fecha')
            id_turno = row.get('id_turno')
            estado = row.get('estado')
        else:
            id_reserva, nombre, edificio, fecha, id_turno, estado = row
        return cls(id_reserva=id_reserva, nombre_sala=nombre, edificio=edificio, fecha=fecha, id_turno=id_turno, estado=estado)

    @classmethod
    def create(cls, nombre_sala, edificio, fecha, id_turno, estado='activa', participants=None):
        """Crear reserva. Si se pasa `participants` (lista de CI strings), se relacionan
        con la reserva creada (fecha_solicitud_reserva = now, asistencia=False por defecto).
        """
        obj = cls(None, nombre_sala, edificio, fecha, id_turno, estado)
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado) VALUES (%s,%s,%s,%s,%s)",
                (obj.nombre_sala, obj.edificio, obj.fecha, obj.id_turno, obj.estado)
            )
            conn.commit()
            obj.id_reserva = cur.lastrowid
        except mysql.connector.IntegrityError:
            raise
        finally:
            cur.close()
            conn.close()

        # Si se pasaron participantes, agregarlos (usa add_participant que maneja la inserción individual)
        if participants:
            try:
                for ci in participants:
                    # add_participant hará validaciones (sanciones, FK, capacidad, etc)
                    obj.add_participant(ci_participante=ci)
            except Exception:
                # limpiar reserva creada para no dejar estado parcial
                try:
                    obj.delete()
                except Exception:
                    pass
                raise

        return obj

    @classmethod
    def get_by_id(cls, id_reserva):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT id_reserva, nombre_sala, edificio, fecha, id_turno, estado FROM reserva WHERE id_reserva=%s",
                (id_reserva,)
            )
            row = cur.fetchone()
        finally:
            cur.close()
            conn.close()
        return cls.from_row(row)

    @classmethod
    def list_all(cls, limit=100, offset=0):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT id_reserva, nombre_sala, edificio, fecha, id_turno, estado FROM reserva ORDER BY fecha DESC LIMIT %s OFFSET %s",
                (limit, offset)
            )
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()
        # Si no hay filas, devolvemos lista vacía
        if not rows:
            return []

        # Instancias de Reservation para las filas obtenidas
        reservations = [cls.from_row(r) for r in rows]

        # Recolectar todos los ids de reserva para consultar participantes en una sola consulta
        ids = [r['id_reserva'] for r in rows]

        # Obtener participantes y asistencia para todas las reservas obtenidas
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            placeholders = ','.join(['%s'] * len(ids))
            query = (
                "SELECT rp.id_reserva, rp.ci_participante, rp.fecha_solicitud_reserva, rp.asistencia, "
                "p.nombre, p.apellido, p.email "
                "FROM reserva_participante rp LEFT JOIN Participante p ON rp.ci_participante = p.ci "
                f"WHERE rp.id_reserva IN ({placeholders})"
            )
            cur.execute(query, tuple(ids))
            part_rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

        # Mapear participantes por id_reserva
        participants_map = {}
        for pr in part_rows:
            rid = pr['id_reserva']
            fecha_sol = pr.get('fecha_solicitud_reserva')
            # convertir fecha a ISO si es datetime
            if hasattr(fecha_sol, 'isoformat'):
                fecha_sol = fecha_sol.isoformat()
            entry = {
                'ci_participante': pr.get('ci_participante'),
                'fecha_solicitud_reserva': fecha_sol,
                'asistencia': bool(pr.get('asistencia')),
                'nombre': pr.get('nombre'),
                'apellido': pr.get('apellido'),
                'email': pr.get('email')
            }
            participants_map.setdefault(rid, []).append(entry)

        # Adjuntar la lista de participantes a cada instancia Reservation
        for res in reservations:
            # atributo dinámico `participants` con lista de dicts (vacía si no hay participantes)
            res.participants = participants_map.get(res.id_reserva, [])

        return reservations

    def update(self, nombre_sala=None, edificio=None, fecha=None, id_turno=None, estado=None, participants=None):
        new_nombre = nombre_sala if nombre_sala is not None else self.nombre_sala
        new_edificio = edificio if edificio is not None else self.edificio
        new_fecha = fecha if fecha is not None else self.fecha
        new_id_turno = id_turno if id_turno is not None else self.id_turno
        new_estado = estado if estado is not None else self.estado

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE reserva SET nombre_sala=%s, edificio=%s, fecha=%s, id_turno=%s, estado=%s WHERE id_reserva=%s",
                (new_nombre, new_edificio, new_fecha, new_id_turno, new_estado, self.id_reserva)
            )
            conn.commit()
            self.nombre_sala = new_nombre
            self.edificio = new_edificio
            if isinstance(new_fecha, str):
                from datetime import datetime
                self.fecha = datetime.strptime(new_fecha, '%Y-%m-%d').date()
            else:
                self.fecha = new_fecha
            self.id_turno = int(new_id_turno)
            self.estado = new_estado
        finally:
            cur.close()
            conn.close()
        # Si se recibe una lista `participants`, sincronizar la relación:
        # - añadir los CI que estén en `participants` y no en la relación actual
        # - eliminar los CI que estén en la relación actual y no en `participants`
        if participants is not None:
            # obtener participantes actuales (list_participants devuelve dicts)
            current = [p.get('ci_participante') for p in self.list_participants()]
            # normalizar a strings
            current_set = set(filter(None, map(str, current)))
            new_set = set(filter(None, map(str, participants)))

            to_add = new_set - current_set
            to_remove = current_set - new_set

            for ci in to_add:
                try:
                    self.add_participant(ci_participante=ci)
                except mysql.connector.IntegrityError:
                    # propagar o ignorar? dejamos propagar para que la capa superior decida
                    raise

            for ci in to_remove:
                self.remove_participant(ci)

        return self

    def delete(self):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # remove participants first
            cur.execute("DELETE FROM reserva_participante WHERE id_reserva=%s", (self.id_reserva,))
            cur.execute("DELETE FROM reserva WHERE id_reserva=%s", (self.id_reserva,))
            conn.commit()
        finally:
            cur.close()
            conn.close()
        return True

    # Participant management
    def add_participant(self, ci_participante, fecha_solicitud=None, asistencia=False):
        if fecha_solicitud is None:
            fecha_solicitud = datetime.now()
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # comprobar si el participante está sancionado en la fecha de la reserva
            cur.execute(
                "SELECT 1 FROM Sancion_participante WHERE ci_participante=%s AND fecha_inicio <= %s AND fecha_fin >= %s",
                (ci_participante, self.fecha, self.fecha)
            )
            if cur.fetchone():
                raise ValueError('Participant has an active sanction for this date')

            cur.execute(
                "INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia) VALUES (%s,%s,%s,%s)",
                (ci_participante, self.id_reserva, fecha_solicitud, int(bool(asistencia)))
            )
            conn.commit()
        except mysql.connector.IntegrityError:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
        return True

    def remove_participant(self, ci_participante):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM reserva_participante WHERE id_reserva=%s AND ci_participante=%s",
                (self.id_reserva, ci_participante)
            )
            conn.commit()
        finally:
            cur.close()
            conn.close()
        return True

    def list_participants(self):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT rp.ci_participante, rp.fecha_solicitud_reserva, rp.asistencia, p.nombre, p.apellido, p.email "
                "FROM reserva_participante rp LEFT JOIN Participante p ON rp.ci_participante = p.ci "
                "WHERE rp.id_reserva=%s",
                (self.id_reserva,)
            )
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()
        return rows