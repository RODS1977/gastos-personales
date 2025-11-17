from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.gastos_service import GastosService

gastos_bp = Blueprint('gastos', __name__)

@gastos_bp.route('/gastos', methods=['GET'])
@jwt_required()
def obtener_gastos():
    usuario_id = get_jwt_identity()
    return GastosService.obtener_gastos(usuario_id)

@gastos_bp.route('/gastos', methods=['POST'])
@jwt_required()
def crear_gasto():
    usuario_id = get_jwt_identity()
    return GastosService.crear_gasto(usuario_id, request.get_json())

@gastos_bp.route('/gastos/<int:gasto_id>', methods=['PUT'])
@jwt_required()
def actualizar_gasto(gasto_id):
    usuario_id = get_jwt_identity()
    return GastosService.actualizar_gasto(usuario_id, gasto_id, request.get_json())

@gastos_bp.route('/gastos/<int:gasto_id>', methods=['DELETE'])
@jwt_required()
def eliminar_gasto(gasto_id):
    usuario_id = get_jwt_identity()
    return GastosService.eliminar_gasto(usuario_id, gasto_id)