import mysql.connector
from config import DATABASE_CONFIG

def get_db_connection():
    config = DATABASE_CONFIG
    conn = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )
    cursor = conn.cursor()
    return conn, cursor
