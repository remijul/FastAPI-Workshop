"""
Dépendances pour l'injection de dépendances FastAPI.

TODO NIVEAU 3 - Option Auth:
- Créer get_current_user() pour vérifier le token JWT
"""

from fastapi import Depends, HTTPException, status, Header
from typing import Optional


# TODO NIVEAU 3 - Option Auth: Créer la dépendance d'authentification

def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """
    Dépendance qui vérifie l'authentification JWT.
    
    TODO NIVEAU 3:
    - Vérifier le header Authorization
    - Extraire et décoder le token JWT
    - Retourner le username
    - Lever HTTPException 401 si invalide
    
    Returns:
        Username de l'utilisateur authentifié
    
    Raises:
        HTTPException: 401 si non authentifié
    """
    # TODO NIVEAU 3: Implémenter
    pass