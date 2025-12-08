"""Exercice 1 - Repositories"""

from .database import get_db_connection


class UserRepository:
    """Repository pour les utilisateurs."""
    
    @staticmethod
    def create(username: str, hashed_password: str) -> int:
        """Crée un utilisateur."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
            (username, hashed_password)
        )
        user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return user_id
    
    @staticmethod
    def get_by_username(username: str) -> dict | None:
        """Récupère un utilisateur par username."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        
        conn.close()
        
        return dict(row) if row else None


class ArticleRepository:
    """Repository pour les articles."""
    
    @staticmethod
    def create(title: str, content: str, author: str) -> int:
        """Crée un article."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO articles (title, content, author) VALUES (?, ?, ?)",
            (title, content, author)
        )
        article_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return article_id
    
    @staticmethod
    def get_all() -> list[dict]:
        """Récupère tous les articles."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()
        
        conn.close()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def get_by_author(author: str) -> list[dict]:
        """Récupère les articles d'un auteur."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM articles WHERE author = ?", (author,))
        rows = cursor.fetchall()
        
        conn.close()
        
        return [dict(row) for row in rows]