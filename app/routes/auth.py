from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['POST'])
def registro():
    return AuthService.registrar_usuario(request.get_json())

@auth_bp.route('/login', methods=['POST'])
def login():
    return AuthService.login_usuario(request.get_json())