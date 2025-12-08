"""
Concepts : Fonctions Python
"""


def calculate_total_price(price: float, quantity: int) -> float:
    """
    Calcule le prix total d'un article.
    
    Args:
        price: Prix unitaire
        quantity: Quantité
        
    Returns:
        Prix total
    """
    return price * quantity


def apply_discount(price: float, discount_percent: float) -> float:
    """
    Applique une réduction sur un prix.
    
    Args:
        price: Prix initial
        discount_percent: Pourcentage de réduction (0-100)
        
    Returns:
        Prix après réduction
    """
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("La réduction doit être comprise entre 0 et 100")
    
    discount_amount = price * (discount_percent / 100)
    return price - discount_amount


def format_product_name(name: str) -> str:
    """
    Formate le nom d'un produit (majuscule première lettre, trim).
    
    Args:
        name: Nom du produit
        
    Returns:
        Nom formaté
    """
    return name.strip().capitalize()