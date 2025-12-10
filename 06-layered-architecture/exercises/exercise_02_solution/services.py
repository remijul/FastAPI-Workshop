"""
Solution Exercice 2 - Service
"""

from fastapi import HTTPException, status
from .repositories import TaskRepository
from .models import TaskCreate, TaskResponse


class TaskService:
    """Service pour les tâches."""
    
    # Solution TODO 3: Implémenter les méthodes
    
    @staticmethod
    def _get_priority_label(priority: int) -> str:
        """
        Calcule le label de priorité.
        
        Logique métier :
        - 1-2 : "Basse"
        - 3 : "Moyenne"
        - 4-5 : "Haute"
        """
        if priority <= 2:
            return "Basse"
        elif priority == 3:
            return "Moyenne"
        else:
            return "Haute"
    
    @staticmethod
    def create_task(task_data: TaskCreate) -> TaskResponse:
        """
        Crée une tâche avec priority_label.
        
        Args:
            task_data: Données de la tâche à créer
            
        Returns:
            TaskResponse avec priority_label calculé
        """
        # Créer la tâche dans la base
        task_id = TaskRepository.create(
            title=task_data.title,
            priority=task_data.priority,
            completed=task_data.completed
        )
        
        # Calculer priority_label (logique métier)
        priority_label = TaskService._get_priority_label(task_data.priority)
        
        return TaskResponse(
            id=task_id,
            title=task_data.title,
            priority=task_data.priority,
            completed=task_data.completed,
            priority_label=priority_label
        )
    
    @staticmethod
    def get_task(task_id: int) -> TaskResponse:
        """
        Récupère une tâche avec priority_label.
        
        Args:
            task_id: ID de la tâche
            
        Returns:
            TaskResponse avec priority_label calculé
            
        Raises:
            HTTPException: 404 si la tâche n'existe pas
        """
        task = TaskRepository.get_by_id(task_id)
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tâche non trouvée"
            )
        
        # Calculer priority_label
        priority_label = TaskService._get_priority_label(task["priority"])
        
        return TaskResponse(
            id=task["id"],
            title=task["title"],
            priority=task["priority"],
            completed=bool(task["completed"]),
            priority_label=priority_label
        )
    
    @staticmethod
    def get_all_tasks() -> list[TaskResponse]:
        """
        Récupère toutes les tâches avec priority_label.
        
        Returns:
            Liste de TaskResponse avec priority_label calculé
        """
        tasks = TaskRepository.get_all()
        
        return [
            TaskResponse(
                id=task["id"],
                title=task["title"],
                priority=task["priority"],
                completed=bool(task["completed"]),
                priority_label=TaskService._get_priority_label(task["priority"])
            )
            for task in tasks
        ]
    
    @staticmethod
    def complete_task(task_id: int) -> TaskResponse:
        """
        Marque une tâche comme complétée.
        
        Args:
            task_id: ID de la tâche
            
        Returns:
            TaskResponse mise à jour
            
        Raises:
            HTTPException: 404 si la tâche n'existe pas
        """
        # Marquer comme complétée
        success = TaskRepository.mark_completed(task_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tâche non trouvée"
            )
        
        # Récupérer la tâche mise à jour
        task = TaskRepository.get_by_id(task_id)
        priority_label = TaskService._get_priority_label(task["priority"])
        
        return TaskResponse(
            id=task["id"],
            title=task["title"],
            priority=task["priority"],
            completed=bool(task["completed"]),
            priority_label=priority_label
        )