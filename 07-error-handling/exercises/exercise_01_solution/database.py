"""Solution Exercice 1 - Base de données"""

import sqlite3

DATABASE_PATH = "databases/exercise_01.db"


def get_db_connection():
    """Crée une connexion à la base de données."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialise la base avec table accounts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_name TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0.0
        )
    """)
    
    conn.commit()
    conn.close()