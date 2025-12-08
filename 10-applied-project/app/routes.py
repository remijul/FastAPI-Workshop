"""
Routes de l'API.

TODO NIVEAU 1:
- POST /characters : Créer un personnage
- GET /characters : Lister tous les personnages
- GET /characters/{id} : Récupérer un personnage
- PUT /characters/{id} : Modifier un personnage
- DELETE /characters/{id} : Supprimer un personnage

TODO NIVEAU 2:
- GET /characters?class=... : Filtrer par classe
- GET /characters?min_level=...&max_level=... : Filtrer par niveau
- GET /characters/stats : Statistiques
- GET /classes : Liste des classes
- POST /characters/{id}/level-up : Augmenter le niveau

Rappel: Les routes délèguent tout au service.
"""

from fastapi import APIRouter, Query, status
from typing import Optional
from app.models import CharacterCreate, CharacterUpdate, CharacterResponse
from app.services import CharacterService
from app.config import VALID_CLASSES

router = APIRouter(prefix="/characters", tags=["characters"])


# TODO NIVEAU 1: Implémenter les routes CRUD de base

@router.post("", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
def create_character(character: CharacterCreate):
    """
    Crée un nouveau personnage.
    
    TODO NIVEAU 1:
    - Appeler CharacterService.create_character()
    - Retourner le résultat
    """
    # TODO: Implémenter
    pass


@router.get("", response_model=list[CharacterResponse])
def get_characters(
    character_class: Optional[str] = Query(None, alias="class"),
    min_level: Optional[int] = Query(None, ge=1, le=100),
    max_level: Optional[int] = Query(None, ge=1, le=100)
):
    """
    Récupère tous les personnages avec filtres optionnels.
    
    TODO NIVEAU 1:
    - Si aucun filtre, appeler CharacterService.get_all_characters()
    
    TODO NIVEAU 2:
    - Si filtres présents, appeler CharacterService.get_characters_filtered()
    """
    # TODO: Implémenter
    pass


@router.get("/{character_id}", response_model=CharacterResponse)
def get_character(character_id: int):
    """
    Récupère un personnage par ID.
    
    TODO NIVEAU 1:
    - Appeler CharacterService.get_character()
    """
    # TODO: Implémenter
    pass


@router.put("/{character_id}", response_model=CharacterResponse)
def update_character(character_id: int, character: CharacterUpdate):
    """
    Met à jour un personnage.
    
    TODO NIVEAU 1:
    - Appeler CharacterService.update_character()
    """
    # TODO: Implémenter
    pass


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(character_id: int):
    """
    Supprime un personnage.
    
    TODO NIVEAU 1:
    - Appeler CharacterService.delete_character()
    - Ne rien retourner (204 No Content)
    """
    # TODO: Implémenter
    pass


# TODO NIVEAU 2: Implémenter les routes avancées

@router.get("/stats", response_model=dict)
def get_statistics():
    """
    Récupère les statistiques globales.
    
    TODO NIVEAU 2:
    - Appeler CharacterService.get_statistics()
    """
    # TODO NIVEAU 2: Implémenter
    pass


@router.post("/{character_id}/level-up", response_model=CharacterResponse)
def level_up_character(character_id: int):
    """
    Augmente le niveau d'un personnage de 1.
    
    TODO NIVEAU 2:
    - Appeler CharacterService.level_up()
    """
    # TODO NIVEAU 2: Implémenter
    pass


# Route pour lister les classes disponibles
@router.get("/classes", response_model=list[str], tags=["metadata"])
def get_classes():
    """
    Retourne la liste des classes de personnages disponibles.
    
    TODO NIVEAU 2:
    - Retourner VALID_CLASSES depuis config
    """
    # TODO NIVEAU 2: Implémenter (très simple)
    pass


# TODO NIVEAU 3 - Option Combat: Ajouter route de combat
# TODO NIVEAU 3 - Option Auth: Ajouter routes d'authentification
# TODO NIVEAU 3 - Option Jinja2: Ajouter routes web

# ==================== NIVEAU 3 - OPTION JINJA2 : ROUTES WEB ====================

# TODO NIVEAU 3: Décommenter et compléter ces routes si vous implémentez Jinja2

# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from app.config import VALID_CLASSES
# 
# templates = Jinja2Templates(directory="app/templates")
# 
# 
# @router.get("/", response_class=HTMLResponse, include_in_schema=False)
# def home_page(
#     request: Request,
#     character_class: Optional[str] = Query(None, alias="class"),
#     min_level: Optional[int] = Query(None, ge=1, le=100),
#     max_level: Optional[int] = Query(None, ge=1, le=100)
# ):
#     """
#     Page d'accueil avec liste des personnages.
#     
#     TODO NIVEAU 3:
#     - Si filtres présents, appeler get_characters_filtered()
#     - Sinon appeler get_all_characters()
#     - Retourner templates.TemplateResponse avec les données
#     """
#     # TODO: Implémenter
#     pass
# 
# 
# @router.get("/{character_id}/details", response_class=HTMLResponse, include_in_schema=False)
# def character_detail_page(request: Request, character_id: int):
#     """
#     Page de détail d'un personnage.
#     
#     TODO NIVEAU 3:
#     - Récupérer le personnage avec get_character()
#     - Retourner templates.TemplateResponse
#     """
#     # TODO: Implémenter
#     pass