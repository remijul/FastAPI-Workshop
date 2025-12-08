"""
Concepts : JWT (JSON Web Tokens)

JWT = Jeton signé qui contient des informations (claims).
Utilisé pour maintenir la session utilisateur sans serveur de sessions.
"""

from fastapi import FastAPI, HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional

app = FastAPI(
    title="API JWT Basics",
    description="Démonstration des JWT",
    version="1.0.0"
)

# Configuration
SECRET_KEY = "votre-clé-secrète-super-longue-et-complexe-ne-jamais-partager"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexte de hachage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Base de données simulée
users_db = {}


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crée un JWT.
    
    Args:
        data: Données à inclure dans le token (ex: {"sub": "username"})
        expires_delta: Durée de validité du token
        
    Returns:
        Token JWT signé
    """
    to_encode = data.copy()
    
    # Définir l'expiration
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    
    # Créer et signer le token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Décode et vérifie un JWT.
    
    Args:
        token: JWT à décoder
        
    Returns:
        Données contenues dans le token
        
    Raises:
        HTTPException: Si le token est invalide ou expiré
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
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
    
    return {"message": "Utilisateur créé", "username": username}


@app.post("/login")
def login(username: str, password: str):
    """
    Authentifie un utilisateur et retourne un JWT.
    """
    user = users_db.get(username)
    
    if not user or not pwd_context.verify(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects"
        )
    
    # Créer le token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # en secondes
    }


@app.get("/protected")
def protected_route(token: str):
    """
    Route protégée : nécessite un token valide.
    
    En production, on utiliserait un header Authorization,
    mais pour simplifier on passe le token en query parameter.
    """
    # Décoder le token
    payload = decode_access_token(token)
    username = payload.get("sub")
    
    if not username:
        raise HTTPException(401, "Token invalide")
    
    return {
        "message": f"Bonjour {username}, vous êtes authentifié !",
        "username": username,
        "token_expires_at": datetime.fromtimestamp(payload.get("exp")).isoformat()
    }


# Pour lancer :
# uvicorn concepts.concepts_02_jwt_basics:app --reload
#
# Workflow complet :
# 1. POST /register?username=bob&password=secret123
# 2. POST /login?username=bob&password=secret123
#    → Copier le "access_token" de la réponse
# 3. GET /protected?token=<coller_le_token_ici>
#    → Accès autorisé !
# 4. Attendre 30 minutes ou modifier le token
#    → GET /protected?token=invalid → Erreur 401