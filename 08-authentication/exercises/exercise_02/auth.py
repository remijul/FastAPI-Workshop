"""
Exercice 2 - Authentification

TODO 1: Implémenter les fonctions d'authentification (identique à exercice 1)
"""

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "votre-clé-secrète-changez-moi-en-production-exercice2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# TODO 1: Implémenter les 3 fonctions

def hash_password(password: str) -> str:
    """Hache un mot de passe."""
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe."""
    pass


def create_access_token(data: dict) -> str:
    """Crée un JWT avec expiration."""
    pass