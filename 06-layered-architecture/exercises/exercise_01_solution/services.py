"""
Solution Exercice 1 - Service (logique métier)
"""

from fastapi import HTTPException, status
from .repositories import NoteRepository
from .models import NoteCreate, NoteResponse


class NoteService:
    """Service pour gérer la logique métier des notes."""
    
    # Solution TODO 3: Implémenter les méthodes
    
    @staticmethod
    def create_note(note_data: NoteCreate) -> NoteResponse:
        """
        Crée une note.
        
        Logique métier : calculer passed = (grade >= 10)
        
        Args:
            note_data: Données de la note à créer
            
        Returns:
            NoteResponse avec passed calculé
        """
        # Créer la note dans la base
        note_id = NoteRepository.create(
            student_name=note_data.student_name,
            subject=note_data.subject,
            grade=note_data.grade
        )
        
        # Calculer passed (logique métier)
        passed = note_data.grade >= 10
        
        return NoteResponse(
            id=note_id,
            student_name=note_data.student_name,
            subject=note_data.subject,
            grade=note_data.grade,
            passed=passed
        )
    
    @staticmethod
    def get_note(note_id: int) -> NoteResponse:
        """
        Récupère une note par ID.
        
        Lever HTTPException 404 si non trouvé.
        Calculer passed pour la réponse.
        
        Args:
            note_id: ID de la note
            
        Returns:
            NoteResponse avec passed calculé
            
        Raises:
            HTTPException: 404 si la note n'existe pas
        """
        note = NoteRepository.get_by_id(note_id)
        
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note non trouvée"
            )
        
        # Calculer passed
        passed = note["grade"] >= 10
        
        return NoteResponse(
            id=note["id"],
            student_name=note["student_name"],
            subject=note["subject"],
            grade=note["grade"],
            passed=passed
        )
    
    @staticmethod
    def get_all_notes() -> list[NoteResponse]:
        """
        Récupère toutes les notes.
        
        Calculer passed pour chaque note.
        
        Returns:
            Liste de NoteResponse avec passed calculé
        """
        notes = NoteRepository.get_all()
        
        return [
            NoteResponse(
                id=note["id"],
                student_name=note["student_name"],
                subject=note["subject"],
                grade=note["grade"],
                passed=note["grade"] >= 10
            )
            for note in notes
        ]