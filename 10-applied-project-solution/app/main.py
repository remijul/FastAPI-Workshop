"""
Point d'entrée de l'application.
SOLUTION COMPLÈTE
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.database import init_database, init_users_table
from app.routes import router, auth_router
from app.config import APP_NAME, VERSION
from app.exceptions import (
    CharacterNotFoundError,
    InvalidClassError,
    InvalidLevelError,
    MaxLevelReachedError
)

# Initialiser la base de données
init_database()
init_users_table()  # NIVEAU 3

# Créer l'application
app = FastAPI(
    title=APP_NAME,
    description="API REST pour gérer des personnages de jeu vidéo",
    version=VERSION
)

# Monter les fichiers statiques (NIVEAU 3 - Jinja2)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# ==================== GESTIONNAIRES D'EXCEPTIONS (NIVEAU 2) ====================

@app.exception_handler(CharacterNotFoundError)
async def character_not_found_handler(request: Request, exc: CharacterNotFoundError):
    """Gestionnaire pour CharacterNotFoundError."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Character Not Found",
            "message": exc.message,
            "character_id": exc.character_id
        }
    )


@app.exception_handler(InvalidClassError)
async def invalid_class_handler(request: Request, exc: InvalidClassError):
    """Gestionnaire pour InvalidClassError."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid Class",
            "message": exc.message,
            "provided_class": exc.character_class,
            "valid_classes": exc.valid_classes
        }
    )


@app.exception_handler(InvalidLevelError)
async def invalid_level_handler(request: Request, exc: InvalidLevelError):
    """Gestionnaire pour InvalidLevelError."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid Level",
            "message": exc.message,
            "provided_level": exc.level,
            "min_level": exc.min_level,
            "max_level": exc.max_level
        }
    )


@app.exception_handler(MaxLevelReachedError)
async def max_level_reached_handler(request: Request, exc: MaxLevelReachedError):
    """Gestionnaire pour MaxLevelReachedError."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Max Level Reached",
            "message": exc.message,
            "character_id": exc.character_id,
            "max_level": exc.max_level
        }
    )


# ==================== ROUTES ====================

# Inclure les routers
app.include_router(router)
app.include_router(auth_router)  # NIVEAU 3


@app.get("/")
def root():
    """Route racine."""
    return {
        "message": "API de gestion de personnages de jeu vidéo",
        "version": VERSION,
        "documentation": "/docs",
        "web_interface": "/characters/web/home"  # NIVEAU 3
    }


@app.get("/health")
def health_check():
    """Endpoint de santé pour monitoring."""
    return {"status": "healthy", "version": VERSION}


# Pour lancer:
# uvicorn app.main:app --reload