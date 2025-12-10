"""
Solution Exercice 2 - Point d'entrée avec middleware
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import logging
import time
from .database import init_database
from .routes import router
from .exceptions import RoomNotFoundError, RoomNotAvailableError, InvalidDateError

# Configurer le logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

init_database()

app = FastAPI(
    title="API Réservation d'Hôtel",
    description="API avec middleware et gestion d'erreurs",
    version="1.0.0"
)


# Solution TODO 3: Créer le middleware de logging

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware qui log toutes les requêtes.
    
    Log :
    - Méthode et chemin de la requête
    - Temps de traitement
    - Code de statut de la réponse
    """
    start_time = time.time()
    
    # Logger la requête entrante
    logger.info(f"Request: {request.method} {request.url.path}")
    
    # Exécuter la requête
    response = await call_next(request)
    
    # Calculer le temps de traitement
    process_time = time.time() - start_time
    
    # Logger la réponse
    logger.info(
        f"Completed: {request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Duration: {process_time:.3f}s"
    )
    
    return response


# Solution TODO 3: Créer les gestionnaires d'exceptions

@app.exception_handler(RoomNotFoundError)
async def room_not_found_handler(request: Request, exc: RoomNotFoundError):
    """Gère les erreurs RoomNotFoundError."""
    logger.warning(f"RoomNotFoundError: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Room Not Found",
            "message": exc.message,
            "room_id": exc.room_id
        }
    )


@app.exception_handler(RoomNotAvailableError)
async def room_not_available_handler(request: Request, exc: RoomNotAvailableError):
    """Gère les erreurs RoomNotAvailableError."""
    logger.warning(f"RoomNotAvailableError: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Room Not Available",
            "message": exc.message,
            "room_id": exc.room_id,
            "room_name": exc.room_name
        }
    )


@app.exception_handler(InvalidDateError)
async def invalid_date_handler(request: Request, exc: InvalidDateError):
    """Gère les erreurs InvalidDateError."""
    logger.warning(f"InvalidDateError: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid Date",
            "message": exc.message
        }
    )


app.include_router(router)


@app.get("/")
def root():
    """Route racine."""
    return {
        "message": "API de réservation d'hôtel",
        "features": [
            "Gestion des chambres",
            "Système de réservation",
            "Middleware de logging",
            "Gestion d'erreurs personnalisées"
        ]
    }


# Pour lancer :
# uvicorn exercises.exercise_02_solution.main:app --reload
#
# Le middleware logge toutes les requêtes dans la console.
# Observez les logs lors des tests !