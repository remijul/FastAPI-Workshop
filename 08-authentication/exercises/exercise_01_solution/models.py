"""Solution Exercice 1 - Modèles"""

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    """Modèle pour l'inscription."""
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Modèle pour la connexion."""
    username: str
    password: str


class Token(BaseModel):
    """Modèle pour le token JWT."""
    access_token: str
    token_type: str


class ArticleCreate(BaseModel):
    """Modèle pour créer un article."""
    title: str = Field(..., min_length=5)
    content: str = Field(..., min_length=10)


class ArticleResponse(BaseModel):
    """Modèle de réponse pour un article."""
    id: int
    title: str
    content: str
    author: str