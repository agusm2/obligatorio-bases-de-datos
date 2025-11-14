import mysql.connector
from database.db import get_db_connection

class Classroom:
    ALLOWED_ROOM_TYPES = ('libre', 'posgrado', 'docente')

    def __init__(self, name, building, capacity=None, room_type='libre'):
        if not name:
            raise ValueError("name es obligatorio")
        if not building:
            raise ValueError("building es obligatorio")
        if room_type not in Classroom.ALLOWED_ROOM_TYPES:
            raise ValueError(f"room_type debe ser uno de {Classroom.ALLOWED_ROOM_TYPES}")
        self.name = str(name)
        self.building = str(building)
        self.capacity = int(capacity) if capacity is not None else None
        self.room_type = room_type

    @property
    def pk(self):
        """Clave primaria compuesta por (name, building)."""
        return (self.name, self.building)

    def to_dict(self):
        return {
            'nombre_sala': self.name,
            'edificio': self.building,
            'capacidad': self.capacity,
            'tipo_sala': self.room_type
        }

    @classmethod
    def from_row(cls, row):
        if not row:
            return None
        if isinstance(row, dict):
            nombre = row.get('nombre_sala')
            edificio = row.get('edificio')
            capacidad = row.get('capacidad')
            tipo = row.get('tipo_sala')
        else:
            nombre, edificio, capacidad, tipo = row
        return cls(name=nombre, building=edificio, capacity=capacidad, room_type=tipo)

    @classmethod
    def create(cls, name, building, capacity=None, room_type='libre'):
        obj = cls(name, building, capacity, room_type)
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO sala (nombre_sala, edificio, capacidad, tipo_sala) VALUES (%s,%s,%s,%s)",
                (obj.name, obj.building, obj.capacity, obj.room_type)
            )
            conn.commit()
        except mysql.connector.IntegrityError:
            # Propagar para que la capa superior pueda decidir (409/400)
            raise
        finally:
            cur.close()
            conn.close()
        return obj

    @classmethod
    def get_by_pk(cls, name, building):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT nombre_sala, edificio, capacidad, tipo_sala FROM sala WHERE nombre_sala=%s AND edificio=%s",
                (name, building)
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
                "SELECT nombre_sala, edificio, capacidad, tipo_sala FROM sala ORDER BY edificio, nombre_sala LIMIT %s OFFSET %s",
                (limit, offset)
            )
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()
        return [cls.from_row(r) for r in rows]

    def update(self, capacity=None, room_type=None):
        if room_type is not None and room_type not in Classroom.ALLOWED_ROOM_TYPES:
            raise ValueError("room_type inválido")
        new_capacity = int(capacity) if capacity is not None else self.capacity
        new_room_type = room_type if room_type is not None else self.room_type

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE sala SET capacidad=%s, tipo_sala=%s WHERE nombre_sala=%s AND edificio=%s",
                (new_capacity, new_room_type, self.name, self.building)
            )
            conn.commit()
            self.capacity = new_capacity
            self.room_type = new_room_type
        finally:
            cur.close()
            conn.close()
        return self

    def delete(self):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM sala WHERE nombre_sala=%s AND edificio=%s",
                (self.name, self.building)
            )
            conn.commit()
        finally:
            cur.close()
            conn.close()
        return True

    def __eq__(self, other):
        if not isinstance(other, Classroom):
            return NotImplemented
        return self.pk == other.pk

    def __hash__(self):
        return hash(self.pk)

    def __repr__(self):
        return f"Classroom(nombre_sala={self.name!r}, edificio={self.building!r})"