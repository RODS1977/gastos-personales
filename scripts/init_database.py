import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import mysql.connector
except ImportError:
    import pymysql
    import os
from dotenv import load_dotenv

load_dotenv()

def get_connection(use_database=False):
    """Obtener conexión a MySQL"""
    try:
        # Intentar con mysql-connector-python primero
        if use_database:
            return mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'gastos_personales_db')
            )
        else:
            return mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', '')
            )
    except ImportError:
        # Fallback a PyMySQL
        if use_database:
            return pymysql.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'gastos_personales_db'),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        else:
            return pymysql.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

def init_database():
    """Inicializar base de datos y tablas"""
    conn = None
    try:
        print("🔗 Conectando a MySQL...")
        conn = get_connection(use_database=False)
        cursor = conn.cursor()
        
        db_name = os.getenv('DB_NAME', 'gastos_personales_db')
        
        print(f"📊 Creando base de datos '{db_name}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        
        print("🗂️ Creando tablas...")
        
        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(150) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de categorías
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) UNIQUE NOT NULL,
                descripcion TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de gastos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gastos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                categoria_id INT NOT NULL,
                monto DECIMAL(10, 2) NOT NULL,
                fecha DATE NOT NULL,
                descripcion VARCHAR(255),
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE RESTRICT
            )
        """)
        
        # Insertar categorías predeterminadas
        categorias = [
            ('comida', 'Gastos en alimentación y restaurantes'),
            ('transporte', 'Transporte público, gasolina, taxi, etc.'),
            ('entretenimiento', 'Cine, conciertos, hobbies'),
            ('salud', 'Medicamentos, consultas médicas, seguro'),
            ('educacion', 'Cursos, libros, material educativo'),
            ('otros', 'Otros gastos no categorizados')
        ]
        
        print("📝 Insertando categorías predeterminadas...")
        for categoria in categorias:
            cursor.execute(
                "INSERT IGNORE INTO categorias (nombre, descripcion) VALUES (%s, %s)",
                categoria
            )
        
        conn.commit()
        print("✅ Base de datos y tablas creadas exitosamente")
        print(f"📊 Base de datos: {db_name}")
        print("📋 Tablas: usuarios, categorias, gastos")
        print("🎯 Categorías: comida, transporte, entretenimiento, salud, educacion, otros")
        
    except Exception as e:
        print(f"❌ Error al crear la base de datos: {str(e)}")
        print("💡 Soluciones:")
        print("   1. Ejecuta: pip install mysql-connector-python")
        print("   2. O ejecuta: pip install cryptography")
        print("   3. Verifica que MySQL esté ejecutándose")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔒 Conexión cerrada")

if __name__ == '__main__':
    init_database()