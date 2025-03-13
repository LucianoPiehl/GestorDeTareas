import mysql.connector
from flask import g

def get_db():
    """Obtiene la conexión a la base de datos, reutilizándola si ya existe."""
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gestordetareas"
        )
    return g.db

def close_db(e=None):
    """Cierra la conexión a la base de datos si existe."""
    db = g.pop('db', None)
    if db is not None:
        db.close()
