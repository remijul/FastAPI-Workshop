"""
Solution Exercice 2 - Repository
"""

from .database import get_db_connection


class TaskRepository:
    """Repository pour les tâches."""
    
    # Solution TODO 2: Implémenter les méthodes
    
    @staticmethod
    def create(title: str, priority: int, completed: bool) -> int:
        """
        Crée une tâche.
        
        Args:
            title: Titre de la tâche
            priority: Priorité (1-5)
            completed: Tâche complétée ou non
            
        Returns:
            ID de la tâche créée
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO tasks (title, priority, completed) VALUES (?, ?, ?)",
            (title, priority, int(completed))
        )
        task_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return task_id
    
    @staticmethod
    def get_by_id(task_id: int) -> dict | None:
        """
        Récupère une tâche par ID.
        
        Args:
            task_id: ID de la tâche
            
        Returns:
            Dictionnaire avec les données de la tâche ou None
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        return dict(row) if row else None
    
    @staticmethod
    def get_all() -> list[dict]:
        """
        Récupère toutes les tâches.
        
        Returns:
            Liste de dictionnaires avec toutes les tâches
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        
        conn.close()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def mark_completed(task_id: int) -> bool:
        """
        Marque une tâche comme complétée.
        
        Args:
            task_id: ID de la tâche
            
        Returns:
            True si la mise à jour a réussi, False sinon
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE tasks SET completed = 1 WHERE id = ?",
            (task_id,)
        )
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success