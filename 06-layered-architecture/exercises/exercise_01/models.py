"""
Exercice 1 - Modèles Pydantic

TODO 1: Créer les modèles Pydantic
- NoteCreate : student_name (str, min 2 car), subject (str, min 2 car), grade (float, 0-20)
- NoteResponse : id, student_name, subject, grade, passed (bool)
"""

from pydantic import BaseModel, Field


# TODO 1: Créer les modèles
class NoteCreate(BaseModel):
    pass


class NoteResponse(BaseModel):
    pass