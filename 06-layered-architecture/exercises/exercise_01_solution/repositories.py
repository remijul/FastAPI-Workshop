"""
Solution Exercice 1 - Repository (accès aux données)
"""

from .database import get_db_connection


class NoteRepository:
    """Repository pour gérer l'accès aux données des notes."""
    
    # Solution TODO 2: Implémenter les méthodes
    
    @staticmethod
    def create(student_name: str, subject: str, grade: float) -> int:
        """
        Crée une note et retourne son ID.
        
        Args:
            student_name: Nom de l'étudiant
            subject: Matière
            grade: Note (0-20)
            
        Returns:
            ID de la note créée
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO notes (student_name, subject, grade) VALUES (?, ?, ?)",
            (student_name, subject, grade)
        )
        note_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return note_id
    
    @staticmethod
    def get_by_id(note_id: int) -> dict | None:
        """
        Récupère une note par ID.
        
        Args:
            note_id: ID de la note
            
        Returns:
            Dictionnaire avec les données de la note ou None
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        return dict(row) if row else None
    
    @staticmethod
    def get_all() -> list[dict]:
        """
        Récupère toutes les notes.
        
        Returns:
            Liste de dictionnaires avec toutes les notes
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM notes")
        rows = cursor.fetchall()
        
        conn.close()
        
        return [dict(row) for row in rows]