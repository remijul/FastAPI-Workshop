"""
Solution Exercice 1 - Dépendances
"""

from fastapi import Depends, HTTPException, status, Header
from jose import JWTError, jwt
from typing import Optional
from .auth import SECRET_KEY, ALGORITHM


# Solution TODO 2

def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """
    Dépendance qui extrait et vérifie le token JWT.
    """
    # Vérifier que le header existe
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token manquant",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Extraire le token
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Type d'authentification invalide"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Format du header Authorization invalide"
        )
    
    # Décoder le token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide"
            )
        
        return username
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré"
        )