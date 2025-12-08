"""
Exercice 1 - Point d'entrée

TODO 3: Configurer les gestionnaires d'exceptions
- Créer un exception_handler pour AccountNotFoundError (404)
- Créer un exception_handler pour InsufficientFundsError (400)
- Créer un exception_handler pour NegativeAmountError (400)
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from .database import init_database
from .routes import router
from .exceptions import (
    AccountNotFoundError,
    InsufficientFundsError,
    NegativeAmountError
)

init_database()

app = FastAPI(
    title="API Gestion de Comptes Bancaires",
    description="API avec gestion d'erreurs personnalisées",
    version="1.0.0"
)


# TODO 3: Créer les gestionnaires d'exceptions
# Exemple :
# @app.exception_handler(AccountNotFoundError)
# async def account_not_found_handler(request: Request, exc: AccountNotFoundError):
#     return JSONResponse(
#         status_code=status.HTTP_404_NOT_FOUND,
#         content={"error": "Account Not Found", "message": exc.message}
#     )


app.include_router(router)


# Pour lancer :
# uvicorn exercises.exercise_01.main:app --reload