"""
Services contenant la logique métier.

TODO NIVEAU 1:
- Implémenter create_character() : Créer un personnage
- Implémenter get_character() : Récupérer un personnage (gérer 404)
- Implémenter get_all_characters() : Lister tous les personnages
- Implémenter update_character() : Modifier un personnage
- Implémenter delete_character() : Supprimer un personnage

TODO NIVEAU 2:
- Implémenter get_characters_filtered() : Filtrage
- Implémenter get_statistics() : Statistiques
- Implémenter level_up() : Augmenter le niveau

Rappel: Les services contiennent la LOGIQUE MÉTIER, pas de SQL direct.
"""

from app.repositories import CharacterRepository
from app.models import CharacterCreate, CharacterUpdate, CharacterResponse
from app.exceptions import CharacterNotFoundError
from typing import Optional


class CharacterService:
    """Service pour la logique métier des personnages."""
    
    @staticmethod
    def create_character(character_data: CharacterCreate) -> CharacterResponse:
        """
        Crée un nouveau personnage.
        
        TODO NIVEAU 1:
        - Appeler CharacterRepository.create() avec les données
        - Récupérer l'ID créé
        - Construire et retourner CharacterResponse
        
        Args:
            character_data: Données du personnage à créer
        
        Returns:
            CharacterResponse avec le personnage créé
        """
        # TODO: Implémenter
        pass
    
    @staticmethod
    def get_character(character_id: int) -> CharacterResponse:
        """
        Récupère un personnage par ID.
        
        TODO NIVEAU 1:
        - Appeler CharacterRepository.get_by_id()
        - Si None, lever CharacterNotFoundError (après avoir créé l'exception)
        - Sinon, construire et retourner CharacterResponse
        
        Args:
            character_id: ID du personnage
        
        Returns:
            CharacterResponse
        
        Raises:
            CharacterNotFoundError: Si le personnage n'existe pas
        """
        # TODO: Implémenter
        pass
    
    @staticmethod
    def get_all_characters() -> list[CharacterResponse]:
        """
        Récupère tous les personnages.
        
        TODO NIVEAU 1:
        - Appeler CharacterRepository.get_all()
        - Convertir chaque dict en CharacterResponse
        - Retourner la liste
        
        Returns:
            Liste de CharacterResponse
        """
        # TODO: Implémenter
        pass
    
    @staticmethod
    def update_character(character_id: int, 
                        character_data: CharacterUpdate) -> CharacterResponse:
        """
        Met à jour un personnage.
        
        TODO NIVEAU 1:
        - Vérifier que le personnage existe (get_character)
        - Construire un dict avec seulement les champs fournis (exclude_unset)
        - Appeler CharacterRepository.update()
        - Retourner le personnage mis à jour
        
        Args:
            character_id: ID du personnage
            character_data: Données à mettre à jour
        
        Returns:
            CharacterResponse mis à jour
        
        Raises:
            CharacterNotFoundError: Si le personnage n'existe pas
        """
        # TODO: Implémenter
        # Astuce: character_data.model_dump(exclude_unset=True)
        pass
    
    @staticmethod
    def delete_character(character_id: int) -> None:
        """
        Supprime un personnage.
        
        TODO NIVEAU 1:
        - Vérifier que le personnage existe
        - Appeler CharacterRepository.delete()
        
        Args:
            character_id: ID du personnage
        
        Raises:
            CharacterNotFoundError: Si le personnage n'existe pas
        """
        # TODO: Implémenter
        pass
    
    # TODO NIVEAU 2: Implémenter les fonctionnalités avancées
    
    @staticmethod
    def get_characters_filtered(character_class: Optional[str] = None,
                               min_level: Optional[int] = None,
                               max_level: Optional[int] = None) -> list[CharacterResponse]:
        """
        Récupère les personnages avec filtres.
        
        TODO NIVEAU 2:
        - Valider la classe si fournie (doit être dans VALID_CLASSES)
        - Appeler CharacterRepository.get_by_filters()
        - Convertir en CharacterResponse
        """
        # TODO NIVEAU 2: Implémenter
        pass
    
    @staticmethod
    def get_statistics() -> dict:
        """
        Récupère les statistiques globales.
        
        TODO NIVEAU 2:
        - Appeler CharacterRepository.get_stats()
        - Formater et retourner
        """
        # TODO NIVEAU 2: Implémenter
        pass
    
    @staticmethod
    def level_up(character_id: int) -> CharacterResponse:
        """
        Augmente le niveau d'un personnage de 1.
        
        TODO NIVEAU 2:
        - Récupérer le personnage
        - Vérifier qu'il n'est pas déjà niveau 100
        - Augmenter: level +1, health_points +10, attack +2, defense +1
        - Mettre à jour avec CharacterRepository.update()
        - Retourner le personnage mis à jour
        
        Raises:
            CharacterNotFoundError: Si le personnage n'existe pas
            ValueError: Si déjà niveau 100
        """
        # TODO NIVEAU 2: Implémenter
        pass


# TODO NIVEAU 3 - Option Combat: Créer BattleService
class BattleService:
    """Service pour gérer les combats entre personnages."""
    
    @staticmethod
    def simulate_battle(character1_id: int, character2_id: int) -> dict:
        """
        Simule un combat entre deux personnages.
        
        TODO NIVEAU 3:
        - Récupérer les deux personnages
        - Simuler le combat tour par tour
        - Retourner le résultat
        """
        # TODO NIVEAU 3: Implémenter
        pass


# TODO NIVEAU 3 - Option Auth: Créer AuthService
class AuthService:
    """Service pour l'authentification."""
    
    @staticmethod
    def register(username: str, password: str) -> bool:
        """Enregistre un utilisateur."""
        # TODO NIVEAU 3: Implémenter
        pass
    
    @staticmethod
    def authenticate(username: str, password: str) -> bool:
        """Authentifie un utilisateur."""
        # TODO NIVEAU 3: Implémenter
        pass