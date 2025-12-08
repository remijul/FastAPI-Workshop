"""
Couche Repository : Accès aux données

Cette couche contient :
- Toutes les requêtes SQL
- Les opérations CRUD sur la base de données
- Aucune logique métier (juste l'accès aux données)

Responsabilité : Communiquer avec la base de données
"""

from .database import get_db_connection


class ProductRepository:
    """Repository pour gérer l'accès aux données des produits."""
    
    @staticmethod
    def create(name: str, price: float, stock: int) -> int:
        """
        Crée un produit dans la base de données.
        
        Args:
            name: Nom du produit
            price: Prix du produit
            stock: Stock du produit
            
        Returns:
            ID du produit créé
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
            (name, price, stock)
        )
        product_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return product_id
    
    @staticmethod
    def get_by_id(product_id: int) -> dict | None:
        """
        Récupère un produit par son ID.
        
        Args:
            product_id: ID du produit
            
        Returns:
            Dictionnaire avec les données du produit ou None
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        return dict(row) if row else None
    
    @staticmethod
    def get_by_name(name: str) -> dict | None:
        """Récupère un produit par son nom."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM products WHERE name = ?", (name,))
        row = cursor.fetchone()
        
        conn.close()
        
        return dict(row) if row else None
    
    @staticmethod
    def get_all() -> list[dict]:
        """Récupère tous les produits."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        
        conn.close()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def update_stock(product_id: int, new_stock: int) -> bool:
        """
        Met à jour le stock d'un produit.
        
        Returns:
            True si la mise à jour a réussi, False sinon
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE products SET stock = ? WHERE id = ?",
            (new_stock, product_id)
        )
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    @staticmethod
    def delete(product_id: int) -> bool:
        """
        Supprime un produit.
        
        Returns:
            True si la suppression a réussi, False sinon
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success