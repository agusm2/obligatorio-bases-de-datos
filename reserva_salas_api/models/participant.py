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
    def create(cls, ci, name, surname, email=None):
        obj = cls(ci, name, surname, email)
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO Participante (ci, nombre, apellido, email) VALUES (%s,%s,%s,%s)",
                (obj.ci, obj.name, obj.surname, obj.email)
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
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                "SELECT ci, nombre, apellido, email FROM Participante ORDER BY apellido, nombre LIMIT %s OFFSET %s",
                (limit, offset)
            )
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()
        return [cls.from_row(r) for r in rows]

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

    def __eq__(self, other):
        if not isinstance(other, Participant):
            return NotImplemented
        return self.pk == other.pk

    def __hash__(self):
        return hash(self.pk)

    def __repr__(self):
        return f"Participant(ci={self.ci!r}, nombre={self.name!r}, apellido={self.surname!r})"
