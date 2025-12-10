"""
Solution Exercice 1 - Service
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
    
    # Solution TODO 2: Implémenter les méthodes
    
    @staticmethod
    def create_account(account_data: AccountCreate) -> AccountResponse:
        """Crée un compte bancaire."""
        account_id = AccountRepository.create(
            owner_name=account_data.owner_name,
            balance=account_data.initial_balance
        )
        
        return AccountResponse(
            id=account_id,
            owner_name=account_data.owner_name,
            balance=account_data.initial_balance
        )
    
    @staticmethod
    def get_account(account_id: int) -> AccountResponse:
        """
        Récupère un compte.
        
        Lever AccountNotFoundError si le compte n'existe pas.
        """
        account = AccountRepository.get_by_id(account_id)
        
        if not account:
            raise AccountNotFoundError(account_id)
        
        return AccountResponse(
            id=account["id"],
            owner_name=account["owner_name"],
            balance=account["balance"]
        )
    
    @staticmethod
    def deposit(account_id: int, transaction: TransactionRequest) -> AccountResponse:
        """
        Dépose de l'argent sur un compte.
        
        Lever NegativeAmountError si amount <= 0.
        Lever AccountNotFoundError si compte non trouvé.
        """
        # Vérifier le montant
        if transaction.amount <= 0:
            raise NegativeAmountError(transaction.amount)
        
        # Récupérer le compte
        account = AccountRepository.get_by_id(account_id)
        if not account:
            raise AccountNotFoundError(account_id)
        
        # Calculer le nouveau solde
        new_balance = account["balance"] + transaction.amount
        
        # Mettre à jour
        AccountRepository.update_balance(account_id, new_balance)
        
        return AccountResponse(
            id=account["id"],
            owner_name=account["owner_name"],
            balance=new_balance
        )
    
    @staticmethod
    def withdraw(account_id: int, transaction: TransactionRequest) -> AccountResponse:
        """
        Retire de l'argent d'un compte.
        
        Lever AccountNotFoundError si compte non trouvé.
        Lever InsufficientFundsError si balance < amount.
        """
        # Récupérer le compte
        account = AccountRepository.get_by_id(account_id)
        if not account:
            raise AccountNotFoundError(account_id)
        
        # Vérifier le solde
        if account["balance"] < transaction.amount:
            raise InsufficientFundsError(
                account_id=account_id,
                amount=transaction.amount,
                balance=account["balance"]
            )
        
        # Calculer le nouveau solde
        new_balance = account["balance"] - transaction.amount
        
        # Mettre à jour
        AccountRepository.update_balance(account_id, new_balance)
        
        return AccountResponse(
            id=account["id"],
            owner_name=account["owner_name"],
            balance=new_balance
        )