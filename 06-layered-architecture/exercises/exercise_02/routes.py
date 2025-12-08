"""
Exercice 2 - Routes

TODO 4: Implémenter les routes
- POST /tasks
- GET /tasks
- GET /tasks/{task_id}
- PUT /tasks/{task_id}/complete
"""

from fastapi import APIRouter
from .models import TaskCreate, TaskResponse
from .services import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


# TODO 4: Implémenter les routes