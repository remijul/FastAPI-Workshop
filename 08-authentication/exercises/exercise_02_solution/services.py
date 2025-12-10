"""Exercice 2 - Services"""

from fastapi import HTTPException, status
from .repositories import UserRepository, TaskRepository
from .models import UserRegister, UserLogin, Token, TaskCreate, TaskResponse
from .auth import hash_password, verify_password, create_access_token


class AuthService:
    """Service d'authentification."""
    
    @staticmethod
    def register(user_data: UserRegister) -> dict:
        """Enregistre un nouvel utilisateur."""
        existing_user = UserRepository.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(400, "Nom d'utilisateur déjà pris")
        
        hashed_password = hash_password(user_data.password)
        UserRepository.create(user_data.username, hashed_password, user_data.role.value)
        
        return {"message": "Utilisateur créé avec succès"}
    
    @staticmethod
    def login(user_data: UserLogin) -> Token:
        """Authentifie un utilisateur."""
        user = UserRepository.get_by_username(user_data.username)
        
        if not user or not verify_password(user_data.password, user["hashed_password"]):
            raise HTTPException(401, "Identifiants incorrects")
        
        access_token = create_access_token(data={"sub": user_data.username})
        
        return Token(access_token=access_token, token_type="bearer")


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
            owner=owner,
            completed=False
        )
    
    @staticmethod
    def get_my_tasks(username: str) -> list[TaskResponse]:
        """Récupère les tâches de l'utilisateur."""
        tasks = TaskRepository.get_by_owner(username)
        return [
            TaskResponse(
                id=task["id"],
                title=task["title"],
                description=task["description"],
                owner=task["owner"],
                completed=bool(task["completed"])
            )
            for task in tasks
        ]
    
    @staticmethod
    def get_all_tasks() -> list[TaskResponse]:
        """Récupère toutes les tâches (admin only)."""
        tasks = TaskRepository.get_all()
        return [
            TaskResponse(
                id=task["id"],
                title=task["title"],
                description=task["description"],
                owner=task["owner"],
                completed=bool(task["completed"])
            )
            for task in tasks
        ]
    
    @staticmethod
    def delete_task(task_id: int) -> dict:
        """Supprime une tâche (admin only)."""
        success = TaskRepository.delete(task_id)
        
        if not success:
            raise HTTPException(404, "Tâche non trouvée")
        
        return {"message": "Tâche supprimée"}