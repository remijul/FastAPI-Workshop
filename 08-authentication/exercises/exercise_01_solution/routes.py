"""Solution Exercice 1 - Routes"""

from fastapi import APIRouter, Depends
from .models import UserRegister, UserLogin, Token, ArticleCreate, ArticleResponse
from .services import AuthService, ArticleService
from .dependencies import get_current_user

auth_router = APIRouter(prefix="/auth", tags=["auth"])
articles_router = APIRouter(prefix="/articles", tags=["articles"])


@auth_router.post("/register")
def register(user: UserRegister):
    """Enregistre un nouvel utilisateur."""
    return AuthService.register(user)


@auth_router.post("/login", response_model=Token)
def login(user: UserLogin):
    """Authentifie un utilisateur."""
    return AuthService.login(user)


@articles_router.get("", response_model=list[ArticleResponse])
def get_all_articles():
    """Liste tous les articles (public)."""
    return ArticleService.get_all_articles()


@articles_router.post("", response_model=ArticleResponse, status_code=201)
def create_article(
    article: ArticleCreate,
    current_user: str = Depends(get_current_user)
):
    """Crée un article (protégé)."""
    return ArticleService.create_article(article, current_user)


@articles_router.get("/my-articles", response_model=list[ArticleResponse])
def get_my_articles(current_user: str = Depends(get_current_user)):
    """Récupère les articles de l'utilisateur connecté (protégé)."""
    return ArticleService.get_my_articles(current_user)