"""
Exercice 2 - Point d'entrée

TODO 3: Assembler l'application
"""

from fastapi import FastAPI
from .database import init_database
from .routes import auth_router, tasks_router

# TODO 3: Compléter

# Pour lancer :
# uvicorn exercises.exercise_02.main:app --reload