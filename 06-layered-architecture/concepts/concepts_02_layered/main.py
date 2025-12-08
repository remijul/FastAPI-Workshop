"""
Point d'entrée de l'application

Ce fichier assemble toutes les couches :
- Initialise la base de données
- Crée l'application FastAPI
- Enregistre les routes
"""

from fastapi import FastAPI
from .database import init_database
from .routes import router

# Initialiser la base de données
init_database()

# Créer l'application
app = FastAPI(
    title="API avec Architecture en Couches",
    description="Démonstration de la séparation des responsabilités",
    version="1.0.0"
)

# Enregistrer les routes
app.include_router(router)


@app.get("/")
def root():
    """Route racine."""
    return {
        "message": "API avec architecture en couches",
        "architecture": {
            "models": "Structures de données (Pydantic)",
            "database": "Gestion de la connexion",
            "repositories": "Accès aux données (SQL)",
            "services": "Logique métier",
            "routes": "Points d'entrée HTTP"
        }
    }


# Pour lancer :
# uvicorn concepts.concepts_02_layered.main:app --reload
#
# Avantages de cette architecture :
# 1. Code organisé et maintenable
# 2. Facile à tester (chaque couche indépendamment)
# 3. Réutilisation du code
# 4. Séparation des responsabilités claire