"""Solution Exercice 1 - Routes"""

from fastapi import APIRouter
from .models import AccountCreate, TransactionRequest, AccountResponse
from .services import AccountService

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=AccountResponse, status_code=201)
def create_account(account: AccountCreate):
    """Crée un compte."""
    return AccountService.create_account(account)


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: int):
    """Récupère un compte."""
    return AccountService.get_account(account_id)


@router.post("/{account_id}/deposit", response_model=AccountResponse)
def deposit(account_id: int, transaction: TransactionRequest):
    """Dépose de l'argent."""
    return AccountService.deposit(account_id, transaction)


@router.post("/{account_id}/withdraw", response_model=AccountResponse)
def withdraw(account_id: int, transaction: TransactionRequest):
    """Retire de l'argent."""
    return AccountService.withdraw(account_id, transaction)