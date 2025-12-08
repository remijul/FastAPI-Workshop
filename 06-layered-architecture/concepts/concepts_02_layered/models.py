"""
Couche Modèles : Définition des structures de données

Cette couche contient :
- Les modèles Pydantic pour la validation
- Les modèles de requête (Create, Update)
- Les modèles de réponse (Response)
"""

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    """Modèle pour créer un produit."""
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class ProductUpdate(BaseModel):
    """Modèle pour mettre à jour un produit."""
    name: str | None = None
    price: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)


class ProductResponse(BaseModel):
    """Modèle de réponse pour un produit."""
    id: int
    name: str
    price: float
    stock: int