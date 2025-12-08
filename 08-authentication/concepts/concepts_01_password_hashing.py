"""
Concepts : Hachage de mots de passe

RÈGLE D'OR : Ne JAMAIS stocker les mots de passe en clair !
On utilise un algorithme de hachage (bcrypt) pour sécuriser les mots de passe.
"""

from fastapi import FastAPI
from passlib.context import CryptContext

app = FastAPI(
    title="API Password Hashing",
    description="Démonstration du hachage de mots de passe",
    version="1.0.0"
)

# Configurer le contexte de hachage avec bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Base de données simulée
users_db = {}


def hash_password(password: str) -> str:
    """
    Hache un mot de passe.
    
    Args:
        password: Mot de passe en clair
        
    Returns:
        Hash du mot de passe
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie qu'un mot de passe correspond au hash.
    
    Args:
        plain_password: Mot de passe en clair
        hashed_password: Hash stocké
        
    Returns:
        True si le mot de passe est correct
    """
    return pwd_context.verify(plain_password, hashed_password)


@app.post("/register")
def register(username: str, password: str):
    """
    Enregistre un utilisateur avec mot de passe haché.
    
    Le mot de passe n'est JAMAIS stocké en clair.
    """
    if username in users_db:
        return {"error": "Utilisateur existe déjà"}
    
    # Hacher le mot de passe avant de le stocker
    hashed_password = hash_password(password)
    
    users_db[username] = {
        "username": username,
        "hashed_password": hashed_password
    }
    
    return {
        "message": "Utilisateur créé",
        "username": username,
        "note": "Le mot de passe est stocké de manière sécurisée (haché)"
    }


@app.post("/login")
def login(username: str, password: str):
    """
    Vérifie les identifiants d'un utilisateur.
    """
    user = users_db.get(username)
    
    if not user:
        return {"error": "Utilisateur non trouvé"}
    
    # Vérifier le mot de passe
    if not verify_password(password, user["hashed_password"]):
        return {"error": "Mot de passe incorrect"}
    
    return {
        "message": "Connexion réussie",
        "username": username
    }


@app.get("/debug/users")
def debug_users():
    """
    Route de debug pour voir les utilisateurs.
    
    Notez que les mots de passe sont hachés (impossibles à lire).
    """
    return {
        "users": [
            {
                "username": user["username"],
                "hashed_password": user["hashed_password"][:50] + "..."  # Tronqué pour lisibilité
            }
            for user in users_db.values()
        ]
    }


# Pour lancer :
# uvicorn concepts.concepts_01_password_hashing:app --reload
#
# Tester :
# 1. POST /register?username=alice&password=secret123
# 2. GET /debug/users → Voir le hash (illisible)
# 3. POST /login?username=alice&password=secret123 → OK
# 4. POST /login?username=alice&password=wrongpass → Erreur
#
# Le hash change à chaque fois même avec le même mot de passe !
# C'est normal : bcrypt ajoute un "salt" aléatoire pour plus de sécurité.