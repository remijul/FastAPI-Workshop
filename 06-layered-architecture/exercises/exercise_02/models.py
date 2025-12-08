"""
Exercice 2 - Modèles

TODO 1: Créer les modèles
- TaskCreate : title (str, min 1 car), priority (int, 1-5), completed (bool, default False)
- TaskResponse : id, title, priority, completed, priority_label (str)
"""

from pydantic import BaseModel, Field


# TODO 1: Créer les modèles
class TaskCreate(BaseModel):
    pass


class TaskResponse(BaseModel):
    pass