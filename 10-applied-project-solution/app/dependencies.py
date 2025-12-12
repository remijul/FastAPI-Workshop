"""
Dépendances pour l'injection de dépendances FastAPI.
SOLUTION COMPLÈTE - NIVEAU 3
"""

from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from jose import JWTError
from app.auth import decode_access_token


def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """
    Dépendance qui vérifie l'authentification JWT.
    
    Returns:
        Username de l'utilisateur authentifié
    
    Raises:
        HTTPException: 401 si non authentifié
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token d'authentification manquant",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Extraire le token
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Type d'authentification invalide. Utilisez 'Bearer <token>'"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Format du header Authorization invalide"
        )
    
    # Décoder le token
    try:
        payload = decode_access_token(token)
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