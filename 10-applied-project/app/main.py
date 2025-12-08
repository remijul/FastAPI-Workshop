"""
Point d'entrée de l'application.

TODO NIVEAU 1:
- Initialiser la base de données
- Créer l'application FastAPI
- Inclure le router

TODO NIVEAU 2:
- Ajouter les gestionnaires d'exceptions personnalisées
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.database import init_database
from app.routes import router
from app.config import APP_NAME, VERSION
# from app.exceptions import CharacterNotFoundError  # TODO NIVEAU 2: Décommenter

# TODO NIVEAU 1: Initialiser la base de données
# init_database()

# TODO NIVEAU 1: Créer l'application
app = FastAPI(
    title=APP_NAME,
    description="API REST pour gérer des personnages de jeu vidéo",
    version=VERSION
)


# TODO NIVEAU 2: Ajouter les gestionnaires d'exceptions
# Exemple:
# @app.exception_handler(CharacterNotFoundError)
# async def character_not_found_handler(request: Request, exc: CharacterNotFoundError):
#     return JSONResponse(
#         status_code=status.HTTP_404_NOT_FOUND,
#         content={"error": "Character Not Found", "message": exc.message}
#     )


# TODO NIVEAU 1: Inclure le router
# app.include_router(router)


@app.get("/")
def root():
    """Route racine."""
    return {
        "message": "API de gestion de personnages de jeu vidéo",
        "version": VERSION,
        "documentation": "/docs"
    }


# TODO NIVEAU 3 - Option Jinja2: Monter les fichiers statiques et configurer les templates
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# app.mount("/static", StaticFiles(directory="app/static"), name="static")
# templates = Jinja2Templates(directory="app/templates")


# Pour lancer:
# uvicorn app.main:app --reload