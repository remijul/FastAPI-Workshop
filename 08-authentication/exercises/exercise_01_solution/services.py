"""Solution Exercice 1 - Services"""

from fastapi import HTTPException, status
from .repositories import UserRepository, ArticleRepository
from .models import UserRegister, UserLogin, Token, ArticleCreate, ArticleResponse
from .auth import hash_password, verify_password, create_access_token


class AuthService:
    """Service d'authentification."""
    
    @staticmethod
    def register(user_data: UserRegister) -> dict:
        """Enregistre un nouvel utilisateur."""
        existing_user = UserRepository.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nom d'utilisateur déjà pris"
            )
        
        hashed_password = hash_password(user_data.password)
        UserRepository.create(user_data.username, hashed_password)
        
        return {"message": "Utilisateur créé avec succès"}
    
    @staticmethod
    def login(user_data: UserLogin) -> Token:
        """Authentifie un utilisateur et retourne un token."""
        user = UserRepository.get_by_username(user_data.username)
        
        if not user or not verify_password(user_data.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Identifiants incorrects"
            )
        
        access_token = create_access_token(data={"sub": user_data.username})
        
        return Token(access_token=access_token, token_type="bearer")


class ArticleService:
    """Service pour les articles."""
    
    @staticmethod
    def create_article(article_data: ArticleCreate, author: str) -> ArticleResponse:
        """Crée un article."""
        article_id = ArticleRepository.create(
            title=article_data.title,
            content=article_data.content,
            author=author
        )
        
        return ArticleResponse(
            id=article_id,
            title=article_data.title,
            content=article_data.content,
            author=author
        )
    
    @staticmethod
    def get_all_articles() -> list[ArticleResponse]:
        """Récupère tous les articles."""
        articles = ArticleRepository.get_all()
        return [ArticleResponse(**article) for article in articles]
    
    @staticmethod
    def get_my_articles(username: str) -> list[ArticleResponse]:
        """Récupère les articles de l'utilisateur connecté."""
        articles = ArticleRepository.get_by_author(username)
        return [ArticleResponse(**article) for article in articles]