"""Exercice 1 - Modèles"""

from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    """Modèle pour créer un compte."""
    owner_name: str = Field(..., min_length=2)
    initial_balance: float = Field(0.0, ge=0)


class TransactionRequest(BaseModel):
    """Modèle pour une transaction."""
    amount: float = Field(..., gt=0)


class AccountResponse(BaseModel):
    """Modèle de réponse pour un compte."""
    id: int
    owner_name: str
    balance: float