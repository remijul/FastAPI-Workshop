"""
Couche Service : Logique métier

Cette couche contient :
- La logique métier de l'application
- Les règles de validation métier
- L'orchestration entre différents repositories

Responsabilité : Implémenter la logique métier
"""

from fastapi import HTTPException, status
from .repositories import ProductRepository
from .models import ProductCreate, ProductResponse


class ProductService:
    """Service pour gérer la logique métier des produits."""
    
    @staticmethod
    def create_product(product_data: ProductCreate) -> ProductResponse:
        """
        Crée un produit avec validation métier.
        
        Logique métier :
        - Vérifier que le produit n'existe pas déjà
        - Créer le produit via le repository
        """
        # Vérifier si le produit existe déjà
        existing = ProductRepository.get_by_name(product_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un produit avec ce nom existe déjà"
            )
        
        # Créer le produit
        product_id = ProductRepository.create(
            name=product_data.name,
            price=product_data.price,
            stock=product_data.stock
        )
        
        return ProductResponse(
            id=product_id,
            name=product_data.name,
            price=product_data.price,
            stock=product_data.stock
        )
    
    @staticmethod
    def get_product(product_id: int) -> ProductResponse:
        """Récupère un produit par ID."""
        product = ProductRepository.get_by_id(product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit non trouvé"
            )
        
        return ProductResponse(**product)
    
    @staticmethod
    def get_all_products() -> list[ProductResponse]:
        """Récupère tous les produits."""
        products = ProductRepository.get_all()
        return [ProductResponse(**p) for p in products]
    
    @staticmethod
    def sell_product(product_id: int, quantity: int) -> ProductResponse:
        """
        Vend un produit (réduit le stock).
        
        Logique métier :
        - Vérifier que le produit existe
        - Vérifier que le stock est suffisant
        - Mettre à jour le stock
        """
        # Récupérer le produit
        product = ProductRepository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit non trouvé"
            )
        
        # Vérifier le stock
        if product["stock"] < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock insuffisant"
            )
        
        # Mettre à jour le stock
        new_stock = product["stock"] - quantity
        ProductRepository.update_stock(product_id, new_stock)
        
        # Retourner le produit mis à jour
        updated_product = ProductRepository.get_by_id(product_id)
        return ProductResponse(**updated_product)