# 🚀 Guide de Démarrage - Premières Actions

Ce guide vous accompagne dans les toutes premières étapes du projet pour bien démarrer.

## Étape 1 : Vérifier l'installation

### 1.1 Installer les dépendances
```bash
pip install -r requirements.txt
```

### 1.2 Vérifier que tout fonctionne
```bash
python -c "import fastapi, pydantic, sqlite3; print('✅ Tout est installé')"
```

Si vous voyez "✅ Tout est installé", vous êtes prêt !

---

## Étape 2 : Comprendre la structure du projet
```
mini-projet/
├── app/                      # Votre code source
│   ├── main.py              # Point d'entrée de l'API
│   ├── config.py            # Configuration (chemin DB, etc.)
│   ├── models.py            # Modèles Pydantic
│   ├── database.py          # Connexion et initialisation DB
│   ├── repositories.py      # Accès aux données (SQL)
│   ├── services.py          # Logique métier
│   ├── routes.py            # Endpoints de l'API
│   └── exceptions.py        # Exceptions personnalisées
├── data/
│   └── initial_characters.json  # 10 personnages de départ
├── tests/
│   └── test_characters.py   # Tests à compléter
└── databases/               # Base SQLite (créée automatiquement)
```

**Principe de l'architecture en couches** (rappel étape 6) :
- **Routes** : Reçoit les requêtes HTTP → Appelle le service → Retourne la réponse
- **Services** : Logique métier (validation, calculs) → Appelle le repository
- **Repositories** : Accès aux données (requêtes SQL) → Retourne des données brutes
- **Database** : Connexion et initialisation de la base de données

---

## Étape 3 : Créer le modèle de données (models.py)

### 3.1 Ouvrir `app/models.py`

Ce fichier contient des TODO. Voici ce que vous devez faire :

### 3.2 Créer le modèle `CharacterBase`
```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CharacterBase(BaseModel):
    """Modèle de base pour un personnage."""
    name: str = Field(..., min_length=2, description="Nom du personnage")
    character_class: str = Field(..., alias="class", description="Classe du personnage")
    level: int = Field(..., ge=1, le=100, description="Niveau du personnage")
    health_points: int = Field(..., ge=50, le=500, description="Points de vie")
    attack: int = Field(..., ge=10, le=100, description="Points d'attaque")
    defense: int = Field(..., ge=5, le=50, description="Points de défense")
    speed: int = Field(..., ge=10, le=100, description="Vitesse")
    special_ability: Optional[str] = Field(None, description="Capacité spéciale")
    image_url: Optional[str] = Field(None, description="URL de l'image")
```

**Note importante** : On utilise `alias="class"` car `class` est un mot-clé Python.

### 3.3 Créer les autres modèles
```python
class CharacterCreate(CharacterBase):
    """Modèle pour créer un personnage."""
    pass  # Hérite de CharacterBase

class CharacterUpdate(BaseModel):
    """Modèle pour modifier un personnage (tous les champs optionnels)."""
    name: Optional[str] = Field(None, min_length=2)
    character_class: Optional[str] = Field(None, alias="class")
    level: Optional[int] = Field(None, ge=1, le=100)
    health_points: Optional[int] = Field(None, ge=50, le=500)
    attack: Optional[int] = Field(None, ge=10, le=100)
    defense: Optional[int] = Field(None, ge=5, le=50)
    speed: Optional[int] = Field(None, ge=10, le=100)
    special_ability: Optional[str] = None
    image_url: Optional[str] = None

class CharacterResponse(CharacterBase):
    """Modèle de réponse pour un personnage."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True  # Pour compatibilité avec SQLite Row
```

---

## Étape 4 : Configurer la base de données (database.py)

### 4.1 Ouvrir `app/database.py`

### 4.2 Créer la fonction de connexion
```python
import sqlite3
import json
from pathlib import Path

DATABASE_PATH = "databases/characters.db"

def get_db_connection():
    """Crée une connexion à la base de données."""
    # Créer le dossier databases s'il n'existe pas
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
    return conn
```

### 4.3 Créer la table des personnages
```python
def init_database():
    """Initialise la base de données et charge les données initiales."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Créer la table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class TEXT NOT NULL,
            level INTEGER NOT NULL,
            health_points INTEGER NOT NULL,
            attack INTEGER NOT NULL,
            defense INTEGER NOT NULL,
            speed INTEGER NOT NULL,
            special_ability TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Vérifier si la table est vide
    cursor.execute("SELECT COUNT(*) FROM characters")
    count = cursor.fetchone()[0]
    
    # Si vide, charger les données initiales
    if count == 0:
        load_initial_data(cursor)
    
    conn.commit()
    conn.close()

def load_initial_data(cursor):
    """Charge les 10 personnages depuis initial_characters.json."""
    with open("data/initial_characters.json", "r", encoding="utf-8") as f:
        characters = json.load(f)
    
    for char in characters:
        cursor.execute("""
            INSERT INTO characters (name, class, level, health_points, attack, defense, speed, special_ability, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            char["name"],
            char["class"],
            char["level"],
            char["health_points"],
            char["attack"],
            char["defense"],
            char["speed"],
            char.get("special_ability"),
            char.get("image_url")
        ))
```

---

## Étape 5 : Lancer l'application pour la première fois

### 5.1 Compléter `app/main.py`
```python
from fastapi import FastAPI
from app.database import init_database
from app.routes import router

# Initialiser la base de données
init_database()

# Créer l'application
app = FastAPI(
    title="API Gestion de Personnages",
    description="API pour gérer des personnages de jeu vidéo",
    version="1.0.0"
)

# Inclure les routes
app.include_router(router)

@app.get("/")
def root():
    """Route racine."""
    return {
        "message": "API de gestion de personnages de jeu vidéo",
        "documentation": "/docs"
    }
```

### 5.2 Lancer l'application
```bash
uvicorn app.main:app --reload
```

### 5.3 Vérifier dans le navigateur

Ouvrez : http://localhost:8000

Vous devriez voir :
```json
{
  "message": "API de gestion de personnages de jeu vidéo",
  "documentation": "/docs"
}
```

Ouvrez aussi : http://localhost:8000/docs

Vous verrez la documentation interactive (même si les routes ne sont pas encore créées).

---

## Étape 6 : Créer votre premier endpoint (GET /characters)

### 6.1 Dans `app/repositories.py`

Créez la méthode pour récupérer tous les personnages :
```python
from app.database import get_db_connection

class CharacterRepository:
    """Repository pour l'accès aux données des personnages."""
    
    @staticmethod
    def get_all() -> list[dict]:
        """Récupère tous les personnages."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM characters ORDER BY id")
        rows = cursor.fetchall()
        
        conn.close()
        
        return [dict(row) for row in rows]
```

### 6.2 Dans `app/services.py`

Créez le service correspondant :
```python
from app.repositories import CharacterRepository
from app.models import CharacterResponse

class CharacterService:
    """Service pour la logique métier des personnages."""
    
    @staticmethod
    def get_all_characters() -> list[CharacterResponse]:
        """Récupère tous les personnages."""
        characters = CharacterRepository.get_all()
        
        # Convertir les dict en modèles Pydantic
        return [
            CharacterResponse(
                id=char["id"],
                name=char["name"],
                character_class=char["class"],  # Attention : "class" dans la DB
                level=char["level"],
                health_points=char["health_points"],
                attack=char["attack"],
                defense=char["defense"],
                speed=char["speed"],
                special_ability=char["special_ability"],
                image_url=char["image_url"],
                created_at=char["created_at"]
            )
            for char in characters
        ]
```

### 6.3 Dans `app/routes.py`

Créez la route :
```python
from fastapi import APIRouter
from app.models import CharacterResponse
from app.services import CharacterService

router = APIRouter(prefix="/characters", tags=["characters"])

@router.get("", response_model=list[CharacterResponse])
def get_all_characters():
    """Récupère tous les personnages."""
    return CharacterService.get_all_characters()
```

### 6.4 Tester

Relancez l'application (elle devrait se recharger automatiquement avec --reload).

Allez sur http://localhost:8000/docs et testez GET /characters

Vous devriez voir vos 10 personnages ! 🎉

---

## ✅ Checkpoint

À ce stade, vous devriez avoir :
- ✅ L'application qui démarre sans erreur
- ✅ La base de données créée avec 10 personnages
- ✅ L'endpoint GET /characters fonctionnel
- ✅ La documentation interactive accessible

## 🚀 Prochaines étapes

Maintenant que vous avez compris le principe, continuez avec :

1. **POST /characters** : Créer un personnage
   - Repository : `create()`
   - Service : validation + création
   - Route : `@router.post()`

2. **GET /characters/{id}** : Récupérer un personnage
   - Repository : `get_by_id()`
   - Service : gérer le cas "non trouvé"
   - Route : `@router.get("/{id}")`

3. **PUT /characters/{id}** : Modifier un personnage
   - Repository : `update()`
   - Service : logique de mise à jour partielle
   - Route : `@router.put("/{id}")`

4. **DELETE /characters/{id}** : Supprimer un personnage
   - Repository : `delete()`
   - Service : vérifier existence
   - Route : `@router.delete("/{id}")`

**Conseil** : Créez les 3 méthodes (repository, service, route) pour chaque endpoint avant de passer au suivant.

## 💡 Rappel important

**Séparation des responsabilités** :
- ❌ Ne mettez PAS de SQL dans les services
- ❌ Ne mettez PAS de logique métier dans les repositories
- ❌ Ne mettez PAS de logique dans les routes (juste appeler le service)

**Testez au fur et à mesure** :
- Utilisez `/docs` pour tester vos endpoints
- Écrivez les tests dans `tests/test_characters.py`

---

**Vous êtes prêt à coder ! Bon courage ! 💪**