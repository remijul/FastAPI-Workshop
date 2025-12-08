"""Solution Exercice 2 - Modèles"""

from pydantic import BaseModel, Field
from enum import Enum


class UserRole(str, Enum):
    """Rôles utilisateur."""
    USER = "user"
    ADMIN = "admin"


class UserRegister(BaseModel):
    """Modèle pour l'inscription."""
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.USER


class UserLogin(BaseModel):
    """Modèle pour la connexion."""
    username: str
    password: str


class Token(BaseModel):
    """Modèle pour le token JWT."""
    access_token: str
    token_type: str


class TaskCreate(BaseModel):
    """Modèle pour créer une tâche."""
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class TaskResponse(BaseModel):
    """Modèle de réponse pour une tâche."""
    id: int
    title: str
    description: str
    owner: str
    completed: bool