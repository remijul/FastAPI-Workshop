"""
Solution de l'exercice 2 : API de gestion d'inventaire
"""

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

# Création de l'application FastAPI
app = FastAPI(
    title="API Gestion d'Inventaire",
    description="API pour gérer un inventaire de produits avec stock",
    version="1.0.0"
)

# Base de données simulée en mémoire
inventory_db = []
product_id_counter = 1


# Modèle Pydantic ProductCreate
class ProductCreate(BaseModel):
    """Modèle représentant un produit à créer."""
    name: str
    price: float
    quantity: int


@app.get("/inventory", status_code=status.HTTP_200_OK)
def get_all_products():
    """
    Récupère tous les produits de l'inventaire.
    
    Returns:
        Liste de tous les produits
    """
    return inventory_db


@app.get("/inventory/{product_id}")
def get_product_by_id(product_id: int, response: Response):
    """
    Récupère un produit par son ID.
    
    Args:
        product_id: L'identifiant du produit
        response: Objet Response pour modifier le status code
        
    Returns:
        Le produit trouvé ou un message d'erreur
    """
    for product in inventory_db:
        if product["id"] == product_id:
            response.status_code = status.HTTP_200_OK
            return product
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Produit non trouvé"}


@app.post("/inventory", status_code=status.HTTP_201_CREATED)
def add_product(product: ProductCreate):
    """
    Ajoute un nouveau produit à l'inventaire.
    
    Args:
        product: Les données du produit à ajouter
        
    Returns:
        Le produit créé avec son ID
    """
    global product_id_counter
    
    new_product = {
        "id": product_id_counter,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }
    
    inventory_db.append(new_product)
    product_id_counter += 1
    
    return new_product


@app.put("/inventory/{product_id}/restock")
def restock_product(product_id: int, quantity: int, response: Response):
    """
    Réapprovisionne un produit (ajoute au stock existant).
    
    Args:
        product_id: L'ID du produit à réapprovisionner
        quantity: Quantité à ajouter au stock
        response: Objet Response pour modifier le status code
        
    Returns:
        Le produit mis à jour ou un message d'erreur
    """
    for i, product in enumerate(inventory_db):
        if product["id"] == product_id:
            inventory_db[i]["quantity"] += quantity
            response.status_code = status.HTTP_200_OK
            return inventory_db[i]
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Produit non trouvé"}


@app.put("/inventory/{product_id}/sell")
def sell_product(product_id: int, quantity: int, response: Response):
    """
    Vend un produit (réduit le stock).
    
    Args:
        product_id: L'ID du produit à vendre
        quantity: Quantité à vendre
        response: Objet Response pour modifier le status code
        
    Returns:
        Le produit mis à jour, ou un message d'erreur
    """
    for i, product in enumerate(inventory_db):
        if product["id"] == product_id:
            # Vérifier le stock suffisant
            if product["quantity"] < quantity:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"error": "Stock insuffisant"}
            
            # Réduire le stock
            inventory_db[i]["quantity"] -= quantity
            response.status_code = status.HTTP_200_OK
            return inventory_db[i]
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Produit non trouvé"}


@app.delete("/inventory/{product_id}")
def delete_product(product_id: int, response: Response):
    """
    Supprime un produit de l'inventaire.
    
    Args:
        product_id: L'ID du produit à supprimer
        response: Objet Response pour modifier le status code
        
    Returns:
        Message de confirmation ou d'erreur
    """
    for i, product in enumerate(inventory_db):
        if product["id"] == product_id:
            inventory_db.pop(i)
            response.status_code = status.HTTP_200_OK
            return {"message": "Produit supprimé"}
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Produit non trouvé"}


# Pour lancer ce serveur :
# uvicorn exercises.exercise_02_solution:app --reload
#
# Tester dans Swagger :
# 1. POST /inventory pour ajouter un produit
# 2. GET /inventory pour voir tous les produits
# 3. PUT /inventory/{id}/restock?quantity=10 pour réapprovisionner
# 4. PUT /inventory/{id}/sell?quantity=5 pour vendre
# 5. DELETE /inventory/{id} pour supprimer un produit
#
# Scénario de test complet :
# 1. Créer un produit avec quantity=10
# 2. Vendre 3 unités → quantity=7
# 3. Réapprovisionner 5 unités → quantity=12
# 4. Essayer de vendre 20 unités → Erreur "Stock insuffisant"