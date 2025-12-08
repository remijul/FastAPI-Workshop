"""
Solution de l'exercice 1 : Gestion d'un panier d'achat
"""


class Cart:
    """Représente un panier d'achat."""
    
    def __init__(self):
        """Initialise un panier vide."""
        self.items = []
    
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
        # Validation du prix
        if price < 0:
            raise ValueError("Le prix ne peut pas être négatif")
        
        # Validation de la quantité
        if quantity <= 0:
            raise ValueError("La quantité doit être positive")
        
        # Ajout du produit au panier
        product = {
            "name": product_name,
            "price": price,
            "quantity": quantity
        }
        self.items.append(product)
    
    def get_total(self) -> float:
        """
        Calcule le montant total du panier.
        
        Returns:
            Montant total
        """
        total = 0.0
        for item in self.items:
            total += item["price"] * item["quantity"]
        return total
    
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
        # Validation du pourcentage
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Le pourcentage doit être entre 0 et 100")
        
        # Calcul du total avec réduction
        total = self.get_total()
        discount_amount = total * (discount_percent / 100)
        return total - discount_amount
    
    def is_empty(self) -> bool:
        """
        Vérifie si le panier est vide.
        
        Returns:
            True si le panier est vide, False sinon
        """
        return len(self.items) == 0