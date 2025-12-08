"""
Solution Exercice 1 - Exceptions personnalisées
"""


# Solution TODO 1: Créer les exceptions personnalisées

class AccountNotFoundError(Exception):
    """Exception levée quand un compte n'existe pas."""
    def __init__(self, account_id: int):
        self.account_id = account_id
        self.message = f"Compte {account_id} non trouvé"
        super().__init__(self.message)


class InsufficientFundsError(Exception):
    """Exception levée quand le solde est insuffisant."""
    def __init__(self, account_id: int, amount: float, balance: float):
        self.account_id = account_id
        self.amount = amount
        self.balance = balance
        self.message = f"Solde insuffisant pour le compte {account_id}: demandé={amount}, disponible={balance}"
        super().__init__(self.message)


class NegativeAmountError(Exception):
    """Exception levée quand le montant est négatif ou zéro."""
    def __init__(self, amount: float):
        self.amount = amount
        self.message = f"Le montant doit être positif: {amount}"
        super().__init__(self.message)