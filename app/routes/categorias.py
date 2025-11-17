from flask import Blueprint, jsonify
from app.models.database import get_db_connection

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/categorias', methods=['GET'])
def obtener_categorias():
    """Obtener todas las categorías"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion FROM categorias ORDER BY nombre")
            rows = cursor.fetchall()
            # Normalizar filas a objetos dict con claves conocidas
            categorias = []
            if rows:
                # Si el cursor devuelve diccionarios (pymysql.DictCursor), las filas
                # ya tendrán claves; si devuelve tuplas (mysql-connector), convertir
                first = rows[0]
                if isinstance(first, dict):
                    categorias = rows
                else:
                    for r in rows:
                        categorias.append({
                            'id': r[0],
                            'nombre': r[1],
                            'descripcion': r[2]
                        })
        
        return jsonify({
            'status': 'success',
            'data': categorias
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error al obtener categorías: {str(e)}'
        }), 500
    finally:
        if conn:
            conn.close()