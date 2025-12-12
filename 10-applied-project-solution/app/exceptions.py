"""
Exceptions personnalisées pour l'application.
SOLUTION COMPLÈTE
"""


class CharacterNotFoundError(Exception):
    """Exception levée quand un personnage n'existe pas."""
    
    def __init__(self, character_id: int):
        self.character_id = character_id
        self.message = f"Personnage avec l'ID {character_id} non trouvé"
        super().__init__(self.message)


class InvalidClassError(Exception):
    """Exception levée quand la classe du personnage est invalide."""
    
    def __init__(self, character_class: str, valid_classes: list[str]):
        self.character_class = character_class
        self.valid_classes = valid_classes
        self.message = f"Classe '{character_class}' invalide. Classes autorisées : {', '.join(valid_classes)}"
        super().__init__(self.message)


class InvalidLevelError(Exception):
    """Exception levée quand le niveau est hors limites."""
    
    def __init__(self, level: int, min_level: int = 1, max_level: int = 100):
        self.level = level
        self.min_level = min_level
        self.max_level = max_level
        self.message = f"Niveau {level} invalide. Doit être entre {min_level} et {max_level}"
        super().__init__(self.message)


class MaxLevelReachedError(Exception):
    """Exception levée quand un personnage est déjà au niveau maximum."""
    
    def __init__(self, character_id: int, max_level: int = 100):
        self.character_id = character_id
        self.max_level = max_level
        self.message = f"Le personnage {character_id} est déjà au niveau maximum ({max_level})"
        super().__init__(self.message)