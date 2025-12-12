"""
Routes de l'API.
SOLUTION COMPLÈTE
"""

from fastapi import APIRouter, Query, status, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from app.models import CharacterCreate, CharacterUpdate, CharacterResponse, BattleRequest, BattleResult
from app.services import CharacterService, BattleService
from app.config import VALID_CLASSES
from app.dependencies import get_current_user

router = APIRouter(prefix="/characters", tags=["characters"])

# Configuration Jinja2 (NIVEAU 3)
templates = Jinja2Templates(directory="app/templates")


# ==================== NIVEAU 1 : CRUD DE BASE ====================

@router.post("", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
def create_character(
    character: CharacterCreate,
    current_user: str = Depends(get_current_user)  # NIVEAU 3: Protection
):
    """Crée un nouveau personnage (nécessite authentification)."""
    return CharacterService.create_character(character)


@router.get("", response_model=list[CharacterResponse])
def get_characters(
    character_class: Optional[str] = Query(None, alias="class"),
    min_level: Optional[int] = Query(None, ge=1, le=100),
    max_level: Optional[int] = Query(None, ge=1, le=100)
):
    """Récupère tous les personnages avec filtres optionnels."""
    # Si des filtres sont présents (NIVEAU 2)
    if character_class or min_level or max_level:
        return CharacterService.get_characters_filtered(
            character_class=character_class,
            min_level=min_level,
            max_level=max_level
        )
    
    # Sinon, retourner tous les personnages (NIVEAU 1)
    return CharacterService.get_all_characters()


@router.get("/{character_id}", response_model=CharacterResponse)
def get_character(character_id: int):
    """Récupère un personnage par ID."""
    return CharacterService.get_character(character_id)


@router.put("/{character_id}", response_model=CharacterResponse)
def update_character(character_id: int, character: CharacterUpdate):
    """Met à jour un personnage."""
    return CharacterService.update_character(character_id, character)


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(
    character_id: int,
    current_user: str = Depends(get_current_user)  # NIVEAU 3: Protection
):
    """Supprime un personnage (nécessite authentification)."""
    CharacterService.delete_character(character_id)


# ==================== NIVEAU 2 : ENDPOINTS AVANCÉS ====================

@router.get("/stats/global", response_model=dict, tags=["statistics"])
def get_statistics():
    """Récupère les statistiques globales."""
    return CharacterService.get_statistics()


@router.post("/{character_id}/level-up", response_model=CharacterResponse)
def level_up_character(character_id: int):
    """Augmente le niveau d'un personnage de 1."""
    return CharacterService.level_up(character_id)


# Route pour lister les classes disponibles
@router.get("/metadata/classes", response_model=list[str], tags=["metadata"])
def get_classes():
    """Retourne la liste des classes de personnages disponibles."""
    return VALID_CLASSES


# ==================== NIVEAU 3 - OPTION COMBAT ====================

@router.post("/battle", response_model=BattleResult, tags=["battle"])
def battle(battle_request: BattleRequest):
    """Simule un combat entre deux personnages."""
    result = BattleService.simulate_battle(
        battle_request.character1_id,
        battle_request.character2_id
    )
    return result


# ==================== NIVEAU 3 - OPTION JINJA2 : ROUTES WEB ====================

@router.get("/web/home", response_class=HTMLResponse, include_in_schema=False, tags=["web"])
def home_page(
    request: Request,
    character_class: Optional[str] = Query(None, alias="class"),
    min_level: Optional[int] = Query(None, ge=1, le=100),
    max_level: Optional[int] = Query(None, ge=1, le=100)
):
    """Page d'accueil avec liste des personnages."""
    # Récupérer les personnages (avec ou sans filtres)
    if character_class or min_level or max_level:
        characters = CharacterService.get_characters_filtered(
            character_class=character_class,
            min_level=min_level,
            max_level=max_level
        )
    else:
        characters = CharacterService.get_all_characters()
    
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "characters": characters,
            "classes": VALID_CLASSES,
            "selected_class": character_class,
            "min_level": min_level,
            "max_level": max_level
        }
    )


@router.get("/{character_id}/details", response_class=HTMLResponse, include_in_schema=False, tags=["web"])
def character_detail_page(request: Request, character_id: int):
    """Page de détail d'un personnage."""
    character = CharacterService.get_character(character_id)
    
    return templates.TemplateResponse(
        "character_detail.html",
        {
            "request": request,
            "character": character
        }
    )


# ==================== NIVEAU 3 - OPTION AUTH : ROUTES D'AUTHENTIFICATION ====================

from app.models import UserRegister, UserLogin, Token
from app.services import AuthService
from app.auth import create_access_token
from fastapi import HTTPException

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post("/register")
def register(user: UserRegister):
    """Enregistre un nouvel utilisateur."""
    success = AuthService.register(user.username, user.password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce nom d'utilisateur existe déjà"
        )
    
    return {"message": "Utilisateur créé avec succès"}


@auth_router.post("/login", response_model=Token)
def login(user: UserLogin):
    """Authentifie un utilisateur et retourne un token JWT."""
    is_valid = AuthService.authenticate(user.username, user.password)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects"
        )
    
    # Créer le token
    access_token = create_access_token(data={"sub": user.username})
    
    return Token(access_token=access_token, token_type="bearer")

@router.get("/web/battle", response_class=HTMLResponse, include_in_schema=False, tags=["web"])
def battle_page(request: Request):
    """Page web pour les combats entre personnages."""
    # Récupérer tous les personnages
    characters = CharacterService.get_all_characters()
    
    return templates.TemplateResponse(
        "battle.html",
        {
            "request": request,
            "characters": characters
        }
    )