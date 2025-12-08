"""
Exercice 2 - Repository

TODO 2: Implémenter le TaskRepository
- create(title, priority, completed) -> int
- get_by_id(task_id) -> dict | None
- get_all() -> list[dict]
- mark_completed(task_id) -> bool : UPDATE completed = 1
"""

from .database import get_db_connection


class TaskRepository:
    """Repository pour les tâches."""
    
    # TODO 2: Implémenter les méthodes
    
    @staticmethod
    def create(title: str, priority: int, completed: bool) -> int:
        """Crée une tâche."""
        pass
    
    @staticmethod
    def get_by_id(task_id: int) -> dict | None:
        """Récupère une tâche par ID."""
        pass
    
    @staticmethod
    def get_all() -> list[dict]:
        """Récupère toutes les tâches."""
        pass
    
    @staticmethod
    def mark_completed(task_id: int) -> bool:
        """Marque une tâche comme complétée."""
        pass