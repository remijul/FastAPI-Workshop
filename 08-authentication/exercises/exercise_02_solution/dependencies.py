"""
Solution Exercice 2 - Dépendances
"""

from fastapi import Depends, HTTPException, status, Header
from jose import JWTError, jwt
from typing import Optional
from .auth import SECRET_KEY, ALGORITHM
from .repositories import UserRepository


# Solution TODO 2a

def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """Dépendance qui vérifie le token JWT."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token manquant",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(401, "Type d'authentification invalide")
    except ValueError:
        raise HTTPException(401, "Format du header Authorization invalide")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        
        if not username:
            raise HTTPException(401, "Token invalide")
        
        return username
    
    except JWTError:
        raise HTTPException(401, "Token invalide ou expiré")


# Solution TODO 2b

def require_admin(current_user: str = Depends(get_current_user)) -> str:
    """
    Dépendance qui vérifie que l'utilisateur est admin.
    """
    # Récupérer l'utilisateur
    user = UserRepository.get_by_username(current_user)
    
    if not user:
        raise HTTPException(401, "Utilisateur non trouvé")
    
    # Vérifier le rôle
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux administrateurs"
        )
    
    return current_user