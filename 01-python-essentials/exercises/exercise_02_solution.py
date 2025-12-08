"""
Solution de l'exercice 2 : Système de gestion d'utilisateurs
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
        self.users = {}
    
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
        # Validation du nom
        if not name or name.strip() == "":
            raise ValueError("Le nom ne peut pas être vide")
        
        # Validation de l'email
        if "@" not in email:
            raise InvalidEmailError("L'email doit contenir '@'")
        
        # Validation de l'âge
        if age < 0:
            raise ValueError("L'âge ne peut pas être négatif")
        
        # Vérification de l'existence de l'utilisateur
        if email in self.users:
            raise UserAlreadyExistsError(f"L'utilisateur {email} existe déjà")
        
        # Création de l'utilisateur
        user = {
            "name": name,
            "email": email,
            "age": age
        }
        self.users[email] = user
        
        return user
    
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
        if email not in self.users:
            raise UserNotFoundError(f"L'utilisateur {email} n'existe pas")
        
        return self.users[email]
    
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
        # Validation de l'âge
        if new_age < 0:
            raise ValueError("L'âge ne peut pas être négatif")
        
        # Récupération de l'utilisateur (lève UserNotFoundError si absent)
        user = self.get_user(email)
        
        # Mise à jour de l'âge
        user["age"] = new_age
        self.users[email] = user
        
        return user
    
    def count_users(self) -> int:
        """
        Retourne le nombre total d'utilisateurs.
        
        Returns:
            Nombre d'utilisateurs
        """
        return len(self.users)