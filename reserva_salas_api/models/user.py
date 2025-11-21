import mysql.connector
from database.db import get_db_connection


class User:
    def __init__(self, correo, password, tipo_usuario='usuario', sancionado=False):
        if not correo:
            raise ValueError("correo es obligatorio")
        if password is None:
            raise ValueError("password es obligatorio")
        self.correo = str(correo)
        self.password = str(password)
        self.tipo_usuario = str(tipo_usuario) if tipo_usuario is not None else 'usuario'
        # sancionado: boolean indicating whether the user currently has an active sanction
        self.sancionado = bool(sancionado)

    @property
    def pk(self):
        return self.correo

    def to_dict(self, include_password=False):
        d = {
            'correo': self.correo,
            'role': self.tipo_usuario,
        }
        # include sanction status in the returned representation
        d['sancionado'] = bool(self.sancionado)
        if include_password:
            d['password'] = self.password
        return d

    @classmethod
    def from_row(cls, row):
        if not row:
            return None
        if isinstance(row, dict):
            correo = row.get('correo') or row.get('Correo')
            password = row.get('password')
            tipo = row.get('tipo_usuario')
            sanc = row.get('sancionado')
        else:
            # when using a non-dict cursor this will unpack the tuple
            # expected order: correo, password, tipo_usuario, sancionado
            try:
                correo, password, tipo, sanc = row
            except ValueError:
                # fallback for older callers that expect (correo, password, tipo)
                correo, password, tipo = row
                sanc = False
        return cls(correo=correo, password=password, tipo_usuario=tipo, sancionado=sanc)

    @classmethod
    def get_by_pk(cls, correo):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            # include a computed `sancionado` boolean indicating if there's any
            # active sanction for the participant whose email matches the login correo
            cur.execute(
                """
                SELECT L.correo, L.password, L.tipo_usuario,
                       EXISTS(
                           SELECT 1
                           FROM Participante p
                           JOIN Sancion_participante s ON p.ci = s.ci_participante
                           WHERE p.email = L.correo
                             AND s.fecha_inicio <= NOW()
                             AND s.fecha_fin >= CURRENT_DATE()
                       ) AS sancionado
                FROM Login L
                WHERE L.correo = %s
                """,
                (correo,)
            )
            row = cur.fetchone()
        finally:
            cur.close()
            conn.close()
        return cls.from_row(row)