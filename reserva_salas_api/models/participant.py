import mysql.connector
from database.db import get_db_connection


class Participant:
    def __init__(self, ci, name, surname, email=None):
        if not ci:
            raise ValueError("ci es obligatorio")
        if not name:
            raise ValueError("name es obligatorio")
        if not surname:
            raise ValueError("surname es obligatorio")
        self.ci = str(ci)
        self.name = str(name)
        self.surname = str(surname)
        self.email = str(email) if email is not None else None

    @property
    def pk(self):
        return self.ci

    def to_dict(self):
        return {
            'ci': self.ci,
            'nombre': self.name,
            'apellido': self.surname,
            'email': self.email
        }

    @classmethod
    def from_row(cls, row):
        if not row:
            return None
        if isinstance(row, dict):
            ci = row.get('ci')
            nombre = row.get('nombre')
            apellido = row.get('apellido')
            email = row.get('email')
        else:
            ci, nombre, apellido, email = row
        return cls(ci=ci, name=nombre, surname=apellido, email=email)

    @classmethod
    def create(cls, ci, name, surname, email=None, programas=None, password=None, tipo_usuario='usuario'):
        """Crea un participante y opcionalmente sus relaciones a programas.

        Si se pasa `password` se intentará crear además el usuario en la tabla
        `Login` usando el `email` como `correo` y `tipo_usuario`.

        programas: lista de dicts o tuplas con ('nombre_programa', 'rol') o
                   dicts {'nombre_programa':..., 'rol': ...}.
        """
        obj = cls(ci, name, surname, email)
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # Insert participante
            cur.execute(
                "INSERT INTO Participante (ci, nombre, apellido, email) VALUES (%s,%s,%s,%s)",
                (obj.ci, obj.name, obj.surname, obj.email)
            )

            # Si vienen programas, insertarlos en la misma transacción
            if programas:
                for p in programas:
                    if isinstance(p, dict):
                        nombre_programa = p.get('nombre_programa') or p.get('nombre')
                        rol = p.get('rol')
                    else:
                        # asumir tupla/lista (nombre_programa, rol)
                        nombre_programa, rol = p
                    cur.execute(
                        "INSERT INTO Participante_programa_academico (ci_participante, nombre_programa, rol) VALUES (%s,%s,%s)",
                        (obj.ci, nombre_programa, rol)
                    )

            # Si se proporciona password, crear también el login (usa email como correo)
            if password is not None:
                if not obj.email:
                    # No tiene email para usar como login -> considerarlo error del caller
                    raise ValueError('email es obligatorio para crear el Login cuando se pasa password')
                cur.execute(
                    "INSERT INTO Login (correo, password, tipo_usuario) VALUES (%s, %s, %s)",
                    (obj.email, password, tipo_usuario)
                )

            conn.commit()
        except mysql.connector.IntegrityError:
            # rollback and rethrow for service layer to translate (e.g., 409)
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
        return obj

    @classmethod
    def get_programs(cls, ci):
        """Devuelve la lista de programas asociados al participante (nombre_programa, tipo, rol)."""
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT ppa.nombre_programa AS nombre_programa, pa.tipo AS tipo, ppa.rol AS rol "
                "FROM Participante_programa_academico ppa "
                "LEFT JOIN Programa_academico pa ON ppa.nombre_programa = pa.nombre_programa "
                "WHERE ppa.ci_participante = %s",
                (ci,)
            )
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()
        return rows

    @classmethod
    def get_by_pk(cls, ci):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT ci, nombre, apellido, email FROM Participante WHERE ci=%s",
                (ci,)
            )
            row = cur.fetchone()
        finally:
            cur.close()
            conn.close()
        return cls.from_row(row)

    @classmethod
    def list_all(cls, limit=100, offset=0):
        """
        Devuelve una lista de registros donde cada elemento es un dict:
        {
            'participant': Participant(...),
            'programas': [ {'nombre_programa': ..., 'tipo': ..., 'rol': ...}, ... ]
        }

        Aplica limit/offset sobre la lista de participantes, y luego consulta
        los programas asociados a esos participantes en una segunda consulta
        (más eficiente y evita truncar filas por el JOIN).
        """
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            # Obtener los participantes (paginar aquí)
            cur.execute(
                "SELECT ci, nombre, apellido, email FROM Participante ORDER BY apellido, nombre LIMIT %s OFFSET %s",
                (limit, offset)
            )
            participant_rows = cur.fetchall()
            participants = [cls.from_row(r) for r in participant_rows]

            cis = [p.ci for p in participants]
            if not cis:
                return []

            # Obtener programas para los participantes seleccionados
            placeholders = ",".join(["%s"] * len(cis))
            query = (
                "SELECT ppa.ci_participante AS ci, ppa.nombre_programa AS nombre_programa, "
                "pa.tipo AS tipo, ppa.rol AS rol "
                "FROM Participante_programa_academico ppa "
                "JOIN Programa_academico pa ON ppa.nombre_programa = pa.nombre_programa "
                f"WHERE ppa.ci_participante IN ({placeholders})"
            )
            cur.execute(query, tuple(cis))
            program_rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

        # Agrupar programas por ci
        program_map = {}
        for r in program_rows:
            ci = r.get('ci')
            program_map.setdefault(ci, []).append({
                'nombre_programa': r.get('nombre_programa'),
                'tipo': r.get('tipo'),
                'rol': r.get('rol')
            })

        result = []
        for p in participants:
            result.append({'participant': p, 'programas': program_map.get(p.ci, [])})
        return result

    def update(self, email=None):
        new_email = email if email is not None else self.email

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE Participante SET email=%s WHERE ci=%s",
                (new_email, self.ci)
            )
            conn.commit()
            self.email = new_email
        finally:
            cur.close()
            conn.close()
        return self

    def delete(self):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM Participante WHERE ci=%s",
                (self.ci,)
            )
            conn.commit()
        finally:
            cur.close()
            conn.close()
        return True

    @classmethod
    def add_sancion(cls, ci, fecha_fin, fecha_inicio=None):
        """Inserta una sanción para el participante en la tabla Sancion_participante.

        fecha_fin: str 'YYYY-MM-DD' (obligatorio)
        fecha_inicio: str 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS' (opcional)

        Devuelve dict con la sanción creada o lanza ValueError en caso de datos inválidos.
        """
        if isinstance(ci, dict):
            ci = ci.get('ci')

        if not ci:
            raise ValueError('ci es obligatorio')

        # Validar participante existe
        participante = cls.get_by_pk(ci)
        if not participante:
            return None

        # Validar formato de fecha_fin
        from datetime import datetime
        try:
            fecha_fin_date = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        except Exception:
            raise ValueError('fecha_fin inválida, debe tener formato YYYY-MM-DD')

        fecha_inicio_dt = None
        if fecha_inicio:
            parsed = None
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
                try:
                    parsed = datetime.strptime(fecha_inicio, fmt)
                    break
                except Exception:
                    continue
            if not parsed:
                raise ValueError("fecha_inicio inválida, formatos permitidos: 'YYYY-MM-DD' o 'YYYY-MM-DD HH:MM:SS'")
            # Si vino sólo fecha, usar medianoche
            if len(fecha_inicio) == 10:
                fecha_inicio_dt = datetime(parsed.year, parsed.month, parsed.day, 0, 0, 0)
            else:
                fecha_inicio_dt = parsed

        # Comprobar coherencia
        if fecha_inicio_dt is not None and fecha_fin_date < fecha_inicio_dt.date():
            raise ValueError('fecha_fin no puede ser anterior a fecha_inicio')

        # Insertar en la base
        cur_conn = get_db_connection()
        cur = cur_conn.cursor()
        try:
            if fecha_inicio_dt is None:
                cur.execute(
                    "INSERT INTO Sancion_participante (ci_participante, fecha_fin) VALUES (%s, %s)",
                    (ci, fecha_fin_date)
                )
            else:
                cur.execute(
                    "INSERT INTO Sancion_participante (ci_participante, fecha_inicio, fecha_fin) VALUES (%s, %s, %s)",
                    (ci, fecha_inicio_dt.strftime('%Y-%m-%d %H:%M:%S'), fecha_fin_date)
                )
            cur_conn.commit()
        finally:
            cur.close()
            cur_conn.close()

        return {
            'ci': ci,
            'fecha_inicio': fecha_inicio_dt.strftime('%Y-%m-%d %H:%M:%S') if fecha_inicio_dt is not None else None,
            'fecha_fin': fecha_fin_date.strftime('%Y-%m-%d')
        }

    def __eq__(self, other):
        if not isinstance(other, Participant):
            return NotImplemented
        return self.pk == other.pk

    def __hash__(self):
        return hash(self.pk)

    def __repr__(self):
        return f"Participant(ci={self.ci!r}, nombre={self.name!r}, apellido={self.surname!r})"
