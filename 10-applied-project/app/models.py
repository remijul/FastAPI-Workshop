"""
Modèles Pydantic pour la validation des données.

TODO NIVEAU 1:
- Créer CharacterBase avec tous les champs et leurs validations
- Créer CharacterCreate (hérite de CharacterBase)
- Créer CharacterUpdate (tous les champs optionnels)
- Créer CharacterResponse (ajoute id et created_at)

Rappel des champs :
- name: str (min 2 caractères)
- class: str (valeurs: "warrior", "mage", "archer", "tank", "healer")
- level: int (1-100)
- health_points: int (50-500)
- attack: int (10-100)
- defense: int (5-50)
- speed: int (10-100)
- special_ability: Optional[str]
- image_url: Optional[str]
- created_at: datetime (uniquement dans Response)
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.config import VALID_CLASSES


# TODO NIVEAU 1: Créer CharacterBase
class CharacterBase(BaseModel):
    """Modèle de base pour un personnage."""
    # TODO: Ajouter tous les champs avec Field() et leurs contraintes
    # Attention: utiliser alias="class" pour le champ class (mot-clé Python)
    pass


# TODO NIVEAU 1: Créer CharacterCreate
class CharacterCreate(CharacterBase):
    """Modèle pour créer un personnage."""
    # TODO: Hériter de CharacterBase
    # TODO NIVEAU 2 (optionnel): Ajouter un validateur pour vérifier que la classe est valide
    pass


# TODO NIVEAU 1: Créer CharacterUpdate
class CharacterUpdate(BaseModel):
    """Modèle pour modifier un personnage (tous les champs optionnels)."""
    # TODO: Tous les champs de CharacterBase mais en Optional
    pass


# TODO NIVEAU 1: Créer CharacterResponse
class CharacterResponse(CharacterBase):
    """Modèle de réponse pour un personnage."""
    # TODO: Ajouter id et created_at
    # TODO: Ajouter Config avec from_attributes = True
    pass


# TODO NIVEAU 2 (optionnel): Créer CharacterStats pour les statistiques
class CharacterStats(BaseModel):
    """Statistiques globales des personnages."""
    # TODO: Implémenter si vous faites le niveau 2
    pass


# TODO NIVEAU 3 - Option Combat: Créer les modèles pour le combat
class BattleRequest(BaseModel):
    """Requête de combat entre deux personnages."""
    # TODO: character1_id et character2_id
    pass


class BattleResult(BaseModel):
    """Résultat d'un combat."""
    # TODO: winner_id, loser_id, turns, winner_remaining_hp, battle_log
    pass


# TODO NIVEAU 3 - Option Auth: Créer les modèles pour l'authentification
class UserRegister(BaseModel):
    """Modèle pour l'inscription."""
    # TODO: username, password
    pass


class UserLogin(BaseModel):
    """Modèle pour la connexion."""
    # TODO: username, password
    pass


class Token(BaseModel):
    """Modèle pour le token JWT."""
    # TODO: access_token, token_type
    pass