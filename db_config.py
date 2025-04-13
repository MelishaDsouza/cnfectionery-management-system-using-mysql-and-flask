# db_config.py
import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Melisha123456',
        database='Conf'
    )
    return conn