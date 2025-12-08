"""
Concepts : Méthodes PUT et DELETE - Mise à jour et suppression

PUT : Met à jour une ressource existante (remplacement complet)
DELETE : Supprime une ressource
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="API PUT & DELETE Methods",
    description="Démonstration des méthodes PUT et DELETE",
    version="1.0.0"
)

# Base de données simulée en mémoire
products_db = [
    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 10},
    {"id": 2, "name": "Mouse", "price": 25.50, "stock": 50},
    {"id": 3, "name": "Keyboard", "price": 75.00, "stock": 30}
]


class Product(BaseModel):
    """Modèle représentant un produit."""
    name: str
    price: float
    stock: int


@app.get("/products")
def get_all_products():
    """Récupère tous les produits."""
    return products_db


@app.get("/products/{product_id}")
def get_product(product_id: int):
    """Récupère un produit par son ID."""
    for product in products_db:
        if product["id"] == product_id:
            return product
    
    return {"error": "Produit non trouvé"}


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    """
    Met à jour un produit existant (remplacement complet).
    
    Args:
        product_id: L'ID du produit à mettre à jour
        product: Les nouvelles données du produit
        
    Returns:
        Le produit mis à jour ou un message d'erreur
        
    Note:
        PUT remplace TOUTES les données du produit.
        Tous les champs doivent être fournis.
    """
    for i, p in enumerate(products_db):
        if p["id"] == product_id:
            updated_product = {
                "id": product_id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock
            }
            products_db[i] = updated_product
            return updated_product
    
    return {"error": "Produit non trouvé"}


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    """
    Supprime un produit.
    
    Args:
        product_id: L'ID du produit à supprimer
        
    Returns:
        Message de confirmation ou d'erreur
    """
    for i, product in enumerate(products_db):
        if product["id"] == product_id:
            deleted_product = products_db.pop(i)
            return {"message": "Produit supprimé", "product": deleted_product}
    
    return {"error": "Produit non trouvé"}


# Pour lancer ce serveur :
# uvicorn concepts.concepts_03_put_delete_methods:app --reload
#
# Tester dans Swagger :
# 1. GET /products pour voir tous les produits
# 2. PUT /products/1 avec {"name": "Gaming Laptop", "price": 1299.99, "stock": 5}
# 3. GET /products/1 pour voir la modification
# 4. DELETE /products/2 pour supprimer un produit
# 5. GET /products pour vérifier la suppression