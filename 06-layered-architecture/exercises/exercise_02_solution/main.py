"""
Solution Exercice 2 - Point d'entrée
"""

from fastapi import FastAPI
from .database import init_database
from .routes import router

# Solution TODO 5: Compléter

# Initialiser la base de données
init_database()

# Créer l'application
app = FastAPI(
    title="API Gestion de Tâches",
    description="API avec architecture en couches pour gérer les tâches avec priorités",
    version="1.0.0"
)

# Inclure le router
app.include_router(router)


@app.get("/")
def root():
    """Route racine."""
    return {
        "message": "API de gestion de tâches avec priorités",
        "endpoints": {
            "POST /tasks": "Créer une tâche",
            "GET /tasks": "Lister toutes les tâches",
            "GET /tasks/{id}": "Récupérer une tâche",
            "PUT /tasks/{id}/complete": "Compléter une tâche"
        }
    }


# Pour lancer :
# uvicorn exercises.exercise_02_solution.main:app --reload