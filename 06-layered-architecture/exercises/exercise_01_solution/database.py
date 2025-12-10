"""
Solution Exercice 1 - Gestion de la base de données
"""

import sqlite3

DATABASE_PATH = "databases/exercise_01.db"


def get_db_connection():
    """Crée une connexion à la base de données."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """
    Initialise la base de données.
    
    Créer une table "notes" avec :
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - student_name: TEXT NOT NULL
    - subject: TEXT NOT NULL
    - grade: REAL NOT NULL
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            grade REAL NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()