"""Repositories pour l'accès aux données."""

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


class TaskRepository:
    """Repository pour les tâches."""
    
    @staticmethod
    def create(title: str, description: str, owner: str) -> int:
        """Crée une tâche."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO tasks (title, description, owner) VALUES (?, ?, ?)",
            (title, description, owner)
        )
        task_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return task_id
    
    @staticmethod
    def get_all_by_owner(owner: str) -> list[dict]:
        """Récupère toutes les tâches d'un utilisateur."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM tasks WHERE owner = ? ORDER BY id DESC",
            (owner,)
        )
        rows = cursor.fetchall()
        
        conn.close()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def update_completed(task_id: int, completed: bool) -> bool:
        """Met à jour le statut d'une tâche."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE tasks SET completed = ? WHERE id = ?",
            (int(completed), task_id)
        )
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    @staticmethod
    def delete(task_id: int) -> bool:
        """Supprime une tâche."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success