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
            categorias = cursor.fetchall()
        
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