"""
Exercice 1 - Point d'entrée

TODO 5: Assembler l'application
- Initialiser la base de données
- Créer l'app FastAPI
- Inclure le router
"""

from fastapi import FastAPI
from .database import init_database
from .routes import router

# TODO 5: Initialiser la base
# TODO 5: Créer l'app
# TODO 5: Inclure le router

# Pour lancer :
# uvicorn exercises.exercise_01.main:app --reload