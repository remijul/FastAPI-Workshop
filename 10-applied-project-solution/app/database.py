"""
Gestion de la base de données SQLite.
SOLUTION COMPLÈTE
"""

import sqlite3
import json
from pathlib import Path
from app.config import DATABASE_PATH, DATA_DIR


def get_db_connection():
    """Crée une connexion à la base de données."""
    # Créer le dossier databases s'il n'existe pas
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialise la base de données et charge les données initiales."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Créer la table characters
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class TEXT NOT NULL,
            level INTEGER NOT NULL,
            health_points INTEGER NOT NULL,
            attack INTEGER NOT NULL,
            defense INTEGER NOT NULL,
            speed INTEGER NOT NULL,
            special_ability TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Vérifier si la table est vide
    cursor.execute("SELECT COUNT(*) FROM characters")
    count = cursor.fetchone()[0]
    
    # Si vide, charger les données initiales
    if count == 0:
        load_initial_data(cursor)
    
    conn.commit()
    conn.close()


def load_initial_data(cursor):
    """Charge les 10 personnages depuis data/initial_characters.json."""
    json_path = DATA_DIR / "initial_characters.json"
    
    with open(json_path, "r", encoding="utf-8") as f:
        characters = json.load(f)
    
    for char in characters:
        cursor.execute("""
            INSERT INTO characters (name, class, level, health_points, attack, defense, speed, special_ability, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            char["name"],
            char["class"],
            char["level"],
            char["health_points"],
            char["attack"],
            char["defense"],
            char["speed"],
            char.get("special_ability"),
            char.get("image_url")
        ))


# ==================== NIVEAU 3 - OPTION AUTH ====================

def init_users_table():
    """Initialise la table des utilisateurs."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            hashed_password TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()