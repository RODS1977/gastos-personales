from flask import Blueprint, jsonify, send_from_directory
import os

main_bp = Blueprint('main', __name__)

# Ruta para la página principal
@main_bp.route('/')
def serve_frontend():
    # Obtener la ruta absoluta del directorio frontend
    frontend_path = os.path.join(os.path.dirname(__file__), '../../frontend')
    return send_from_directory(frontend_path, 'index.html')

# Ruta para archivos estáticos (CSS, JS, etc.)
@main_bp.route('/<path:filename>')
def serve_static_files(filename):
    frontend_path = os.path.join(os.path.dirname(__file__), '../../frontend')
    return send_from_directory(frontend_path, filename)

# Ruta de información de la API
@main_bp.route('/api/info')
def api_info():
    return jsonify({
        "status": "success",
        "message": "API de Gastos Personales",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth/registro, /auth/login",
            "gastos": "/api/gastos",
            "categorias": "/api/categorias"
        }
    })