"""
Concepts : Paramètres de chemin (path parameters)

NOTE IMPORTANTE - Section "Schemas" dans Swagger :
Vous verrez apparaître une section "Schemas" en bas de la documentation Swagger
avec HTTPValidationError et ValidationError.

Pourquoi ?
Dès qu'une route a des paramètres typés (comme user_id: int), FastAPI génère
automatiquement des schémas de validation. Ces schémas documentent les erreurs
possibles si la validation échoue.

Exemple pratique :
- http://127.0.0.1:8000/users/123 → ✅ Fonctionne (123 est un entier)
- http://127.0.0.1:8000/users/abc → ❌ Erreur 422 (abc n'est pas un entier)

L'erreur 422 retournera un objet conforme au schéma HTTPValidationError
qui explique pourquoi la validation a échoué.

C'est une fonctionnalité AUTOMATIQUE et UTILE de FastAPI !
"""

from fastapi import FastAPI

app = FastAPI(
    title="API avec paramètres de chemin",
    description="Démonstration des path parameters",
    version="1.0.0"
)


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Récupère un utilisateur par son ID.
    
    Args:
        user_id: L'identifiant de l'utilisateur (doit être un entier)
        
    Returns:
        Les informations de l'utilisateur
        
    Note:
        Si user_id n'est pas un entier, FastAPI retourne automatiquement
        une erreur 422 avec les détails de validation.
    """
    return {
        "user_id": user_id,
        "username": f"user_{user_id}",
        "email": f"user{user_id}@example.com"
    }


@app.get("/products/{product_id}")
def get_product(product_id: int):
    """
    Récupère un produit par son ID.
    
    Args:
        product_id: L'identifiant du produit (doit être un entier)
        
    Returns:
        Les informations du produit
    """
    return {
        "product_id": product_id,
        "name": f"Product {product_id}",
        "price": product_id * 10.0
    }


@app.get("/items/{item_name}")
def get_item_by_name(item_name: str):
    """
    Récupère un article par son nom.
    
    Args:
        item_name: Le nom de l'article (string - accepte n'importe quel texte)
        
    Returns:
        Les informations de l'article
        
    Note:
        Comme item_name est un string, FastAPI accepte n'importe quelle valeur.
        Les strings ont moins de contraintes de validation que les int ou float.
    """
    return {
        "item_name": item_name,
        "description": f"Ceci est {item_name}"
    }


# Pour lancer ce serveur :
# uvicorn concepts.concepts_02_path_parameters:app --reload
#
# Puis ouvrir dans le navigateur :
# - http://127.0.0.1:8000/users/123 pour tester
# - http://127.0.0.1:8000/docs pour Swagger UI
# - http://127.0.0.1:8000/redoc pour ReDoc
#
# EXERCICE : Dans Swagger, essayez de passer "abc" au lieu d'un nombre
# pour user_id et observez l'erreur de validation !