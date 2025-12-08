"""
Concepts : Dependency Injection FastAPI

Dependency Injection = Injection de dépendances
Permet de réutiliser du code (ex: vérifier l'authentification) sur plusieurs routes.
"""

from fastapi import FastAPI, Depends, HTTPException, status, Header
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional

app = FastAPI(
    title="API Dependency Injection",
    description="Démonstration de l'injection de dépendances",
    version="1.0.0"
)

# Configuration
SECRET_KEY = "votre-clé-secrète-super-longue-et-complexe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
users_db = {}


def create_access_token(data: dict):
    """Crée un JWT."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# DEPENDENCY : Fonction qui extrait et vérifie le token
def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """
    Dépendance qui vérifie l'authentification.
    
    Cette fonction peut être réutilisée sur toutes les routes protégées.
    
    Args:
        authorization: Header Authorization (format: "Bearer <token>")
        
    Returns:
        Username de l'utilisateur authentifié
        
    Raises:
        HTTPException 401: Si le token est manquant ou invalide
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token manquant",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Extraire le token du header "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(401, "Type d'authentification invalide")
    except ValueError:
        raise HTTPException(401, "Format du header Authorization invalide")
    
    # Décoder le token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        
        if not username:
            raise HTTPException(401, "Token invalide")
        
        return username
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré"
        )


@app.post("/register")
def register(username: str, password: str):
    """Enregistre un utilisateur."""
    if username in users_db:
        raise HTTPException(400, "Utilisateur existe déjà")
    
    users_db[username] = {
        "username": username,
        "hashed_password": pwd_context.hash(password)
    }
    
    return {"message": "Utilisateur créé"}


@app.post("/login")
def login(username: str, password: str):
    """Authentifie et retourne un token."""
    user = users_db.get(username)
    
    if not user or not pwd_context.verify(password, user["hashed_password"]):
        raise HTTPException(401, "Identifiants incorrects")
    
    access_token = create_access_token(data={"sub": username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Route protégée utilisant la dépendance
@app.get("/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    """
    Route protégée : seuls les utilisateurs authentifiés peuvent y accéder.
    
    Le paramètre current_user est automatiquement injecté par FastAPI
    via la dépendance get_current_user.
    """
    return {
        "username": current_user,
        "message": f"Bonjour {current_user} !"
    }


# Autre route protégée utilisant la même dépendance
@app.get("/profile")
def get_profile(current_user: str = Depends(get_current_user)):
    """Autre route protégée - réutilise la même dépendance."""
    user = users_db.get(current_user)
    return {
        "username": user["username"],
        "account_created": "2024-01-01"  # Exemple
    }


# Route publique (pas de dépendance)
@app.get("/public")
def public_route():
    """Route publique accessible sans authentification."""
    return {"message": "Cette route est publique"}


# Pour lancer :
# uvicorn concepts.concepts_03_dependency_injection:app --reload
#
# Workflow :
# 1. POST /register?username=alice&password=secret
# 2. POST /login?username=alice&password=secret
#    → Copier le access_token
# 3. GET /me avec header: Authorization: Bearer <token>
#    → Accès autorisé
# 4. GET /profile avec le même header
#    → Accès autorisé (même dépendance réutilisée)
# 5. GET /me sans header
#    → Erreur 401
# 6. GET /public (pas besoin de token)
#    → OK
#
# Avantage : Le code de vérification du token est écrit une seule fois
# et réutilisé avec Depends() sur toutes les routes protégées !