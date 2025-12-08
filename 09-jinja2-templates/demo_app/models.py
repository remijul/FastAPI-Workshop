"""Modèles Pydantic pour l'application de démonstration."""

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    """Modèle pour l'inscription."""
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class TaskCreate(BaseModel):
    """Modèle pour créer une tâche."""
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class TaskResponse(BaseModel):
    """Modèle de réponse pour une tâche."""
    id: int
    title: str
    description: str
    completed: bool
    owner: str