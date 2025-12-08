"""
Concepts : Modèles de réponse

Les response_model permettent de :
- Filtrer les données retournées (ex: masquer les mots de passe)
- Documenter clairement ce que retourne l'API
- Valider automatiquement les réponses
"""

from fastapi import FastAPI, Response, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

app = FastAPI(
    title="API Modèles de réponse",
    description="Démonstration des response_model",
    version="1.0.0"
)


# Modèle d'entrée (ce que le client envoie)
class UserCreate(BaseModel):
    """Données pour créer un utilisateur."""
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=8)
    age: int = Field(..., ge=0)


# Modèle de sortie (ce que l'API retourne)
class UserResponse(BaseModel):
    """Données publiques d'un utilisateur (sans mot de passe)."""
    id: int
    username: str
    email: EmailStr
    age: int


# Modèle complet en base de données
class UserInDB(BaseModel):
    """Représentation complète en base (avec mot de passe)."""
    id: int
    username: str
    email: EmailStr
    password: str  # Stocké (hashé dans une vraie app)
    age: int


users_db = []
user_id_counter = 1


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """
    Crée un utilisateur.
    
    Le client envoie : username, email, password, age
    L'API retourne : id, username, email, age (PAS le password !)
    
    Le response_model=UserResponse filtre automatiquement le password.
    """
    global user_id_counter
    
    # Créer l'utilisateur complet en base
    user_in_db = UserInDB(
        id=user_id_counter,
        username=user.username,
        email=user.email,
        password=user.password,  # Dans une vraie app : hasher le mot de passe
        age=user.age
    )
    
    users_db.append(user_in_db.model_dump())
    user_id_counter += 1
    
    # Retourner sans le password (automatique grâce à response_model)
    return user_in_db


@app.get("/users", response_model=list[UserResponse])
def get_all_users():
    """
    Retourne tous les utilisateurs (sans mots de passe).
    
    Le response_model filtre automatiquement les passwords.
    """
    return users_db


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, response: Response):
    """
    Retourne un utilisateur par ID (sans mot de passe).
    """
    for user in users_db:
        if user["id"] == user_id:
            return user
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Utilisateur non trouvé"}


# Modèle avec champs calculés
class ProductBase(BaseModel):
    """Données de base d'un produit."""
    name: str
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class ProductResponse(ProductBase):
    """Réponse avec champs calculés."""
    id: int
    total_value: float  # Champ calculé : price * stock
    in_stock: bool  # Champ calculé : stock > 0


products_db = []
product_id_counter = 1


@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductBase):
    """
    Crée un produit.
    
    Le response_model ajoute automatiquement des champs calculés.
    """
    global product_id_counter
    
    product_dict = product.model_dump()
    product_dict["id"] = product_id_counter
    product_dict["total_value"] = product.price * product.stock
    product_dict["in_stock"] = product.stock > 0
    
    products_db.append(product_dict)
    product_id_counter += 1
    
    return product_dict


# Pour lancer ce serveur :
# uvicorn concepts.concepts_04_response_models:app --reload
#
# Les response_model sont utiles pour :
# 1. Sécurité : masquer les données sensibles (password)
# 2. Documentation : indiquer clairement ce qui est retourné
# 3. Validation : s'assurer que la réponse est conforme
# 4. Transformation : ajouter des champs calculés