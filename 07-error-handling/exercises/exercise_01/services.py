"""
Exercice 1 - Service

TODO 2: Implémenter les méthodes avec gestion d'erreurs
- create_account : Créer un compte
- get_account : Récupérer un compte (lever AccountNotFoundError si non trouvé)
- deposit : Ajouter de l'argent (lever NegativeAmountError si montant <= 0)
- withdraw : Retirer de l'argent (lever InsufficientFundsError si solde insuffisant)
"""

from .repositories import AccountRepository
from .models import AccountCreate, TransactionRequest, AccountResponse
from .exceptions import (
    AccountNotFoundError,
    InsufficientFundsError,
    NegativeAmountError
)


class AccountService:
    """Service pour gérer les comptes bancaires."""
    
    # TODO 2: Implémenter les méthodes
    
    @staticmethod
    def create_account(account_data: AccountCreate) -> AccountResponse:
        """Crée un compte bancaire."""
        pass
    
    @staticmethod
    def get_account(account_id: int) -> AccountResponse:
        """
        Récupère un compte.
        
        Lever AccountNotFoundError si le compte n'existe pas.
        """
        pass
    
    @staticmethod
    def deposit(account_id: int, transaction: TransactionRequest) -> AccountResponse:
        """
        Dépose de l'argent sur un compte.
        
        Lever NegativeAmountError si amount <= 0.
        Lever AccountNotFoundError si compte non trouvé.
        """
        pass
    
    @staticmethod
    def withdraw(account_id: int, transaction: TransactionRequest) -> AccountResponse:
        """
        Retire de l'argent d'un compte.
        
        Lever AccountNotFoundError si compte non trouvé.
        Lever InsufficientFundsError si balance < amount.
        """
        pass