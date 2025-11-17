try:
    from flask import Flask
    print("✅ Flask está instalado correctamente")
    
    import pymysql
    print("✅ PyMySQL está instalado correctamente")
    
    from flask_bcrypt import Bcrypt
    print("✅ Flask-Bcrypt está instalado correctamente")
    
    from flask_jwt_extended import JWTManager
    print("✅ Flask-JWT-Extended está instalado correctamente")
    
    from dotenv import load_dotenv
    print("✅ python-dotenv está instalado correctamente")
    
    print("🎉 ¡Todas las dependencias están listas!")
    
except ImportError as e:
    print(f"❌ Error: {e}")
    print("💡 Ejecuta: pip install Flask PyMySQL flask-bcrypt flask-jwt-extended python-dotenv")