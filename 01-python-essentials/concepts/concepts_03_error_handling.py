"""
Concepts : Gestion des erreurs
"""


class InsufficientStockError(Exception):
    """Exception levée quand le stock est insuffisant."""
    pass


class InvalidPriceError(Exception):
    """Exception levée quand le prix est invalide."""
    pass


def validate_price(price: float) -> None:
    """
    Valide qu'un prix est correct.
    
    Args:
        price: Prix à valider
        
    Raises:
        InvalidPriceError: Si le prix est négatif ou nul
    """
    if price <= 0:
        raise InvalidPriceError(f"Le prix doit être positif, reçu: {price}")


def process_order(product_name: str, quantity: int, stock: int) -> dict:
    """
    Traite une commande avec gestion d'erreurs.
    
    Args:
        product_name: Nom du produit
        quantity: Quantité commandée
        stock: Stock disponible
        
    Returns:
        Dictionnaire avec le résultat de la commande
        
    Raises:
        ValueError: Si les paramètres sont invalides
        InsufficientStockError: Si le stock est insuffisant
    """
    if not product_name:
        raise ValueError("Le nom du produit ne peut pas être vide")
    
    if quantity <= 0:
        raise ValueError("La quantité doit être positive")
    
    if stock < quantity:
        raise InsufficientStockError(
            f"Stock insuffisant: {stock} disponible(s), {quantity} demandé(s)"
        )
    
    return {
        "product": product_name,
        "quantity": quantity,
        "remaining_stock": stock - quantity,
        "status": "success"
    }


def safe_divide(a: float, b: float) -> float:
    """
    Division sécurisée avec gestion de division par zéro.
    
    Args:
        a: Numérateur
        b: Dénominateur
        
    Returns:
        Résultat de la division ou 0.0 si division par zéro
    """
    try:
        return a / b
    except ZeroDivisionError:
        return 0.0