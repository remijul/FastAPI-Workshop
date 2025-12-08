"""
Solution Exercice 2 - Point d'entrée
"""

from fastapi import FastAPI
from .database import init_database
from .routes import auth_router, tasks_router

# Solution TODO 3

# Initialiser la base
init_database()

# Créer l'app
app = FastAPI(
    title="API Tâches avec Rôles",
    description="API de gestion de tâches avec authentification et autorisation",
    version="1.0.0"
)

# Inclure les routers
app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/")
def root():
    """Route racine."""
    return {
        "message": "API Tâches avec authentification et rôles",
        "roles": {
            "user": "Peut créer et voir ses tâches",
            "admin": "Peut voir toutes les tâches et les supprimer"
        },
        "endpoints": {
            "POST /auth/register": "Créer un compte (user ou admin)",
            "POST /auth/login": "Se connecter",
            "POST /tasks": "Créer une tâche (user/admin)",
            "GET /tasks/my-tasks": "Mes tâches (user/admin)",
            "GET /tasks/all": "Toutes les tâches (admin only)",
            "DELETE /tasks/{id}": "Supprimer une tâche (admin only)"
        }
    }


# Pour lancer :
# uvicorn exercises.exercise_02_solution.main:app --reload