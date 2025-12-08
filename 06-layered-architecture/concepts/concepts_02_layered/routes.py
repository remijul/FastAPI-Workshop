"""
Couche Routes : Points d'entrée de l'API

Cette couche contient :
- Les définitions des routes FastAPI
- La validation des entrées (via Pydantic)
- Les appels aux services
- Aucune logique métier (délégué aux services)

Responsabilité : Exposer l'API HTTP
"""

from fastapi import APIRouter
from .models import ProductCreate, ProductResponse
from .services import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate):
    """
    Crée un nouveau produit.
    
    La route ne fait que :
    1. Recevoir les données
    2. Appeler le service
    3. Retourner la réponse
    """
    return ProductService.create_product(product)


@router.get("", response_model=list[ProductResponse])
def get_all_products():
    """Liste tous les produits."""
    return ProductService.get_all_products()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    """Récupère un produit par ID."""
    return ProductService.get_product(product_id)


@router.put("/{product_id}/sell", response_model=ProductResponse)
def sell_product(product_id: int, quantity: int):
    """
    Vend un produit (réduit le stock).
    
    La logique métier (vérification stock, etc.) est dans le service.
    """
    return ProductService.sell_product(product_id, quantity)