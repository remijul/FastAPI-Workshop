"""
Gestion de la base de données SQLite.

TODO NIVEAU 1:
- Implémenter get_db_connection()
- Implémenter init_database() avec création de la table characters
- Implémenter load_initial_data() pour charger les 10 personnages

Rappel: La table doit contenir les colonnes correspondant au modèle Character.
"""

import sqlite3
import json
from pathlib import Path
from app.config import DATABASE_PATH, DATA_DIR


def get_db_connection():
    """
    Crée une connexion à la base de données.
    
    TODO NIVEAU 1:
    - Créer le dossier databases s'il n'existe pas (Path.mkdir)
    - Créer la connexion avec sqlite3.connect()
    - Définir row_factory = sqlite3.Row pour accéder aux colonnes par nom
    - Retourner la connexion
    """
    # TODO: Implémenter
    pass


def init_database():
    """
    Initialise la base de données et charge les données initiales.
    
    TODO NIVEAU 1:
    - Créer la table characters avec toutes les colonnes
    - Vérifier si la table est vide
    - Si vide, appeler load_initial_data()
    
    Colonnes de la table:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - name: TEXT NOT NULL
    - class: TEXT NOT NULL
    - level: INTEGER NOT NULL
    - health_points: INTEGER NOT NULL
    - attack: INTEGER NOT NULL
    - defense: INTEGER NOT NULL
    - speed: INTEGER NOT NULL
    - special_ability: TEXT
    - image_url: TEXT
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
    # TODO: Implémenter
    pass


def load_initial_data(cursor):
    """
    Charge les 10 personnages depuis data/initial_characters.json.
    
    TODO NIVEAU 1:
    - Ouvrir le fichier data/initial_characters.json
    - Parser le JSON
    - Insérer chaque personnage dans la table
    
    Args:
        cursor: Curseur de la base de données
    """
    # TODO: Implémenter
    pass


# TODO NIVEAU 3 - Option Auth: Créer la table users si nécessaire
def init_users_table():
    """
    Initialise la table des utilisateurs (pour l'authentification).
    
    TODO NIVEAU 3 (optionnel):
    - Créer la table users avec: id, username, hashed_password
    """
    pass