"""
Exercice 1 - Authentification

TODO 1: Implémenter les fonctions d'authentification
- hash_password(password) : Hacher un mot de passe avec bcrypt
- verify_password(plain_password, hashed_password) : Vérifier un mot de passe
- create_access_token(data) : Créer un JWT avec expiration de 30 minutes
"""

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

# Configuration
SECRET_KEY = "votre-clé-secrète-changez-moi-en-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexte de hachage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# TODO 1: Implémenter les 3 fonctions

def hash_password(password: str) -> str:
    """Hache un mot de passe avec bcrypt."""
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe contre son hash."""
    pass


def create_access_token(data: dict) -> str:
    """
    Crée un JWT.
    
    - Copier data
    - Ajouter expiration : datetime.now(timezone.utc) + timedelta(minutes=30)
    - Encoder avec jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    """
    pass