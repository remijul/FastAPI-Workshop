"""
Couche Base de Données : Gestion de la connexion

Cette couche contient :
- La configuration de la base de données
- Les fonctions utilitaires pour la connexion
- L'initialisation de la base
"""

import sqlite3

DATABASE_PATH = "databases/layered.db"


def get_db_connection():
    """
    Crée et retourne une connexion à la base de données.
    
    Returns:
        Connexion SQLite configurée
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialise la base de données avec les tables nécessaires."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()