"""
Solution Exercice 2 - Routes
"""

from fastapi import APIRouter
from .models import TaskCreate, TaskResponse
from .services import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


# Solution TODO 4: Implémenter les routes

@router.post("", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    """Crée une nouvelle tâche."""
    return TaskService.create_task(task)


@router.get("", response_model=list[TaskResponse])
def get_all_tasks():
    """Liste toutes les tâches."""
    return TaskService.get_all_tasks()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """Récupère une tâche par ID."""
    return TaskService.get_task(task_id)


@router.put("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int):
    """Marque une tâche comme complétée."""
    return TaskService.complete_task(task_id)