from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
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