# Étape 2 : FastAPI Essentials

## Objectifs

Cette étape vous permet de découvrir FastAPI et ses fonctionnalités de base :

- Créer une application FastAPI
- Définir des routes GET simples
- Utiliser les paramètres de chemin (path parameters)
- Utiliser les paramètres de requête (query parameters)
- Découvrir la documentation automatique avec Swagger UI et ReDoc
- Tester une API avec pytest et TestClient

## Prérequis

- Python 3.8 ou supérieur installé
- Avoir validé l'étape 1 (Fondations Python)

## Installation

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

Les packages installés :
- `fastapi` : Framework web pour créer des API
- `uvicorn` : Serveur ASGI pour exécuter FastAPI
- `pytest` : Framework de tests
- `httpx` : Client HTTP pour les tests (requis par TestClient)

## Structure du dossier
```
02-fastapi-essentials/
├── concepts/
│   ├── concepts_01_hello_world.py         # Première API simple
│   ├── concepts_02_path_parameters.py     # Paramètres de chemin
│   └── concepts_03_query_parameters.py    # Paramètres de requête
├── exercises/
│   ├── exercise_01.py                     # Exercice 1 : API de tâches
│   └── exercise_02.py                     # Exercice 2 : Calculatrice
├── tests/
│   ├── test_concepts.py                   # Tests des concepts
│   ├── test_exercise_01.py                # Tests exercice 1
│   └── test_exercise_02.py                # Tests exercice 2
├── requirements.txt                        # Dépendances Python
└── README.md                              # Ce fichier
```

## Étapes de travail

### 1. Découvrir les concepts

#### Concept 1 : Hello World

Lisez le fichier `concepts/concepts_01_hello_world.py` puis lancez le serveur :
```bash
uvicorn concepts.concepts_01_hello_world:app --reload
```

Ouvrez dans votre navigateur :
- **http://127.0.0.1:8000** : Tester l'API
- **http://127.0.0.1:8000/docs** : Documentation Swagger UI (interactive)
- **http://127.0.0.1:8000/redoc** : Documentation ReDoc (lecture)

**Point d'attention** : Vous ne verrez PAS de section "Schemas" dans Swagger car aucune route n'a de paramètres nécessitant validation.

Arrêtez le serveur avec `Ctrl+C` avant de passer au concept suivant.

#### Concept 2 : Paramètres de chemin

Lisez le fichier `concepts/concepts_02_path_parameters.py` puis lancez :
```bash
uvicorn concepts.concepts_02_path_parameters:app --reload
```

Testez les routes :
- http://127.0.0.1:8000/users/123
- http://127.0.0.1:8000/products/5
- http://127.0.0.1:8000/items/laptop

**Point d'attention** : Vous verrez maintenant une section "Schemas" dans Swagger ! C'est normal, FastAPI génère automatiquement des schémas de validation pour les erreurs.

**Expérience** : Dans Swagger, essayez `/users/abc` au lieu d'un nombre → Erreur 422 avec détails de validation !

#### Concept 3 : Paramètres de requête

Lisez le fichier `concepts/concepts_03_query_parameters.py` puis lancez :
```bash
uvicorn concepts.concepts_03_query_parameters:app --reload
```

Testez les routes :
- http://127.0.0.1:8000/search?query=laptop&limit=5
- http://127.0.0.1:8000/products?category=electronics&min_price=100
- http://127.0.0.1:8000/calculate?a=10&b=5&operation=multiply

**Différences avec path parameters** :
- Les query parameters apparaissent après le `?` dans l'URL
- Ils peuvent avoir des valeurs par défaut
- Ils peuvent être optionnels

### 2. Exécuter les tests des concepts

Vérifiez votre compréhension en lançant les tests :
```bash
pytest tests/test_concepts.py -v
```

Tous les tests doivent passer ✅

### 3. Compléter l'exercice 1 : API de gestion de tâches

**Objectif** : Créer une API simple pour gérer des tâches.

Ouvrez `exercises/exercise_01.py` et complétez les TODO.

**Routes à implémenter** :
- `GET /` : Message de bienvenue
- `GET /tasks` : Liste de toutes les tâches
- `GET /tasks/search?status=all` : Recherche avec filtre
- `GET /tasks/{task_id}` : Récupérer une tâche par ID

**⚠️ IMPORTANT - Ordre des routes** :
```python
# ✅ BON ORDRE
@app.get("/tasks/search")  # Route fixe EN PREMIER
@app.get("/tasks/{task_id}")  # Route avec paramètre APRÈS

# ❌ MAUVAIS ORDRE
@app.get("/tasks/{task_id}")  # FastAPI matchera "search" comme un task_id
@app.get("/tasks/search")  # Cette route ne sera jamais atteinte !
```

**Tester votre code** :
```bash
# Lancer le serveur
uvicorn exercises.exercise_01:app --reload

# Dans un autre terminal, lancer les tests
pytest tests/test_exercise_01.py -v
```

### 4. Compléter l'exercice 2 : API calculatrice

**Objectif** : Créer une API de calculatrice avec différentes opérations.

Ouvrez `exercises/exercise_02.py` et complétez les TODO.

**Routes à implémenter** :
- `GET /` : Informations sur l'API
- `GET /calculate/{operation}?a=10&b=5` : Calcul selon l'opération
- `GET /square/{number}` : Carré d'un nombre

**Opérations supportées** : add, subtract, multiply, divide, power

**Gestion d'erreur** : Pour la division par zéro, retourner :
```json
{
  "operation": "divide",
  "a": 10,
  "b": 0,
  "result": null,
  "error": "Division par zéro"
}
```

**Tester votre code** :
```bash
# Lancer le serveur
uvicorn exercises.exercise_02:app --reload

# Dans un autre terminal, lancer les tests
pytest tests/test_exercise_02.py -v
```

## Commandes utiles

### Lancer un serveur FastAPI
```bash
# Format général
uvicorn chemin.vers.module:app --reload

# Exemples
uvicorn concepts.concepts_01_hello_world:app --reload
uvicorn exercises.exercise_01:app --reload

# Options utiles
--reload          # Rechargement automatique lors des modifications
--port 8001       # Changer le port (par défaut 8000)
--host 0.0.0.0    # Accessible depuis d'autres machines
```

### Tester avec pytest
```bash
# Tous les tests de l'étape
pytest tests/ -v

# Un fichier de test spécifique
pytest tests/test_exercise_01.py -v

# Un test spécifique
pytest tests/test_exercise_01.py::test_root -v

# Avec affichage des print()
pytest tests/ -v -s

# Arrêter au premier échec
pytest tests/ -v -x
```

## URLs importantes

Une fois un serveur FastAPI lancé :
- **http://127.0.0.1:8000** : L'API elle-même
- **http://127.0.0.1:8000/docs** : Documentation Swagger UI (interactive, pour tester)
- **http://127.0.0.1:8000/redoc** : Documentation ReDoc (lecture, style moderne)
- **http://127.0.0.1:8000/openapi.json** : Schéma OpenAPI brut

## Critères de validation

L'étape est validée quand :
- ✅ Vous avez exploré les 3 concepts et testé dans Swagger
- ✅ Tous les tests de `test_exercise_01.py` passent
- ✅ Tous les tests de `test_exercise_02.py` passent
- ✅ Vous comprenez la différence entre path et query parameters
- ✅ Vous comprenez l'importance de l'ordre des routes

## Concepts clés à retenir

### Créer une application FastAPI
```python
from fastapi import FastAPI

app = FastAPI(
    title="Mon API",
    description="Description de l'API",
    version="1.0.0"
)
```

### Définir une route
```python
@app.get("/endpoint")
def ma_fonction():
    return {"message": "Hello"}
```

### Path parameters (dans l'URL)
```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

### Query parameters (après le ?)
```python
@app.get("/search")
def search(query: str, limit: int = 10):
    return {"query": query, "limit": limit}
```

### Documentation automatique
FastAPI génère automatiquement :
- Swagger UI (`/docs`) : documentation interactive
- ReDoc (`/redoc`) : documentation moderne en lecture seule
- Schéma OpenAPI (`/openapi.json`)

### Validation automatique
FastAPI valide automatiquement les types et génère des erreurs 422 si :
- Un path parameter n'est pas du bon type
- Un query parameter obligatoire est manquant
- Un query parameter n'est pas du bon type

## Dépannage

### Le serveur ne démarre pas
```bash
# Vérifier que les dépendances sont installées
pip list | grep fastapi
pip list | grep uvicorn

# Réinstaller si nécessaire
pip install -r requirements.txt
```

### Port 8000 déjà utilisé
```bash
# Utiliser un autre port
uvicorn exercises.exercise_01:app --reload --port 8001
```

### Les tests échouent
```bash
# Vérifier que httpx est installé (requis pour TestClient)
pip install httpx

# Lancer les tests avec plus de détails
pytest tests/test_exercise_01.py -v -s
```

### Erreur 422 inattendue
- Vérifiez les types de vos paramètres
- Vérifiez l'ordre de vos routes (routes fixes avant routes avec paramètres)
- Consultez les détails de l'erreur dans la réponse JSON

## Pour aller plus loin

Une fois cette étape validée, vous pouvez explorer :
- La documentation FastAPI : https://fastapi.tiangolo.com/
- Les différents types de paramètres : Path, Query, Body
- Les codes de statut HTTP : 200, 404, 422, 500...
- Les méthodes HTTP : GET, POST, PUT, DELETE

**Prochaine étape** : Routes et méthodes HTTP avec validation Pydantic