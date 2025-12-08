"""Exercice 2 - Routes"""

from fastapi import APIRouter, Depends
from .models import UserRegister, UserLogin, Token, TaskCreate, TaskResponse
from .services import AuthService, TaskService
from .dependencies import get_current_user, require_admin

auth_router = APIRouter(prefix="/auth", tags=["auth"])
tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])


# Routes d'authentification
@auth_router.post("/register")
def register(user: UserRegister):
    """Enregistre un utilisateur."""
    return AuthService.register(user)


@auth_router.post("/login", response_model=Token)
def login(user: UserLogin):
    """Authentifie un utilisateur."""
    return AuthService.login(user)


# Routes utilisateur
@tasks_router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    current_user: str = Depends(get_current_user)
):
    """Crée une tâche (protégé)."""
    return TaskService.create_task(task, current_user)


@tasks_router.get("/my-tasks", response_model=list[TaskResponse])
def get_my_tasks(current_user: str = Depends(get_current_user)):
    """Récupère mes tâches (protégé)."""
    return TaskService.get_my_tasks(current_user)


# Routes admin
@tasks_router.get("/all", response_model=list[TaskResponse])
def get_all_tasks(admin_user: str = Depends(require_admin)):
    """Récupère toutes les tâches (admin only)."""
    return TaskService.get_all_tasks()


@tasks_router.delete("/{task_id}")
def delete_task(task_id: int, admin_user: str = Depends(require_admin)):
    """Supprime une tâche (admin only)."""
    return TaskService.delete_task(task_id)