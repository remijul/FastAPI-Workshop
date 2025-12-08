"""
Exercice 2 : Système de gestion d'utilisateurs

Objectif : Créer un système simple de gestion d'utilisateurs avec validation
et gestion d'erreurs personnalisées.

TODO:
1. Implémenter la classe UserManager
2. Créer et utiliser les exceptions personnalisées
3. Faire passer tous les tests dans tests/test_exercise_02.py
"""


class UserAlreadyExistsError(Exception):
    """Exception levée quand un utilisateur existe déjà."""
    pass


class UserNotFoundError(Exception):
    """Exception levée quand un utilisateur n'existe pas."""
    pass


class InvalidEmailError(Exception):
    """Exception levée quand l'email est invalide."""
    pass


class UserManager:
    """Gère une collection d'utilisateurs."""
    
    def __init__(self):
        """Initialise le gestionnaire d'utilisateurs."""
        # TODO: Initialiser un dictionnaire pour stocker les utilisateurs
        # Format suggéré: {email: {"name": ..., "email": ..., "age": ...}}
        pass
    
    def add_user(self, name: str, email: str, age: int) -> dict:
        """
        Ajoute un nouvel utilisateur.
        
        Args:
            name: Nom de l'utilisateur
            email: Email de l'utilisateur
            age: Âge de l'utilisateur
            
        Returns:
            Dictionnaire représentant l'utilisateur créé
            
        Raises:
            ValueError: Si le nom est vide ou l'âge est négatif
            InvalidEmailError: Si l'email ne contient pas '@'
            UserAlreadyExistsError: Si l'email existe déjà
        """
        # TODO: Valider le nom (non vide)
        # TODO: Valider l'email (contient '@')
        # TODO: Valider l'âge (>= 0)
        # TODO: Vérifier que l'email n'existe pas déjà
        # TODO: Ajouter l'utilisateur et le retourner
        pass
    
    def get_user(self, email: str) -> dict:
        """
        Récupère un utilisateur par son email.
        
        Args:
            email: Email de l'utilisateur
            
        Returns:
            Dictionnaire représentant l'utilisateur
            
        Raises:
            UserNotFoundError: Si l'utilisateur n'existe pas
        """
        # TODO: Chercher et retourner l'utilisateur
        # TODO: Lever une exception si non trouvé
        pass
    
    def update_age(self, email: str, new_age: int) -> dict:
        """
        Met à jour l'âge d'un utilisateur.
        
        Args:
            email: Email de l'utilisateur
            new_age: Nouvel âge
            
        Returns:
            Utilisateur mis à jour
            
        Raises:
            UserNotFoundError: Si l'utilisateur n'existe pas
            ValueError: Si l'âge est négatif
        """
        # TODO: Valider le nouvel âge
        # TODO: Récupérer l'utilisateur (utilisez get_user)
        # TODO: Mettre à jour l'âge et retourner l'utilisateur
        pass
    
    def count_users(self) -> int:
        """
        Retourne le nombre total d'utilisateurs.
        
        Returns:
            Nombre d'utilisateurs
        """
        # TODO: Retourner le nombre d'utilisateurs
        pass