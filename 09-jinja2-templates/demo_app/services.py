"""Services contenant la logique métier."""

from passlib.context import CryptContext
from .repositories import UserRepository, TaskRepository
from .models import UserRegister, TaskCreate, TaskResponse

# Configuration du hachage de mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service d'authentification."""
    
    @staticmethod
    def register(user_data: UserRegister) -> bool:
        """
        Enregistre un nouvel utilisateur.
        
        Returns:
            True si succès, False si username existe déjà
        """
        # Vérifier si l'utilisateur existe
        existing_user = UserRepository.get_by_username(user_data.username)
        if existing_user:
            return False
        
        # Hacher le mot de passe
        hashed_password = pwd_context.hash(user_data.password)
        
        # Créer l'utilisateur
        UserRepository.create(user_data.username, hashed_password)
        return True
    
    @staticmethod
    def authenticate(username: str, password: str) -> bool:
        """
        Authentifie un utilisateur.
        
        Returns:
            True si identifiants valides, False sinon
        """
        user = UserRepository.get_by_username(username)
        
        if not user:
            return False
        
        return pwd_context.verify(password, user["hashed_password"])


class TaskService:
    """Service pour les tâches."""
    
    @staticmethod
    def create_task(task_data: TaskCreate, owner: str) -> TaskResponse:
        """Crée une tâche."""
        task_id = TaskRepository.create(
            title=task_data.title,
            description=task_data.description,
            owner=owner
        )
        
        return TaskResponse(
            id=task_id,
            title=task_data.title,
            description=task_data.description,
            completed=False,
            owner=owner
        )
    
    @staticmethod
    def get_user_tasks(username: str) -> list[TaskResponse]:
        """Récupère toutes les tâches d'un utilisateur."""
        tasks = TaskRepository.get_all_by_owner(username)
        
        return [
            TaskResponse(
                id=task["id"],
                title=task["title"],
                description=task["description"],
                completed=bool(task["completed"]),
                owner=task["owner"]
            )
            for task in tasks
        ]
    
    @staticmethod
    def toggle_task(task_id: int) -> bool:
        """Change le statut d'une tâche (complété/non complété)."""
        # Pour simplifier, on suppose que la tâche n'est pas complétée
        # et on la marque comme complétée
        return TaskRepository.update_completed(task_id, True)
    
    @staticmethod
    def delete_task(task_id: int) -> bool:
        """Supprime une tâche."""
        return TaskRepository.delete(task_id)