# Étape 8 : Authentification JWT

## Objectifs

Cette étape vous apprend à sécuriser votre API avec authentification JWT :

- Hacher les mots de passe avec bcrypt
- Créer et vérifier des tokens JWT
- Protéger les routes avec dependency injection
- Gérer les rôles utilisateur (user/admin)

## Prérequis

- Python 3.8 ou supérieur installé
- Avoir validé l'étape 7 (Gestion des erreurs)

## Installation
```bash
pip install -r requirements.txt
```

Nouveaux packages :
- `python-jose[cryptography]` : Création et vérification de JWT
- `passlib[bcrypt]` : Hachage sécurisé des mots de passe
- `bcrypt==4.0.1` : Backend pour passlib

## Les 3 piliers de l'authentification
```
1. HACHAGE → Stocker les mots de passe en sécurité
2. JWT → Maintenir la session utilisateur
3. DEPENDENCIES → Protéger les routes
```

## Concept 1 : Hachage de mots de passe
```bash
uvicorn concepts.concepts_01_password_hashing:app --reload
```

**RÈGLE D'OR** : Ne JAMAIS stocker les mots de passe en clair !
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hacher un mot de passe
hashed = pwd_context.hash("secret123")
# → $2b$12$KIXxG7... (impossible à décoder)

# Vérifier un mot de passe
is_valid = pwd_context.verify("secret123", hashed)
# → True
```

**Caractéristiques bcrypt** :
- Chaque hash est unique (même mot de passe)
- Irreversible (impossible de retrouver le mot de passe)
- Lent volontairement (protection contre brute force)

**Testez** :
1. Créer un utilisateur avec mot de passe
2. Voir le hash (illisible)
3. Login avec bon mot de passe → OK
4. Login avec mauvais mot de passe → Erreur

## Concept 2 : JWT (JSON Web Tokens)
```bash
uvicorn concepts.concepts_02_jwt_basics:app --reload
```

**JWT** = Jeton signé contenant des informations (username, expiration).

**Structure d'un JWT** : `header.payload.signature`
```python
from jose import jwt
from datetime import datetime, timedelta

# Créer un token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return token

# Token créé
token = create_access_token({"sub": "alice"})
# → "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Décoder le token
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
# → {"sub": "alice", "exp": 1234567890}
```

**Workflow** :
1. Utilisateur login → Reçoit un token JWT
2. Chaque requête → Envoie le token dans le header
3. Serveur → Vérifie le token, extrait le username

## Concept 3 : Dependency Injection
```bash
uvicorn concepts.concepts_03_dependency_injection:app --reload
```

**Dependency Injection** : Réutiliser du code sur plusieurs routes.
```python
from fastapi import Depends, Header, HTTPException

# Dépendance qui vérifie l'authentification
def get_current_user(authorization: str = Header(None)) -> str:
    if not authorization:
        raise HTTPException(401, "Token manquant")
    
    scheme, token = authorization.split()
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload.get("sub")

# Route protégée
@app.get("/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}
```

**Avantage** : Code écrit une fois, réutilisé partout avec `Depends()`.

## Exercice 1 : API de blog (3 TODO)

**Objectif** : API de blog avec authentification JWT.

**Structure** : Architecture en couches + `auth.py` + `dependencies.py`

**TODO 1** (`auth.py`) : Implémenter les fonctions d'authentification
```python
def hash_password(password: str) -> str:
    # Utiliser pwd_context.hash()
    
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Utiliser pwd_context.verify()
    
def create_access_token(data: dict) -> str:
    # Créer JWT avec expiration 30 minutes
```

**TODO 2** (`dependencies.py`) : Créer la dépendance d'authentification
```python
def get_current_user(authorization: str = Header(None)) -> str:
    # 1. Vérifier header existe
    # 2. Extraire token : scheme, token = authorization.split()
    # 3. Décoder JWT
    # 4. Retourner username
```

**TODO 3** (`main.py`) : Assembler l'application
```python
init_database()
app = FastAPI()
app.include_router(auth_router)
app.include_router(articles_router)
```

**Routes** :
- `POST /auth/register` : Créer un compte
- `POST /auth/login` : Se connecter (obtenir token)
- `GET /articles` : Lister articles (public)
- `POST /articles` : Créer article (protégé)
- `GET /articles/my-articles` : Mes articles (protégé)

**Tester** :
```bash
uvicorn exercises.exercise_01.main:app --reload
pytest tests/test_exercise_01.py -v
```

## Exercice 2 : API de tâches avec rôles (3 TODO)

**Objectif** : API avec 2 rôles (user/admin) et autorisation.

**Rôles** :
- **user** : Créer et voir ses tâches
- **admin** : Voir toutes les tâches et les supprimer

**TODO 1** (`auth.py`) : Identique à exercice 1

**TODO 2** (`dependencies.py`) : 2 dépendances
```python
def get_current_user(authorization: str = Header(None)) -> str:
    # Identique à exercice 1

def require_admin(current_user: str = Depends(get_current_user)) -> str:
    # 1. Récupérer user depuis DB
    # 2. Vérifier role == "admin"
    # 3. Lever HTTPException 403 si non admin
```

**TODO 3** (`main.py`) : Assembler

**Routes utilisateur** :
- `POST /tasks` : Créer tâche
- `GET /tasks/my-tasks` : Mes tâches

**Routes admin** :
- `GET /tasks/all` : Toutes les tâches (admin only)
- `DELETE /tasks/{id}` : Supprimer tâche (admin only)

**Tester** :
```bash
uvicorn exercises.exercise_02.main:app --reload
pytest tests/test_exercise_02.py -v
```

## Format du header Authorization
```
Authorization: Bearer <token>
```

Exemple :
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Workflow complet

**1. Inscription** :
```bash
POST /auth/register
{"username": "alice", "password": "secret123"}
→ {"message": "Utilisateur créé"}
```

**2. Connexion** :
```bash
POST /auth/login
{"username": "alice", "password": "secret123"}
→ {"access_token": "eyJhbG...", "token_type": "bearer"}
```

**3. Utiliser l'API** :
```bash
POST /articles
Headers: Authorization: Bearer eyJhbG...
Body: {"title": "Mon article", "content": "Contenu"}
→ Article créé avec author="alice"
```

## Sécurité : Les bases

**✅ À FAIRE** :
- Hacher tous les mots de passe avec bcrypt
- Utiliser une SECRET_KEY longue et aléatoire
- Définir une expiration sur les tokens (30 min)
- Utiliser HTTPS en production

**❌ À NE PAS FAIRE** :
- Stocker les mots de passe en clair
- Partager la SECRET_KEY
- Créer des tokens sans expiration
- Envoyer des tokens en clair (HTTP)

## Codes HTTP d'authentification

- **401 Unauthorized** : Token manquant ou invalide
- **403 Forbidden** : Token valide mais droits insuffisants

**Exemple** :
```python
# 401 : Pas de token
GET /articles/my-articles
→ 401 "Token manquant"

# 403 : User essaie d'accéder à route admin
GET /tasks/all (en tant que user)
→ 403 "Accès réservé aux administrateurs"
```

## Critères de validation

L'étape est validée quand :
- ✅ Vous comprenez le hachage bcrypt
- ✅ Vous savez créer et vérifier des JWT
- ✅ Vous utilisez Depends() pour protéger les routes
- ✅ Tous les tests de `test_exercise_01.py` passent
- ✅ Tous les tests de `test_exercise_02.py` passent

## Dépannage

### "Token manquant"
Vérifiez le header :
```python
headers = {"Authorization": f"Bearer {token}"}
```

### "Token invalide ou expiré"
- Le token a peut-être expiré (30 min)
- Reconnectez-vous pour obtenir un nouveau token

### "Accès réservé aux administrateurs"
Créez un utilisateur admin :
```python
{"username": "admin", "password": "admin123", "role": "admin"}
```

### ImportError jose
```bash
pip install python-jose[cryptography]
```

## Pour aller plus loin

- Refresh tokens
- OAuth2 / OpenID Connect
- Tokens dans des cookies
- Rate limiting par utilisateur
- Blacklist de tokens révoqués

**Félicitations !** Vous savez maintenant sécuriser une API FastAPI. 🎉