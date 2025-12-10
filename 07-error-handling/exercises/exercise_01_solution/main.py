"""
Solution Exercice 1 - Point d'entrée
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


# Solution TODO 3: Créer les gestionnaires d'exceptions

@app.exception_handler(AccountNotFoundError)
async def account_not_found_handler(request: Request, exc: AccountNotFoundError):
    """Gère les erreurs AccountNotFoundError."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Account Not Found",
            "message": exc.message,
            "account_id": exc.account_id
        }
    )


@app.exception_handler(InsufficientFundsError)
async def insufficient_funds_handler(request: Request, exc: InsufficientFundsError):
    """Gère les erreurs InsufficientFundsError."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Insufficient Funds",
            "message": exc.message,
            "account_id": exc.account_id,
            "requested": exc.amount,
            "balance": exc.balance
        }
    )


@app.exception_handler(NegativeAmountError)
async def negative_amount_handler(request: Request, exc: NegativeAmountError):
    """Gère les erreurs NegativeAmountError."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Negative Amount",
            "message": exc.message,
            "amount": exc.amount
        }
    )


app.include_router(router)


# Pour lancer :
# uvicorn exercises.exercise_01_solution.main:app --reload