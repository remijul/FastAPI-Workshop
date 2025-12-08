"""
Exercice 2 - Service

TODO 3: Implémenter le TaskService
- create_task(task_data) -> TaskResponse : avec priority_label calculé
- get_task(task_id) -> TaskResponse : avec priority_label
- get_all_tasks() -> list[TaskResponse] : avec priority_label
- complete_task(task_id) -> TaskResponse : marque completed=True

Logique métier priority_label :
- 1-2 : "Basse"
- 3 : "Moyenne"
- 4-5 : "Haute"
"""

from fastapi import HTTPException, status
from .repositories import TaskRepository
from .models import TaskCreate, TaskResponse


class TaskService:
    """Service pour les tâches."""
    
    # TODO 3: Implémenter les méthodes
    
    @staticmethod
    def _get_priority_label(priority: int) -> str:
        """Calcule le label de priorité."""
        if priority <= 2:
            return "Basse"
        elif priority == 3:
            return "Moyenne"
        else:
            return "Haute"
    
    @staticmethod
    def create_task(task_data: TaskCreate) -> TaskResponse:
        """Crée une tâche avec priority_label."""
        pass
    
    @staticmethod
    def get_task(task_id: int) -> TaskResponse:
        """Récupère une tâche avec priority_label."""
        pass
    
    @staticmethod
    def get_all_tasks() -> list[TaskResponse]:
        """Récupère toutes les tâches avec priority_label."""
        pass
    
    @staticmethod
    def complete_task(task_id: int) -> TaskResponse:
        """Marque une tâche comme complétée."""
        pass