"""
Exercice 1 - Service (logique métier)

TODO 3: Implémenter le NoteService
- create_note(note_data) -> NoteResponse : Crée une note avec passed=(grade >= 10)
- get_note(note_id) -> NoteResponse : Récupère une note (404 si non trouvé)
- get_all_notes() -> list[NoteResponse] : Récupère toutes les notes avec passed calculé
"""

from fastapi import HTTPException, status
from .repositories import NoteRepository
from .models import NoteCreate, NoteResponse


class NoteService:
    """Service pour gérer la logique métier des notes."""
    
    # TODO 3: Implémenter les méthodes
    
    @staticmethod
    def create_note(note_data: NoteCreate) -> NoteResponse:
        """
        Crée une note.
        
        Logique métier : calculer passed = (grade >= 10)
        """
        pass
    
    @staticmethod
    def get_note(note_id: int) -> NoteResponse:
        """
        Récupère une note par ID.
        
        Lever HTTPException 404 si non trouvé.
        Calculer passed pour la réponse.
        """
        pass
    
    @staticmethod
    def get_all_notes() -> list[NoteResponse]:
        """
        Récupère toutes les notes.
        
        Calculer passed pour chaque note.
        """
        pass