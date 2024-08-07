import mysql.connector
from config import DATABASE_CONFIG

def create_tables():
    config = DATABASE_CONFIG
    conn = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INT AUTO_INCREMENT PRIMARY KEY,
        content TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        query TEXT NOT NULL,
        response TEXT NOT NULL,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
