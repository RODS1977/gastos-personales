from app import create_app
import os

# Crear la aplicación Flask
app = create_app()

if __name__ == '__main__':
    # Obtener configuración del entorno
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Iniciando servidor en: http://{host}:{port}")
    print(f"📊 Modo debug: {debug}")
    print("⏹️  Presiona Ctrl+C para detener el servidor")
    
    # Ejecutar la aplicación
    app.run(host=host, port=port, debug=debug)