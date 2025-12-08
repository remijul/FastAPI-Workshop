"""
Exercice 1 - Repository (accès aux données)

TODO 2: Implémenter le NoteRepository
- create(student_name, subject, grade) -> int : Crée une note, retourne l'ID
- get_by_id(note_id) -> dict | None : Récupère une note par ID
- get_all() -> list[dict] : Récupère toutes les notes
"""

from .database import get_db_connection


class NoteRepository:
    """Repository pour gérer l'accès aux données des notes."""
    
    # TODO 2: Implémenter les méthodes
    
    @staticmethod
    def create(student_name: str, subject: str, grade: float) -> int:
        """Crée une note et retourne son ID."""
        pass
    
    @staticmethod
    def get_by_id(note_id: int) -> dict | None:
        """Récupère une note par ID."""
        pass
    
    @staticmethod
    def get_all() -> list[dict]:
        """Récupère toutes les notes."""
        pass