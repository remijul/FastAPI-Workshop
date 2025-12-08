"""
Concepts : Codes de statut HTTP

Les codes HTTP indiquent le résultat d'une requête :
- 200 : Succès (OK)
- 201 : Créé (Created)
- 204 : Pas de contenu (No Content)
- 404 : Non trouvé (Not Found)
- 400 : Mauvaise requête (Bad Request)
"""

from fastapi import FastAPI, status, Response

app = FastAPI(
    title="API Status Codes",
    description="Démonstration des codes de statut HTTP",
    version="1.0.0"
)

# Base de données simulée
items_db = {}
item_id_counter = 1


@app.get("/items", status_code=status.HTTP_200_OK)
def get_items():
    """
    Récupère tous les items.
    
    Status: 200 OK (par défaut pour GET)
    """
    return list(items_db.values())


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(name: str, price: float):
    """
    Crée un nouvel item.
    
    Status: 201 Created (indique qu'une ressource a été créée)
    """
    global item_id_counter
    
    new_item = {
        "id": item_id_counter,
        "name": name,
        "price": price
    }
    items_db[item_id_counter] = new_item
    item_id_counter += 1
    
    return new_item


@app.get("/items/{item_id}")
def get_item(item_id: int, response: Response):
    """
    Récupère un item par son ID.
    
    Status: 200 OK si trouvé, 404 Not Found sinon
    """
    if item_id in items_db:
        return items_db[item_id]
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Item non trouvé"}


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, response: Response):
    """
    Supprime un item.
    
    Status: 204 No Content si succès, 404 Not Found sinon
    
    Note: 204 signifie "succès mais pas de contenu à retourner"
    """
    if item_id in items_db:
        del items_db[item_id]
        return None  # Pas de contenu avec 204
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Item non trouvé"}


# Pour lancer ce serveur :
# uvicorn concepts.concepts_04_status_codes:app --reload
#
# Tester dans Swagger et observer les codes de statut :
# - POST /items : Code 201
# - GET /items : Code 200
# - GET /items/999 (non existant) : Code 404
# - DELETE /items/1 : Code 204
#
# Les codes de statut sont visibles dans :
# - La console du navigateur (onglet Réseau)
# - La réponse Swagger (en haut de la réponse)