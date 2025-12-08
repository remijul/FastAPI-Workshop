"""
Exceptions personnalisées pour l'application.

TODO NIVEAU 2:
- Créer CharacterNotFoundError
- Créer InvalidClassError
- Créer InvalidLevelError
- Ajouter les gestionnaires d'exceptions dans main.py
"""


# TODO NIVEAU 2: Créer les exceptions personnalisées

class CharacterNotFoundError(Exception):
    """Exception levée quand un personnage n'existe pas."""
    # TODO NIVEAU 2: Implémenter
    # Astuce: __init__(self, character_id: int)
    pass


class InvalidClassError(Exception):
    """Exception levée quand la classe du personnage est invalide."""
    # TODO NIVEAU 2: Implémenter
    pass


class InvalidLevelError(Exception):
    """Exception levée quand le niveau est hors limites."""
    # TODO NIVEAU 2: Implémenter
    pass