from app.models.gasto import Gasto
from app.utils.responses import success_response, error_response
from app.utils.validations import validar_monto, validar_fecha, validar_descripcion

class GastosService:
    @staticmethod
    def obtener_gastos(usuario_id):
        try:
            gastos = Gasto.obtener_por_usuario(usuario_id)
            return success_response(
                message='Gastos obtenidos exitosamente',
                data=gastos,
                status_code=200
            )
        except Exception as e:
            return error_response(f'Error interno del servidor: {str(e)}', status_code=500)

    @staticmethod
    def crear_gasto(usuario_id, data):
        try:
            if not data:
                return error_response('Datos JSON requeridos', status_code=400)
            
            # Extraer y validar campos
            categoria_id = data.get('categoria_id')
            monto = data.get('monto')
            fecha = data.get('fecha')
            descripcion = data.get('descripcion', '').strip()
            
            # Validaciones
            errores = []
            
            if not categoria_id:
                errores.append('La categoría es requerida')
            elif not isinstance(categoria_id, int) or categoria_id <= 0:
                errores.append('ID de categoría inválido')
            
            if not validar_monto(monto):
                errores.append('Monto debe ser un número positivo')
            
            if not fecha or not validar_fecha(fecha):
                errores.append('Fecha inválida. Formato: YYYY-MM-DD')
            
            if not validar_descripcion(descripcion):
                errores.append('Descripción muy larga (máx. 255 caracteres)')
            
            if errores:
                return error_response('Errores de validación', errors=errores, status_code=400)
            
            # Crear gasto
            gasto_id = Gasto.crear(usuario_id, categoria_id, monto, fecha, descripcion)
            
            # Obtener gasto creado
            nuevo_gasto = Gasto.obtener_por_id(gasto_id)
            
            return success_response(
                message='Gasto creado exitosamente',
                data=nuevo_gasto,
                status_code=201
            )
            
        except Exception as e:
            return error_response(f'Error interno del servidor: {str(e)}', status_code=500)

    @staticmethod
    def actualizar_gasto(usuario_id, gasto_id, data):
        try:
            if not data:
                return error_response('Datos JSON requeridos', status_code=400)
            
            # Verificar que el gasto existe y pertenece al usuario
            gasto_existente = Gasto.obtener_por_id_y_usuario(gasto_id, usuario_id)
            if not gasto_existente:
                return error_response('Gasto no encontrado', status_code=404)
            
            # Validar campos a actualizar
            campos_actualizables = {}
            errores = []
            
            if 'categoria_id' in data:
                categoria_id = data['categoria_id']
                if not isinstance(categoria_id, int) or categoria_id <= 0:
                    errores.append('ID de categoría inválido')
                else:
                    campos_actualizables['categoria_id'] = categoria_id
            
            if 'monto' in data:
                monto = data['monto']
                if not validar_monto(monto):
                    errores.append('Monto debe ser un número positivo')
                else:
                    campos_actualizables['monto'] = monto
            
            if 'fecha' in data:
                fecha = data['fecha']
                if not fecha or not validar_fecha(fecha):
                    errores.append('Fecha inválida. Formato: YYYY-MM-DD')
                else:
                    campos_actualizables['fecha'] = fecha
            
            if 'descripcion' in data:
                descripcion = data['descripcion'].strip()
                if not validar_descripcion(descripcion):
                    errores.append('Descripción muy larga (máx. 255 caracteres)')
                else:
                    campos_actualizables['descripcion'] = descripcion
            
            if errores:
                return error_response('Errores de validación', errors=errores, status_code=400)
            
            # Actualizar gasto si hay campos válidos
            if campos_actualizables:
                Gasto.actualizar(gasto_id, campos_actualizables)
            
            # Obtener gasto actualizado
            gasto_actualizado = Gasto.obtener_por_id(gasto_id)
            
            return success_response(
                message='Gasto actualizado exitosamente',
                data=gasto_actualizado,
                status_code=200
            )
            
        except Exception as e:
            return error_response(f'Error interno del servidor: {str(e)}', status_code=500)

    @staticmethod
    def eliminar_gasto(usuario_id, gasto_id):
        try:
            # Verificar que el gasto existe y pertenece al usuario
            gasto = Gasto.obtener_por_id_y_usuario(gasto_id, usuario_id)
            if not gasto:
                return error_response('Gasto no encontrado', status_code=404)
            
            # Eliminar gasto
            Gasto.eliminar(gasto_id)
            
            return success_response(
                message='Gasto eliminado exitosamente',
                data={'gasto_eliminado': gasto},
                status_code=200
            )
            
        except Exception as e:
            return error_response(f'Error interno del servidor: {str(e)}', status_code=500)