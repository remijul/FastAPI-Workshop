"""
Repository pour l'accès aux données (couche SQL).

TODO NIVEAU 1:
- Implémenter create() : Créer un personnage
- Implémenter get_by_id() : Récupérer un personnage par ID
- Implémenter get_all() : Récupérer tous les personnages
- Implémenter update() : Modifier un personnage
- Implémenter delete() : Supprimer un personnage

TODO NIVEAU 2:
- Implémenter get_by_filters() : Filtrer par classe et/ou niveau
- Implémenter get_stats() : Calculer les statistiques

Rappel: Les repositories ne contiennent QUE du SQL, pas de logique métier.
"""

from app.database import get_db_connection
from typing import Optional


class CharacterRepository:
    """Repository pour l'accès aux données des personnages."""
    
    @staticmethod
    def create(name: str, character_class: str, level: int, health_points: int,
               attack: int, defense: int, speed: int, 
               special_ability: Optional[str] = None,
               image_url: Optional[str] = None) -> int:
        """
        Crée un nouveau personnage.
        
        TODO NIVEAU 1:
        - Ouvrir la connexion
        - Exécuter INSERT INTO characters
        - Récupérer cursor.lastrowid
        - Commit et fermer
        - Retourner l'ID
        
        Returns:
            ID du personnage créé
        """
        # TODO: Implémenter
        pass
    
    @staticmethod
    def get_by_id(character_id: int) -> dict | None:
        """
        Récupère un personnage par ID.
        
        TODO NIVEAU 1:
        - Ouvrir la connexion
        - Exécuter SELECT * FROM characters WHERE id = ?
        - Récupérer avec fetchone()
        - Fermer la connexion
        - Retourner dict(row) si trouvé, sinon None
        
        Returns:
            Dictionnaire avec les données du personnage ou None
        """
        # TODO: Implémenter
        pass
    
    @staticmethod
    def get_all() -> list[dict]:
        """
        Récupère tous les personnages.
        
        TODO NIVEAU 1:
        - Ouvrir la connexion
        - Exécuter SELECT * FROM characters ORDER BY id
        - Récupérer avec fetchall()
        - Fermer la connexion
        - Retourner [dict(row) for row in rows]
        
        Returns:
            Liste de dictionnaires avec tous les personnages
        """
        # TODO: Implémenter
        pass
    
    @staticmethod
    def update(character_id: int, **updates) -> bool:
        """
        Met à jour un personnage.
        
        TODO NIVEAU 1:
        - Construire dynamiquement la requête UPDATE avec les champs fournis
        - Exécuter la requête
        - Vérifier cursor.rowcount > 0
        - Retourner True si succès, False sinon
        
        Args:
            character_id: ID du personnage
            **updates: Champs à mettre à jour (name=..., level=..., etc.)
        
        Returns:
            True si la mise à jour a réussi, False sinon
        """
        # TODO: Implémenter
        # Astuce: updates.items() pour construire SET name=?, level=?, ...
        pass
    
    @staticmethod
    def delete(character_id: int) -> bool:
        """
        Supprime un personnage.
        
        TODO NIVEAU 1:
        - Exécuter DELETE FROM characters WHERE id = ?
        - Vérifier cursor.rowcount > 0
        - Retourner True si succès, False sinon
        
        Returns:
            True si la suppression a réussi, False sinon
        """
        # TODO: Implémenter
        pass
    
    # TODO NIVEAU 2: Implémenter les méthodes de filtrage et statistiques
    
    @staticmethod
    def get_by_filters(character_class: Optional[str] = None,
                       min_level: Optional[int] = None,
                       max_level: Optional[int] = None) -> list[dict]:
        """
        Récupère les personnages avec filtres.
        
        TODO NIVEAU 2:
        - Construire dynamiquement la clause WHERE selon les filtres fournis
        - Gérer les cas : class seul, level seul, ou combinaison
        
        Returns:
            Liste de personnages filtrés
        """
        # TODO NIVEAU 2: Implémenter
        pass
    
    @staticmethod
    def get_stats() -> dict:
        """
        Calcule les statistiques globales.
        
        TODO NIVEAU 2:
        - COUNT total
        - COUNT par classe
        - AVG level
        - MIN/MAX level
        - AVG attack par classe
        
        Returns:
            Dictionnaire avec les statistiques
        """
        # TODO NIVEAU 2: Implémenter
        pass


# TODO NIVEAU 3 - Option Auth: Créer UserRepository
class UserRepository:
    """Repository pour les utilisateurs."""
    
    @staticmethod
    def create(username: str, hashed_password: str) -> int:
        """Crée un utilisateur."""
        # TODO NIVEAU 3: Implémenter
        pass
    
    @staticmethod
    def get_by_username(username: str) -> dict | None:
        """Récupère un utilisateur par username."""
        # TODO NIVEAU 3: Implémenter
        pass