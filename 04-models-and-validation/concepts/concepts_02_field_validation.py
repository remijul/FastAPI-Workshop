"""
Concepts : Validation des champs avec Pydantic

Pydantic permet d'ajouter des contraintes sur les champs :
- Valeurs min/max
- Longueur de chaînes
- Expressions régulières
- Validation d'email
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional

app = FastAPI(
    title="API Validation des champs",
    description="Démonstration de la validation Pydantic",
    version="1.0.0"
)


class User(BaseModel):
    """Modèle utilisateur avec validation."""
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr  # Valide automatiquement le format email
    age: int = Field(..., ge=0, le=120)  # ge = greater or equal, le = less or equal
    bio: Optional[str] = Field(None, max_length=500)


class Product(BaseModel):
    """Modèle produit avec validation."""
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)  # gt = greater than (strictement positif)
    stock: int = Field(0, ge=0)  # Stock ne peut pas être négatif
    discount: float = Field(0.0, ge=0.0, le=100.0)  # Entre 0 et 100%
    
    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        """Validation personnalisée : le nom ne peut pas être vide après trim."""
        if not v.strip():
            raise ValueError('Le nom ne peut pas être vide')
        return v.strip()


class Article(BaseModel):
    """Modèle article avec validation."""
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=10)
    tags: list[str] = Field(default_factory=list)
    published: bool = False
    
    @field_validator('tags')
    @classmethod
    def tags_must_be_lowercase(cls, v: list[str]) -> list[str]:
        """Validation personnalisée : les tags doivent être en minuscules."""
        return [tag.lower() for tag in v]


users_db = []
products_db = []


@app.post("/users")
def create_user(user: User):
    """
    Crée un utilisateur avec validation stricte.
    
    Validations automatiques :
    - username : 3 à 20 caractères
    - email : format email valide
    - age : entre 0 et 120
    - bio : maximum 500 caractères (optionnel)
    """
    user_dict = user.model_dump()
    users_db.append(user_dict)
    return user_dict


@app.post("/products")
def create_product(product: Product):
    """
    Crée un produit avec validation stricte.
    
    Validations automatiques :
    - name : 1 à 100 caractères, non vide après trim
    - price : strictement positif
    - stock : >= 0
    - discount : entre 0 et 100
    """
    product_dict = product.model_dump()
    products_db.append(product_dict)
    return product_dict


@app.post("/articles")
def create_article(article: Article):
    """
    Crée un article avec validation.
    
    Validations :
    - title : 5 à 200 caractères
    - content : minimum 10 caractères
    - tags : automatiquement convertis en minuscules
    """
    article_dict = article.model_dump()
    return article_dict


# Pour lancer ce serveur :
# uvicorn concepts.concepts_02_field_validation:app --reload
#
# Tester dans Swagger - Essayez ces cas d'erreur :
# 1. User avec username de 2 caractères → Erreur
# 2. User avec email invalide "test" → Erreur
# 3. User avec age = 150 → Erreur
# 4. Product avec price = 0 → Erreur
# 5. Product avec discount = 150 → Erreur
# 6. Article avec title de 3 caractères → Erreur