"""
Concepts : Exceptions personnalisées

Créer ses propres exceptions permet de :
- Rendre le code plus lisible
- Centraliser la gestion des erreurs
- Réutiliser la logique d'erreur
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="API Exceptions Personnalisées",
    description="Démonstration des exceptions personnalisées",
    version="1.0.0"
)


# Définir des exceptions personnalisées
class ProductNotFoundError(Exception):
    """Exception levée quand un produit n'existe pas."""
    def __init__(self, product_id: int):
        self.product_id = product_id
        self.message = f"Produit {product_id} non trouvé"
        super().__init__(self.message)


class InsufficientStockError(Exception):
    """Exception levée quand le stock est insuffisant."""
    def __init__(self, product_name: str, requested: int, available: int):
        self.product_name = product_name
        self.requested = requested
        self.available = available
        self.message = f"Stock insuffisant pour {product_name}: demandé={requested}, disponible={available}"
        super().__init__(self.message)


# Gestionnaires d'exceptions personnalisées
@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(request: Request, exc: ProductNotFoundError):
    """Gère les erreurs ProductNotFoundError."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Product Not Found",
            "message": exc.message,
            "product_id": exc.product_id
        }
    )


@app.exception_handler(InsufficientStockError)
async def insufficient_stock_handler(request: Request, exc: InsufficientStockError):
    """Gère les erreurs InsufficientStockError."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Insufficient Stock",
            "message": exc.message,
            "product": exc.product_name,
            "requested": exc.requested,
            "available": exc.available
        }
    )


# Base de données simulée
products_db = {
    1: {"id": 1, "name": "Laptop", "stock": 5},
    2: {"id": 2, "name": "Mouse", "stock": 10}
}


class SellRequest(BaseModel):
    quantity: int = Field(..., gt=0)


@app.get("/products/{product_id}")
def get_product(product_id: int):
    """Récupère un produit."""
    product = products_db.get(product_id)
    
    if not product:
        # Lever l'exception personnalisée
        raise ProductNotFoundError(product_id)
    
    return product


@app.post("/products/{product_id}/sell")
def sell_product(product_id: int, sell_request: SellRequest):
    """Vend un produit."""
    product = products_db.get(product_id)
    
    if not product:
        raise ProductNotFoundError(product_id)
    
    # Vérifier le stock
    if product["stock"] < sell_request.quantity:
        raise InsufficientStockError(
            product_name=product["name"],
            requested=sell_request.quantity,
            available=product["stock"]
        )
    
    # Mettre à jour le stock
    product["stock"] -= sell_request.quantity
    
    return {
        "message": "Vente réussie",
        "product": product["name"],
        "quantity_sold": sell_request.quantity,
        "remaining_stock": product["stock"]
    }


# Pour lancer :
# uvicorn concepts.concepts_02_custom_exceptions:app --reload
#
# Avantages des exceptions personnalisées :
# 1. Code plus lisible : raise ProductNotFoundError(id)
# 2. Réutilisable partout dans l'application
# 3. Gestion centralisée des erreurs
# 4. Réponses d'erreur cohérentes