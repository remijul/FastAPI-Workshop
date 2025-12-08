"""
Concepts : Classes Python
"""


class Product:
    """Représente un produit dans un catalogue."""
    
    def __init__(self, name: str, price: float, stock: int = 0):
        """
        Initialise un produit.
        
        Args:
            name: Nom du produit
            price: Prix unitaire
            stock: Quantité en stock
        """
        self.name = name
        self.price = price
        self.stock = stock
    
    def is_available(self) -> bool:
        """Vérifie si le produit est disponible en stock."""
        return self.stock > 0
    
    def update_stock(self, quantity: int) -> None:
        """
        Met à jour le stock du produit.
        
        Args:
            quantity: Quantité à ajouter (positif) ou retirer (négatif)
        """
        new_stock = self.stock + quantity
        if new_stock < 0:
            raise ValueError("Le stock ne peut pas être négatif")
        self.stock = new_stock
    
    def get_total_value(self) -> float:
        """Calcule la valeur totale du stock."""
        return self.price * self.stock


class Order:
    """Représente une commande client."""
    
    def __init__(self, order_id: str, customer_name: str):
        """
        Initialise une commande.
        
        Args:
            order_id: Identifiant unique de la commande
            customer_name: Nom du client
        """
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = []  # Liste de tuples (Product, quantity)
    
    def add_item(self, product: Product, quantity: int) -> None:
        """
        Ajoute un produit à la commande.
        
        Args:
            product: Produit à ajouter
            quantity: Quantité commandée
        """
        if quantity <= 0:
            raise ValueError("La quantité doit être positive")
        
        if not product.is_available():
            raise ValueError(f"Le produit {product.name} n'est pas disponible")
        
        if product.stock < quantity:
            raise ValueError(f"Stock insuffisant pour {product.name}")
        
        self.items.append((product, quantity))
    
    def calculate_total(self) -> float:
        """Calcule le montant total de la commande."""
        total = 0.0
        for product, quantity in self.items:
            total += product.price * quantity
        return total
    
    def get_item_count(self) -> int:
        """Retourne le nombre d'articles différents dans la commande."""
        return len(self.items)