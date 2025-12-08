"""
Exercice 2 - Point d'entrée

TODO 5: Assembler l'application
"""

from fastapi import FastAPI
from .database import init_database
from .routes import router

# TODO 5: Compléter

# Pour lancer :
# uvicorn exercises.exercise_02.main:app --reload