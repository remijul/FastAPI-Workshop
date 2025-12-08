"""
Solution Exercice 1 - Point d'entrée
"""

from fastapi import FastAPI
from .database import init_database
from .routes import auth_router, articles_router

# Solution TODO 3

# Initialiser la base
init_database()

# Créer l'app
app = FastAPI(
    title="API Blog avec Authentification",
    description="API de blog avec JWT",
    version="1.0.0"
)

# Inclure les routers
app.include_router(auth_router)
app.include_router(articles_router)


@app.get("/")
def root():
    """Route racine."""
    return {
        "message": "API Blog avec authentification JWT",
        "endpoints": {
            "POST /auth/register": "Créer un compte",
            "POST /auth/login": "Se connecter (obtenir un token)",
            "GET /articles": "Lister les articles (public)",
            "POST /articles": "Créer un article (protégé)",
            "GET /articles/my-articles": "Mes articles (protégé)"
        }
    }


# Pour lancer :
# uvicorn exercises.exercise_01_solution.main:app --reload