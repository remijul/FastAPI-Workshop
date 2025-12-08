"""
Configuration de l'application.

Ce fichier centralise toutes les configurations.
"""

import os
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = os.getenv("DATABASE_PATH", "databases/characters.db")
DATA_DIR = BASE_DIR / "data"

# Classes de personnages autorisées
VALID_CLASSES = ["warrior", "mage", "archer", "tank", "healer"]

# Configuration JWT (pour niveau 3 - authentification)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuration de l'application
APP_NAME = "API Gestion de Personnages"
VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "True") == "True"