"""Solution Exercice 1 - Repository"""

from .database import get_db_connection


class AccountRepository:
    """Repository pour les comptes bancaires."""
    
    @staticmethod
    def create(owner_name: str, balance: float) -> int:
        """Crée un compte."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO accounts (owner_name, balance) VALUES (?, ?)",
            (owner_name, balance)
        )
        account_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return account_id
    
    @staticmethod
    def get_by_id(account_id: int) -> dict | None:
        """Récupère un compte par ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        return dict(row) if row else None
    
    @staticmethod
    def update_balance(account_id: int, new_balance: float) -> bool:
        """Met à jour le solde d'un compte."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE accounts SET balance = ? WHERE id = ?",
            (new_balance, account_id)
        )
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success