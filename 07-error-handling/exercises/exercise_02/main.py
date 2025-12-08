"""
Exercice 2 - Point d'entrée avec middleware

TODO 3: Ajouter un middleware de logging et les gestionnaires d'exceptions
- Créer un middleware qui log chaque requête
- Créer les gestionnaires pour les 3 exceptions
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import logging
from .database import init_database
from .routes import router
from .exceptions import RoomNotFoundError, RoomNotAvailableError, InvalidDateError

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

init_database()

app = FastAPI(
    title="API Réservation d'Hôtel",
    description="API avec middleware et gestion d'erreurs",
    version="1.0.0"
)


# TODO 3: Créer le middleware de logging
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     logger.info(f"Request: {request.method} {request.url.path}")
#     response = await call_next(request)
#     logger.info(f"Status: {response.status_code}")
#     return response


# TODO 3: Créer les gestionnaires d'exceptions


app.include_router(router)


# Pour lancer :
# uvicorn exercises.exercise_02.main:app --reload