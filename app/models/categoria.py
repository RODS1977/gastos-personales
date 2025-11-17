from app.models.database import get_db_connection

class Categoria:
    @staticmethod
    def obtener_todas():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT id, nombre, descripcion FROM categorias ORDER BY nombre"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(categoria_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT id, nombre, descripcion FROM categorias WHERE id = %s"
                cursor.execute(sql, (categoria_id,))
                return cursor.fetchone()
        finally:
            conn.close()