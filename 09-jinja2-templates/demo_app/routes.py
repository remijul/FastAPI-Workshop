"""Routes de l'application."""

from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .services import AuthService, TaskService
from .models import UserRegister, TaskCreate

router = APIRouter()
templates = Jinja2Templates(directory="demo_app/templates")


def get_current_user(request: Request) -> str | None:
    """Récupère l'utilisateur depuis le cookie."""
    return request.cookies.get("username")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Page d'accueil."""
    username = get_current_user(request)
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "username": username}
    )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    """Page d'inscription."""
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "error": None}
    )


@router.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """Traite l'inscription."""
    user_data = UserRegister(username=username, password=password)
    
    success = AuthService.register(user_data)
    
    if not success:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Ce nom d'utilisateur existe déjà"
            }
        )
    
    # Rediriger vers la page de login
    return RedirectResponse(url="/login?registered=true", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, registered: bool = False):
    """Page de connexion."""
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": None,
            "registered": registered
        }
    )


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """Traite la connexion."""
    is_valid = AuthService.authenticate(username, password)
    
    if not is_valid:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Identifiants incorrects",
                "registered": False
            }
        )
    
    # Créer une réponse avec cookie
    response = RedirectResponse(url="/tasks", status_code=303)
    response.set_cookie(key="username", value=username)
    return response


@router.get("/logout")
def logout():
    """Déconnexion."""
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="username")
    return response


@router.get("/tasks", response_class=HTMLResponse)
def tasks_page(request: Request):
    """Page des tâches (protégée)."""
    username = get_current_user(request)
    
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    
    # Récupérer les tâches de l'utilisateur
    tasks = TaskService.get_user_tasks(username)
    
    return templates.TemplateResponse(
        "tasks.html",
        {
            "request": request,
            "username": username,
            "tasks": tasks
        }
    )


@router.get("/tasks/new", response_class=HTMLResponse)
def new_task_page(request: Request):
    """Page pour créer une tâche."""
    username = get_current_user(request)
    
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse(
        "task_form.html",
        {"request": request, "username": username}
    )


@router.post("/tasks/new")
def create_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(...)
):
    """Crée une nouvelle tâche."""
    username = get_current_user(request)
    
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    
    task_data = TaskCreate(title=title, description=description)
    TaskService.create_task(task_data, username)
    
    return RedirectResponse(url="/tasks", status_code=303)


@router.post("/tasks/{task_id}/toggle")
def toggle_task(task_id: int):
    """Change le statut d'une tâche."""
    TaskService.toggle_task(task_id)
    return RedirectResponse(url="/tasks", status_code=303)


@router.post("/tasks/{task_id}/delete")
def delete_task(task_id: int):
    """Supprime une tâche."""
    TaskService.delete_task(task_id)
    return RedirectResponse(url="/tasks", status_code=303)