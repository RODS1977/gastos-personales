from datetime import datetime

def validar_monto(monto):
    return isinstance(monto, (int, float)) and monto > 0

def validar_fecha(fecha_str):
    try:
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validar_descripcion(descripcion):
    return isinstance(descripcion, str) and len(descripcion) <= 255