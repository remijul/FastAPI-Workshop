"""
Exercice 1 - Dépendances

TODO 2: Implémenter la dépendance get_current_user
- Extraire le token du header Authorization
- Décoder le token JWT
- Retourner le username
- Lever HTTPException 401 si invalide
"""

from fastapi import Depends, HTTPException, status, Header
from jose import JWTError, jwt
from typing import Optional
from .auth import SECRET_KEY, ALGORITHM


# TODO 2: Implémenter get_current_user

def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """
    Dépendance qui extrait et vérifie le token JWT.
    
    Steps:
    1. Vérifier que authorization n'est pas None
    2. Extraire le token : scheme, token = authorization.split()
    3. Vérifier que scheme == "bearer" (case insensitive)
    4. Décoder le token : jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    5. Extraire username du payload : payload.get("sub")
    6. Retourner username
    
    Lever HTTPException 401 à chaque étape si erreur.
    """
    pass