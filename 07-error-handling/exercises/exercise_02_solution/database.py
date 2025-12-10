"""Solution Exercice 2 - Base de données"""

import sqlite3

DATABASE_PATH = "databases/exercise_02.db"


def get_db_connection():
    """Crée une connexion à la base de données."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialise les tables rooms et reservations."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            price_per_night REAL NOT NULL,
            available INTEGER NOT NULL DEFAULT 1
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            guest_name TEXT NOT NULL,
            nights INTEGER NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
    """)
    
    conn.commit()
    conn.close()