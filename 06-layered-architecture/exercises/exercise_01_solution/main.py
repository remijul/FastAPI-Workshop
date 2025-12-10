"""
Solution Exercice 1 - Point d'entrée
"""

from fastapi import FastAPI
from .database import init_database
from .routes import router

# Solution TODO 5: Initialiser la base
init_database()

# Solution TODO 5: Créer l'app
app = FastAPI(
    title="API Gestion de Notes",
    description="API avec architecture en couches pour gérer les notes d'étudiants",
    version="1.0.0"
)

# Solution TODO 5: Inclure le router
app.include_router(router)


@app.get("/")
def root():
    """Route racine."""
    return {
        "message": "API de gestion de notes d'étudiants",
        "endpoints": {
            "POST /notes": "Créer une note",
            "GET /notes": "Lister toutes les notes",
            "GET /notes/{id}": "Récupérer une note"
        }
    }


# Pour lancer :
# uvicorn exercises.exercise_01_solution.main:app --reload