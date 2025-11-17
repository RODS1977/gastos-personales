try:
    import mysql.connector
    print("✅ mysql-connector-python instalado")
    
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='tu_password'
    )
    print("✅ Conexión a MySQL exitosa")
    conn.close()
    
except ImportError:
    print("❌ mysql-connector-python no instalado")
    print("💡 Ejecuta: pip install mysql-connector-python")
    
except Exception as e:
    print(f"❌ Error de conexión: {e}")