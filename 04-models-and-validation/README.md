# Étape 4 : Modèles et Validation Pydantic

## Objectifs

Cette étape vous permet de maîtriser la validation des données avec Pydantic :

- Créer des modèles Pydantic avec validation automatique
- Utiliser des contraintes sur les champs (min, max, longueur)
- Créer des modèles imbriqués
- Utiliser les response_model pour filtrer les données
- Gérer les erreurs avec HTTPException

## Prérequis

- Python 3.8 ou supérieur installé
- Avoir validé l'étape 3 (Méthodes HTTP)

## Installation
```bash
pip install -r requirements.txt
```

Nouveaux packages :
- `pydantic` : Validation des données
- `email-validator` : Validation des emails

## Structure du dossier
```
04-models-and-validation/
├── concepts/
│   ├── concepts_01_basic_models.py        # Modèles de base
│   ├── concepts_02_field_validation.py    # Validation des champs
│   ├── concepts_03_nested_models.py       # Modèles imbriqués
│   └── concepts_04_response_models.py     # Filtrage des réponses
├── exercises/
│   ├── exercise_01.py                     # Exercice 1 : Étudiants
│   └── exercise_02.py                     # Exercice 2 : Bibliothèque
└── tests/
    ├── test_concepts.py
    ├── test_exercise_01.py
    └── test_exercise_02.py
```

## Découvrir les concepts

### Concept 1 : Modèles de base
```bash
uvicorn concepts.concepts_01_basic_models:app --reload
```

**Ce que vous allez apprendre** :
- Créer des modèles Pydantic simples
- Utiliser des valeurs par défaut
- Rendre des champs optionnels avec `Optional`

**Testez dans Swagger** :
- Créez un livre avec tous les champs obligatoires
- Créez un livre en omettant les champs optionnels
- Essayez de créer un livre sans champ obligatoire → Erreur 422

### Concept 2 : Validation des champs
```bash
uvicorn concepts.concepts_02_field_validation:app --reload
```

**Ce que vous allez apprendre** :
- Utiliser `Field()` pour ajouter des contraintes
- Valider les emails avec `EmailStr`
- Créer des validateurs personnalisés avec `@field_validator`

**Contraintes disponibles** :
```python
age: int = Field(..., ge=16, le=100)      # Entre 16 et 100
name: str = Field(..., min_length=3)      # Min 3 caractères
price: float = Field(..., gt=0)           # Strictement positif
```

**Testez dans Swagger** :
- Essayez un username de 2 caractères → Erreur 422
- Essayez un email invalide "test" → Erreur 422
- Essayez un âge de 150 → Erreur 422

### Concept 3 : Modèles imbriqués
```bash
uvicorn concepts.concepts_03_nested_models:app --reload
```

**Ce que vous allez apprendre** :
- Imbriquer des modèles dans d'autres modèles
- Valider automatiquement toute la structure

**Exemple** :
```python
class Address(BaseModel):
    street: str
    city: str

class Customer(BaseModel):
    name: str
    address: Address  # Modèle imbriqué
```

### Concept 4 : Response models
```bash
uvicorn concepts.concepts_04_response_models:app --reload
```

**Ce que vous allez apprendre** :
- Utiliser `response_model` pour filtrer les données sensibles
- Ajouter des champs calculés dans les réponses

**Important** : Le `response_model` permet de masquer automatiquement des données (comme les mots de passe) dans la réponse.

## Exercice 1 : Gestion d'étudiants (5 TODO)

**Objectif** : Créer une API avec validation avancée pour gérer des étudiants.

**Ouvrez** `exercises/exercise_01.py`

**Modèles à créer** :
- `StudentCreate` : avec validation (prénom ≥2 car, email, âge 16-100, note 0-20)
- `StudentResponse` : avec un champ calculé "status" (Admis/Refusé)

**Routes à implémenter** :
1. `POST /students` : Créer un étudiant (calculer le status)
2. `GET /students` : Liste tous les étudiants
3. `GET /students/{id}` : Récupérer un étudiant (404 si non trouvé)

**Tester** :
```bash
uvicorn exercises.exercise_01:app --reload
pytest tests/test_exercise_01.py -v
```

## Exercice 2 : Bibliothèque (5 TODO)

**Objectif** : Créer une API de bibliothèque avec emprunts de livres.

**Ouvrez** `exercises/exercise_02.py`

**Modèles à créer** :
- `BookCreate` / `BookResponse` : Livre avec ISBN de 13 caractères
- `MemberCreate` / `MemberResponse` : Membre de la bibliothèque
- `LoanCreate` / `LoanResponse` : Emprunt d'un livre

**Routes à implémenter** :
1. `POST /books` et `POST /members` : Créer livre/membre
2. `POST /loans` : Emprunter un livre (vérifier disponibilité)
3. `PUT /loans/{id}/return` : Retourner un livre

**Tester** :
```bash
uvicorn exercises.exercise_02:app --reload
pytest tests/test_exercise_02.py -v
```

## Concepts clés

### Créer un modèle avec validation
```python
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    age: int = Field(..., ge=18, le=120)
```

### Validation automatique

Pydantic valide automatiquement :
- Les types (str, int, float, bool)
- Les contraintes (min, max, longueur)
- Les formats spéciaux (email)
- Retourne une erreur 422 si invalide

### Gérer les erreurs avec HTTPException
```python
from fastapi import HTTPException, status

# Au lieu de retourner {"error": "..."}
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Ressource non trouvée"
)
```

### Response model
```python
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    # Le response_model filtre automatiquement les champs
    return user_with_password  # Le password ne sera pas retourné
```

## Contraintes Field disponibles

| Contrainte | Usage | Exemple |
|------------|-------|---------|
| `min_length` | Longueur minimale (str) | `Field(..., min_length=3)` |
| `max_length` | Longueur maximale (str) | `Field(..., max_length=20)` |
| `ge` | Greater or equal (≥) | `Field(..., ge=0)` |
| `gt` | Greater than (>) | `Field(..., gt=0)` |
| `le` | Less or equal (≤) | `Field(..., le=100)` |
| `lt` | Less than (<) | `Field(..., lt=100)` |

## Critères de validation

L'étape est validée quand :
- ✅ Vous avez testé les 4 concepts dans Swagger
- ✅ Tous les tests de `test_exercise_01.py` passent
- ✅ Tous les tests de `test_exercise_02.py` passent
- ✅ Vous utilisez HTTPException pour les erreurs
- ✅ Vous comprenez la validation automatique de Pydantic

## Différence entre return et raise
```python
# ❌ MAUVAIS - Ne fonctionne pas avec response_model
@app.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, response: Response):
    if not found:
        response.status_code = 404
        return {"error": "Non trouvé"}  # ❌ Erreur de validation
    return user

# ✅ BON - Utiliser HTTPException
@app.get("/users/{id}", response_model=UserResponse)
def get_user(id: int):
    if not found:
        raise HTTPException(status_code=404, detail="Non trouvé")
    return user
```

## Dépannage

### Erreur "Field required"
- Vérifiez que tous les champs obligatoires sont fournis
- Les champs sans valeur par défaut sont obligatoires

### Erreur de validation (422)
- Lisez le détail de l'erreur dans la réponse JSON
- Vérifiez les types et les contraintes

### email-validator non installé
```bash
pip install email-validator
```

## Pour aller plus loin

- Validateurs personnalisés complexes
- Modèles avec héritage
- Configuration des modèles Pydantic
- Validation de données complexes (JSON, dates)

**Prochaine étape** : Persistance avec SQLite et architecture en couches