"""
Solution Exercice 1 - Modèles Pydantic
"""

from pydantic import BaseModel, Field


# Solution TODO 1: Créer les modèles

class NoteCreate(BaseModel):
    """Modèle pour créer une note."""
    student_name: str = Field(..., min_length=2)
    subject: str = Field(..., min_length=2)
    grade: float = Field(..., ge=0, le=20)


class NoteResponse(BaseModel):
    """Modèle de réponse pour une note."""
    id: int
    student_name: str
    subject: str
    grade: float
    passed: bool