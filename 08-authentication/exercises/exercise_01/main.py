"""
Exercice 1 - Point d'entrée

TODO 3: Assembler l'application
- Initialiser la base
- Créer l'app FastAPI
- Inclure les routers (auth_router et articles_router)
"""

from fastapi import FastAPI
from .database import init_database
from .routes import auth_router, articles_router

# TODO 3: Compléter

# Pour lancer :
# uvicorn exercises.exercise_01.main:app --reload