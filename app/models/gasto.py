from app.models.database import get_db_connection

class Gasto:
    @staticmethod
    def crear(usuario_id, categoria_id, monto, fecha, descripcion):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO gastos (usuario_id, categoria_id, monto, fecha, descripcion)
                    VALUES (%s, %s, %s, %s, %s)
                """, (usuario_id, categoria_id, monto, fecha, descripcion))
                return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def obtener_por_usuario(usuario_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT g.id, c.nombre as categoria, g.monto, g.fecha, g.descripcion,
                           g.fecha_creacion, g.fecha_actualizacion
                    FROM gastos g
                    JOIN categorias c ON g.categoria_id = c.id
                    WHERE g.usuario_id = %s
                    ORDER BY g.fecha DESC, g.fecha_creacion DESC
                """, (usuario_id,))
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(gasto_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT g.id, c.nombre as categoria, g.monto, g.fecha, g.descripcion,
                           g.fecha_creacion, g.fecha_actualizacion
                    FROM gastos g
                    JOIN categorias c ON g.categoria_id = c.id
                    WHERE g.id = %s
                """, (gasto_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id_y_usuario(gasto_id, usuario_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT g.id, c.nombre as categoria, g.monto, g.fecha, g.descripcion
                    FROM gastos g
                    JOIN categorias c ON g.categoria_id = c.id
                    WHERE g.id = %s AND g.usuario_id = %s
                """, (gasto_id, usuario_id))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def actualizar(gasto_id, campos):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                set_clause = ', '.join([f"{key} = %s" for key in campos.keys()])
                valores = list(campos.values())
                valores.append(gasto_id)
                
                cursor.execute(
                    f"UPDATE gastos SET {set_clause} WHERE id = %s",
                    valores
                )
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def eliminar(gasto_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM gastos WHERE id = %s", (gasto_id,))
                conn.commit()
        finally:
            conn.close()