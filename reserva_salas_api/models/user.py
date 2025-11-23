import mysql.connector
from database.db import get_db_connection


class User:
    def __init__(self, correo, password, tipo_usuario="usuario", sancionado=False):
        if not correo:
            raise ValueError("correo es obligatorio")
        if password is None:
            raise ValueError("password es obligatorio")
        self.correo = str(correo)
        self.password = str(password)
        self.tipo_usuario = str(tipo_usuario) if tipo_usuario is not None else "usuario"
        # sancionado: boolean indicating whether the user currently has an active sanction
        self.sancionado = bool(sancionado)

    @property
    def pk(self):
        return self.correo

    def to_dict(self, include_password=False):
        d = {
            "correo": self.correo,
            "role": self.tipo_usuario,
            "sancionado": bool(self.sancionado),
        }
        # include sanction status in the returned representation
        if hasattr(self, "fecha_fin_sancion"):
            d["fecha_fin_sancion"] = self.fecha_fin_sancion
        if include_password:
            d["password"] = self.password

        return d

    @classmethod
    def from_row(cls, row):
        if not row:
            return None

        fecha_fin = None

        if isinstance(row, dict):
            correo = row.get("correo") or row.get("Correo")
            password = row.get("password")
            tipo = row.get("tipo_usuario")
            sanc = row.get("sancionado")
            fecha_fin = row.get("fecha_fin_sancion")
        else:
            # when using a non-dict cursor this will unpack the tuple
            # expected order: correo, password, tipo_usuario, sancionado
            try:
                correo, password, tipo, sanc = row
            except ValueError:
                # fallback for older callers that expect (correo, password, tipo)
                correo, password, tipo = row
                sanc = False
        user = cls(correo=correo, password=password, tipo_usuario=tipo, sancionado=sanc)

        if fecha_fin is not None:
            user.fecha_fin_sancion = fecha_fin

        return user

    @classmethod
    def get_by_pk(cls, correo):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                """
                SELECT 
                    L.correo, 
                    L.password, 
                    L.tipo_usuario,
                    EXISTS(
                        SELECT 1
                        FROM Participante p
                        JOIN Sancion_participante s ON p.ci = s.ci_participante
                        WHERE p.email = L.correo
                        AND s.fecha_inicio <= NOW()
                        AND s.fecha_fin >= CURRENT_DATE()
                    ) AS sancionado,
                    (
                        SELECT s.fecha_fin
                        FROM Participante p
                        JOIN Sancion_participante s ON p.ci = s.ci_participante
                        WHERE p.email = L.correo
                        AND s.fecha_inicio <= NOW()
                        AND s.fecha_fin >= CURRENT_DATE()
                        ORDER BY s.fecha_fin DESC
                        LIMIT 1
                    ) AS fecha_fin_sancion
                FROM Login L
                WHERE L.correo = %s
                """,
                (correo,),
            )
            row = cur.fetchone()
        finally:
            cur.close()
            conn.close()
        return cls.from_row(row)
