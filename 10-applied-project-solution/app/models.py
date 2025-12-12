"""
Modèles Pydantic pour la validation des données.
SOLUTION COMPLÈTE
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.config import VALID_CLASSES


class CharacterBase(BaseModel):
    """Modèle de base pour un personnage."""
    name: str = Field(..., min_length=2, description="Nom du personnage")
    character_class: str = Field(..., alias="class", description="Classe du personnage")
    level: int = Field(..., ge=1, le=100, description="Niveau du personnage")
    health_points: int = Field(..., ge=50, le=500, description="Points de vie")
    attack: int = Field(..., ge=10, le=100, description="Points d'attaque")
    defense: int = Field(..., ge=5, le=50, description="Points de défense")
    speed: int = Field(..., ge=10, le=100, description="Vitesse")
    special_ability: Optional[str] = Field(None, description="Capacité spéciale")
    image_url: Optional[str] = Field(None, description="URL de l'image")


class CharacterCreate(CharacterBase):
    """Modèle pour créer un personnage."""
    
    @field_validator('character_class')
    @classmethod
    def validate_class(cls, v):
        """Valide que la classe est dans la liste autorisée."""
        if v not in VALID_CLASSES:
            raise ValueError(f"Classe invalide. Valeurs autorisées : {', '.join(VALID_CLASSES)}")
        return v


class CharacterUpdate(BaseModel):
    """Modèle pour modifier un personnage (tous les champs optionnels)."""
    name: Optional[str] = Field(None, min_length=2)
    character_class: Optional[str] = Field(None, alias="class")
    level: Optional[int] = Field(None, ge=1, le=100)
    health_points: Optional[int] = Field(None, ge=50, le=500)
    attack: Optional[int] = Field(None, ge=10, le=100)
    defense: Optional[int] = Field(None, ge=5, le=50)
    speed: Optional[int] = Field(None, ge=10, le=100)
    special_ability: Optional[str] = None
    image_url: Optional[str] = None
    
    @field_validator('character_class')
    @classmethod
    def validate_class(cls, v):
        """Valide que la classe est dans la liste autorisée."""
        if v is not None and v not in VALID_CLASSES:
            raise ValueError(f"Classe invalide. Valeurs autorisées : {', '.join(VALID_CLASSES)}")
        return v


class CharacterResponse(CharacterBase):
    """Modèle de réponse pour un personnage."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class CharacterStats(BaseModel):
    """Statistiques globales des personnages."""
    total_characters: int
    characters_by_class: dict[str, int]
    average_level: float
    min_level: int
    max_level: int
    average_attack_by_class: dict[str, float]


class ClassInfo(BaseModel):
    """Information sur une classe."""
    class_name: str
    count: int


# ==================== NIVEAU 3 - OPTION COMBAT ====================

class BattleRequest(BaseModel):
    """Requête de combat entre deux personnages."""
    character1_id: int
    character2_id: int


class BattleResult(BaseModel):
    """Résultat d'un combat."""
    winner_id: int
    winner_name: str
    loser_id: int
    loser_name: str
    turns: int
    winner_remaining_hp: int
    battle_log: list[str]


# ==================== NIVEAU 3 - OPTION AUTH ====================

class UserRegister(BaseModel):
    """Modèle pour l'inscription."""
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Modèle pour la connexion."""
    username: str
    password: str


class Token(BaseModel):
    """Modèle pour le token JWT."""
    access_token: str
    token_type: str