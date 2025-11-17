from app.models.database import get_db_connection

class Usuario:
    @staticmethod
    def crear(nombre, correo, password_hash):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO usuarios (nombre, correo, password_hash) VALUES (%s, %s, %s)",
                    (nombre, correo, password_hash)
                )
                return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def obtener_por_correo(correo):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, nombre, correo, password_hash FROM usuarios WHERE correo = %s",
                    (correo,)
                )
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(usuario_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, nombre, correo, fecha_creacion FROM usuarios WHERE id = %s",
                    (usuario_id,)
                )
                return cursor.fetchone()
        finally:
            conn.close()