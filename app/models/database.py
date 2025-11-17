try:
    import mysql.connector
    USE_MYSQL_CONNECTOR = True
except ImportError:
    import pymysql
    USE_MYSQL_CONNECTOR = False

from flask import current_app

def get_db_connection():
    if USE_MYSQL_CONNECTOR:
        return mysql.connector.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME'],
            charset='utf8mb4'
        )
    else:
        return pymysql.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )