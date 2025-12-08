"""
Exercice 2 - Dépendances

TODO 2: Implémenter 2 dépendances
- get_current_user : Extraire et vérifier le token (identique à exercice 1)
- require_admin : Vérifier que l'utilisateur est admin
"""

from fastapi import Depends, HTTPException, status, Header
from jose import JWTError, jwt
from typing import Optional
from .auth import SECRET_KEY, ALGORITHM
from .repositories import UserRepository


# TODO 2a: Implémenter get_current_user (identique à exercice 1)

def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """Dépendance qui vérifie le token JWT."""
    pass


# TODO 2b: Implémenter require_admin

def require_admin(current_user: str = Depends(get_current_user)) -> str:
    """
    Dépendance qui vérifie que l'utilisateur est admin.
    
    Steps:
    1. Récupérer l'utilisateur depuis la DB : UserRepository.get_by_username(current_user)
    2. Vérifier que user["role"] == "admin"
    3. Si non admin, lever HTTPException 403 "Accès réservé aux administrateurs"
    4. Retourner current_user
    """
    pass