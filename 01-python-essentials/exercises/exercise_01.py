"""
Exercice 1 : Gestion d'un panier d'achat

Objectif : Créer une classe Cart (panier) qui permet d'ajouter des produits,
calculer le total et appliquer des réductions.

TODO:
1. Implémenter la classe Cart avec les méthodes demandées
2. Utiliser la gestion d'erreurs appropriée
3. Faire passer tous les tests dans tests/test_exercise_01.py
"""


class Cart:
    """Représente un panier d'achat."""
    
    def __init__(self):
        """Initialise un panier vide."""
        # TODO: Initialiser la liste des articles
        pass
    
    def add_product(self, product_name: str, price: float, quantity: int = 1) -> None:
        """
        Ajoute un produit au panier.
        
        Args:
            product_name: Nom du produit
            price: Prix unitaire
            quantity: Quantité (par défaut 1)
            
        Raises:
            ValueError: Si le prix est négatif ou la quantité <= 0
        """
        # TODO: Valider les paramètres d'entrée (arguments)
        # TODO: Ajouter le produit sous forme de dictionnaire
        # Format suggéré: {"name": ..., "price": ..., "quantity": ...}
        pass
    
    def get_total(self) -> float:
        """
        Calcule le montant total du panier.
        
        Returns:
            Montant total
        """
        # TODO: Calculer la somme de tous les produits
        pass
    
    def apply_coupon(self, discount_percent: float) -> float:
        """
        Applique un coupon de réduction sur le total.
        
        Args:
            discount_percent: Pourcentage de réduction (0-100)
            
        Returns:
            Nouveau total après réduction
            
        Raises:
            ValueError: Si le pourcentage n'est pas entre 0 et 100
        """
        # TODO: Valider le pourcentage
        # TODO: Calculer et retourner le nouveau total
        pass
    
    def is_empty(self) -> bool:
        """
        Vérifie si le panier est vide.
        
        Returns:
            True si le panier est vide, False sinon
        """
        # TODO: Retourner True si aucun article dans le panier
        pass