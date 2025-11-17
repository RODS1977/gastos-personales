from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # ← NUEVO
from config import config

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Habilitar CORS para todas las rutas ← NUEVO
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
    
    # Inicializar extensiones
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.gastos import gastos_bp
    from app.routes.categorias import categorias_bp
    # Registrar blueprint principal (sirve frontend / o info de API)
    try:
        # Prefer the frontend-serving blueprint if available
        from app.routes.main import main_bp as main_bp_prefer
        main_bp_to_register = main_bp_prefer
    except Exception:
        # Fallback to `app.routes` package-level blueprint
        from app.routes import main_bp as main_bp_fallback
        main_bp_to_register = main_bp_fallback
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(gastos_bp, url_prefix='/api')
    app.register_blueprint(categorias_bp, url_prefix='/api')
    # Registrar sin prefijo para que '/' esté disponible
    app.register_blueprint(main_bp_to_register)
    
    return app