"""
Concepts : Middleware de gestion d'erreurs

Un middleware intercepte toutes les requêtes et réponses.
Utile pour :
- Logger toutes les erreurs
- Formater les réponses d'erreur de manière uniforme
- Gérer les erreurs inattendues
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import time
import logging

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API avec Middleware d'Erreurs",
    description="Démonstration du middleware de gestion d'erreurs",
    version="1.0.0"
)


# Middleware pour logger et gérer les erreurs
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    """
    Middleware qui :
    - Log toutes les requêtes
    - Capture les erreurs inattendues
    - Retourne des réponses formatées
    """
    start_time = time.time()
    
    try:
        # Logger la requête entrante
        logger.info(f"Request: {request.method} {request.url.path}")
        
        # Exécuter la requête
        response = await call_next(request)
        
        # Logger le temps de traitement
        process_time = time.time() - start_time
        logger.info(f"Completed in {process_time:.3f}s - Status: {response.status_code}")
        
        return response
    
    except Exception as exc:
        # Logger l'erreur
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
        
        # Retourner une réponse d'erreur formatée
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "message": "Une erreur inattendue s'est produite",
                "type": type(exc).__name__
            }
        )


# Routes de démonstration
@app.get("/")
def root():
    """Route qui fonctionne normalement."""
    return {"message": "API avec middleware d'erreurs"}


@app.get("/error")
def trigger_error():
    """Route qui déclenche une erreur volontairement."""
    # Ceci va déclencher une ZeroDivisionError
    result = 1 / 0
    return {"result": result}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Route qui peut déclencher une erreur."""
    items = {1: "Laptop", 2: "Mouse"}
    
    # Ceci peut déclencher une KeyError
    return {"item": items[item_id]}


# Pour lancer :
# uvicorn concepts.concepts_03_error_middleware:app --reload
#
# Tester :
# 1. GET / → Fonctionne, logs dans la console
# 2. GET /error → Erreur 500, capturée par le middleware
# 3. GET /items/1 → Fonctionne
# 4. GET /items/999 → Erreur 500, KeyError capturée
#
# Le middleware capture TOUTES les erreurs non gérées
# et retourne une réponse uniforme au lieu de crasher