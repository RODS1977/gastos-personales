from flask import jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models.usuario import Usuario
from app.utils.responses import success_response, error_response
import re

class AuthService:
    @staticmethod
    def registrar_usuario(data):
        try:
            # Validar que se recibieron datos
            if not data:
                return error_response('Datos JSON requeridos', status_code=400)
            
            # Extraer y validar campos requeridos
            nombre = data.get('nombre', '').strip()
            correo = data.get('correo', '').strip().lower()
            password = data.get('password', '')
            
            # Validaciones de campos obligatorios
            if not nombre:
                return error_response('El nombre es requerido', status_code=400)
            
            if not correo:
                return error_response('El correo electrónico es requerido', status_code=400)
            
            if not password:
                return error_response('La contraseña es requerida', status_code=400)
            
            # Validar formato de correo electrónico
            if not AuthService.validar_correo(correo):
                return error_response('Formato de correo electrónico inválido', status_code=400)
            
            # Validar fortaleza de contraseña
            if not AuthService.validar_password(password):
                return error_response(
                    'La contraseña debe tener al menos 6 caracteres, una mayúscula y un número', 
                    status_code=400
                )
            
            # Validar longitud del nombre
            if len(nombre) < 2 or len(nombre) > 100:
                return error_response('El nombre debe tener entre 2 y 100 caracteres', status_code=400)
            
            # Verificar si el correo ya existe
            usuario_existente = Usuario.obtener_por_correo(correo)
            if usuario_existente:
                return error_response('El correo electrónico ya está registrado', status_code=400)
            
            # Hash de la contraseña
            password_hash = generate_password_hash(password).decode('utf-8')
            
            # Crear usuario en la base de datos
            usuario_id = Usuario.crear(nombre, correo, password_hash)
            
            # Crear token de acceso
            access_token = create_access_token(identity=usuario_id)
            
            # Preparar datos de respuesta
            user_data = {
                'id': usuario_id,
                'nombre': nombre,
                'correo': correo,
                'access_token': access_token
            }
            
            return success_response(
                message='Usuario registrado exitosamente', 
                data=user_data, 
                status_code=201
            )
            
        except Exception as e:
            return error_response(f'Error interno del servidor: {str(e)}', status_code=500)

    @staticmethod
    def login_usuario(data):
        try:
            # Validar que se recibieron datos
            if not data:
                return error_response('Datos JSON requeridos', status_code=400)
            
            # Extraer credenciales
            correo = data.get('correo', '').strip().lower()
            password = data.get('password', '')
            
            # Validar campos obligatorios
            if not correo or not password:
                return error_response('Correo y contraseña son requeridos', status_code=400)
            
            # Buscar usuario por correo
            usuario = Usuario.obtener_por_correo(correo)
            if not usuario:
                return error_response('Credenciales inválidas', status_code=401)
            
            # Verificar contraseña
            if not check_password_hash(usuario['password_hash'], password):
                return error_response('Credenciales inválidas', status_code=401)
            
            # Crear token de acceso
            access_token = create_access_token(identity=usuario['id'])
            
            # Preparar datos de respuesta
            user_data = {
                'id': usuario['id'],
                'nombre': usuario['nombre'],
                'correo': usuario['correo'],
                'access_token': access_token
            }
            
            return success_response(
                message='Login exitoso', 
                data=user_data, 
                status_code=200
            )
            
        except Exception as e:
            return error_response(f'Error interno del servidor: {str(e)}', status_code=500)

    @staticmethod
    def validar_correo(correo):
        """Validar formato de correo electrónico"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, correo) is not None

    @staticmethod
    def validar_password(password):
        """
        Validar fortaleza de contraseña
        - Mínimo 6 caracteres
        - Al menos una mayúscula
        - Al menos un número
        """
        if len(password) < 6:
            return False
        
        tiene_mayuscula = any(c.isupper() for c in password)
        tiene_numero = any(c.isdigit() for c in password)
        
        return tiene_mayuscula and tiene_numero

    @staticmethod
    def obtener_perfil(usuario_id):
        try:
            usuario = Usuario.obtener_por_id(usuario_id)
            if not usuario:
                return error_response('Usuario no encontrado', status_code=404)
            
            return success_response(
                message='Perfil obtenido exitosamente',
                data=usuario,
                status_code=200
            )
            
        except Exception as e:
            return error_response(f'Error interno del servidor: {str(e)}', status_code=500)