"""
Exercice 2 : API de gestion d'inventaire

Objectif : Créer une API pour gérer un inventaire de produits avec stock

TODO:
1. Créer une application FastAPI
2. Créer un modèle Pydantic ProductCreate avec : name (str), price (float), quantity (int)
3. Implémenter les 6 routes demandées
4. Gérer les cas d'erreur (stock insuffisant, produit non trouvé)
5. Faire passer tous les tests dans tests/test_exercise_02.py

Pour lancer l'API :
    uvicorn exercises.exercise_02:app --reload

Pour tester :
    pytest tests/test_exercise_02.py -v
"""

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

# TODO: Créer l'application FastAPI
app = None

# TODO: Créer la base de données simulée
inventory_db = []
product_id_counter = 1


# TODO: Créer le modèle Pydantic ProductCreate
# Champs : name (str), price (float), quantity (int)
class ProductCreate(BaseModel):
    pass


# TODO: Route GET /inventory - Retourne tous les produits
# Status code: 200


# TODO: Route GET /inventory/{product_id} - Retourne un produit par ID
# Status code: 200 si trouvé, 404 sinon


# TODO: Route POST /inventory - Ajoute un nouveau produit
# Status code: 201
# Paramètre: product (ProductCreate)


# TODO: Route PUT /inventory/{product_id}/restock - Réapprovisionne un produit
# Status code: 200 si trouvé, 404 sinon
# Paramètres: product_id (int), quantity (int) en query parameter
# Ajouter la quantité au stock existant
# Retourner le produit mis à jour


# TODO: Route PUT /inventory/{product_id}/sell - Vend un produit (réduit le stock)
# Status code: 200 si succès, 404 si non trouvé, 400 si stock insuffisant
# Paramètres: product_id (int), quantity (int) en query parameter
# Si stock insuffisant, retourner: {"error": "Stock insuffisant"}
# Sinon, réduire le stock et retourner le produit mis à jour


# TODO: Route DELETE /inventory/{product_id} - Supprime un produit
# Status code: 200 si trouvé, 404 sinon