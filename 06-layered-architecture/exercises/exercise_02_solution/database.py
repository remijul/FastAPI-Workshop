"""Solution Exercice 2 - Base de données"""

import sqlite3

DATABASE_PATH = "databases/exercise_02.db"


def get_db_connection():
    """Crée une connexion à la base de données."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """
    Initialise la base avec table "tasks" :
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - title: TEXT NOT NULL
    - priority: INTEGER NOT NULL
    - completed: INTEGER NOT NULL DEFAULT 0
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority INTEGER NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)
    
    conn.commit()
    conn.close()