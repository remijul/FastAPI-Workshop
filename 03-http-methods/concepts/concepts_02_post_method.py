"""
Concepts : Méthode POST - Création de données

La méthode POST est utilisée pour CRÉER de nouvelles ressources.
Elle envoie des données dans le corps de la requête (body).
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="API POST Methods",
    description="Démonstration de la méthode POST",
    version="1.0.0"
)

# Base de données simulée en mémoire
users_db = []
user_id_counter = 1


# Modèle Pydantic pour la validation (simple pour cette étape)
class User(BaseModel):
    """Modèle représentant un utilisateur."""
    name: str
    email: str
    age: int


@app.get("/users")
def get_all_users():
    """
    Récupère tous les utilisateurs.
    
    Returns:
        Liste de tous les utilisateurs
    """
    return users_db


@app.post("/users")
def create_user(user: User):
    """
    Crée un nouvel utilisateur.
    
    Args:
        user: Les données de l'utilisateur à créer
        
    Returns:
        L'utilisateur créé avec son ID
        
    Note:
        Pydantic valide automatiquement que :
        - name est une chaîne de caractères
        - email est une chaîne de caractères
        - age est un entier
    """
    global user_id_counter
    
    # Création de l'utilisateur avec un ID
    new_user = {
        "id": user_id_counter,
        "name": user.name,
        "email": user.email,
        "age": user.age
    }
    
    users_db.append(new_user)
    user_id_counter += 1
    
    return new_user


@app.post("/users/bulk")
def create_multiple_users(users: list[User]):
    """
    Crée plusieurs utilisateurs en une seule requête.
    
    Args:
        users: Liste d'utilisateurs à créer
        
    Returns:
        Liste des utilisateurs créés avec leurs IDs
    """
    global user_id_counter
    
    created_users = []
    for user in users:
        new_user = {
            "id": user_id_counter,
            "name": user.name,
            "email": user.email,
            "age": user.age
        }
        users_db.append(new_user)
        created_users.append(new_user)
        user_id_counter += 1
    
    return created_users


# Pour lancer ce serveur :
# uvicorn concepts.concepts_02_post_method:app --reload
#
# Tester dans Swagger :
# 1. GET /users pour voir la liste (vide au début)
# 2. POST /users avec le corps JSON :
#    {"name": "Alice", "email": "alice@example.com", "age": 25}
# 3. GET /users pour voir l'utilisateur créé
#
# Note : POST nécessite d'utiliser Swagger ou un client comme curl/Postman
# car on ne peut pas envoyer de body directement depuis le navigateur