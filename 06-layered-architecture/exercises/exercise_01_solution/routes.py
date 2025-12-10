"""
Solution Exercice 1 - Routes API
"""

from fastapi import APIRouter
from .models import NoteCreate, NoteResponse
from .services import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


# Solution TODO 4: Implémenter les routes

@router.post("", response_model=NoteResponse, status_code=201)
def create_note(note: NoteCreate):
    """
    Crée une nouvelle note.
    
    La route délègue tout au service.
    """
    return NoteService.create_note(note)


@router.get("", response_model=list[NoteResponse])
def get_all_notes():
    """Liste toutes les notes."""
    return NoteService.get_all_notes()


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int):
    """Récupère une note par ID."""
    return NoteService.get_note(note_id)