"""
Solution Exercice 2 - Modèles
"""

from pydantic import BaseModel, Field


# Solution TODO 1: Créer les modèles

class TaskCreate(BaseModel):
    """Modèle pour créer une tâche."""
    title: str = Field(..., min_length=1)
    priority: int = Field(..., ge=1, le=5)
    completed: bool = False


class TaskResponse(BaseModel):
    """Modèle de réponse pour une tâche."""
    id: int
    title: str
    priority: int
    completed: bool
    priority_label: str