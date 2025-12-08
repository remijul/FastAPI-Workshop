"""
Exercice 1 - Routes API

TODO 4: Implémenter les routes
- POST /notes : Créer une note (status_code=201)
- GET /notes : Lister toutes les notes
- GET /notes/{note_id} : Récupérer une note
"""

from fastapi import APIRouter
from .models import NoteCreate, NoteResponse
from .services import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


# TODO 4: Implémenter les routes

# POST /notes
# GET /notes
# GET /notes/{note_id}