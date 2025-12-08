# Étape 6 : Architecture en Couches

## Objectifs

Cette étape vous apprend à organiser votre code en couches séparées :

- Comprendre les limites d'une architecture monolithique
- Séparer les responsabilités en couches distinctes
- Organiser le code pour faciliter la maintenance et les tests
- Appliquer le principe de séparation des préoccupations

## Prérequis

- Python 3.8 ou supérieur installé
- Avoir validé l'étape 5 (Persistance SQLite)

## Installation
```bash
pip install -r requirements.txt
```

Pas de nouveaux packages, mais une nouvelle organisation du code !

## Les 5 couches de l'architecture
```
┌─────────────────────────────────────┐
│  Routes (routes.py)                 │  ← Points d'entrée HTTP
├─────────────────────────────────────┤
│  Services (services.py)             │  ← Logique métier
├─────────────────────────────────────┤
│  Repositories (repositories.py)     │  ← Accès aux données
├─────────────────────────────────────┤
│  Database (database.py)             │  ← Connexion DB
├─────────────────────────────────────┤
│  Models (models.py)                 │  ← Structures de données
└─────────────────────────────────────┘
```

**Principe** : Chaque couche a une responsabilité unique et ne communique qu'avec la couche adjacente.

## Concept 1 : API Monolithique (le problème)
```bash
uvicorn concepts.concepts_01_monolithic:app --reload
```

**Problèmes de cette approche** :
- Tout le code dans un seul fichier
- Logique métier mélangée avec accès DB et routes
- Difficile à tester unitairement
- Code dupliqué partout
- Impossible à réutiliser

**Testez** : Créez quelques produits et observez le code répétitif.

## Concept 2 : Architecture en Couches (la solution)
```bash
uvicorn concepts.concepts_02_layered.main:app --reload
```

**Organisation** :
```
concepts_02_layered/
├── main.py          # Point d'entrée
├── models.py        # Modèles Pydantic
├── database.py      # Connexion DB
├── repositories.py  # Requêtes SQL
├── services.py      # Logique métier
└── routes.py        # Routes FastAPI
```

### Rôle de chaque couche

**models.py** : Structures de données
```python
class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int
```

**database.py** : Gestion de la connexion
```python
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
```

**repositories.py** : Accès aux données (SQL uniquement)
```python
class ProductRepository:
    @staticmethod
    def create(name: str, price: float, stock: int) -> int:
        conn = get_db_connection()
        cursor.execute("INSERT INTO products ...")
        return cursor.lastrowid
```

**services.py** : Logique métier
```python
class ProductService:
    @staticmethod
    def create_product(product_data: ProductCreate) -> ProductResponse:
        # Vérifier si existe déjà (logique métier)
        if ProductRepository.get_by_name(product_data.name):
            raise HTTPException(400, "Produit existe déjà")
        # Créer via repository
        product_id = ProductRepository.create(...)
        return ProductResponse(...)
```

**routes.py** : Points d'entrée HTTP
```python
@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate):
    return ProductService.create_product(product)
```

**main.py** : Assemblage
```python
from .database import init_database
from .routes import router

init_database()
app = FastAPI()
app.include_router(router)
```

**Testez** : L'API fait exactement la même chose, mais le code est organisé !

## Exercice 1 : API de notes d'étudiants (5 TODO)

**Objectif** : Créer une API de gestion de notes avec architecture en couches.

**Structure** :
```
exercises/exercise_01/
├── main.py
├── models.py        # TODO 1: NoteCreate et NoteResponse
├── database.py      # Fourni (table notes)
├── repositories.py  # TODO 2: create, get_by_id, get_all
├── services.py      # TODO 3: logique métier (calcul passed)
└── routes.py        # TODO 4: POST, GET /notes
```

**Logique métier** : Calculer `passed = (grade >= 10)`

**TODO** :
1. **models.py** : Créer `NoteCreate` (student_name, subject, grade) et `NoteResponse` (+ id, passed)
2. **repositories.py** : Implémenter les 3 méthodes d'accès aux données
3. **services.py** : Créer les méthodes avec calcul de `passed`
4. **routes.py** : Créer les 3 routes (POST, GET all, GET by id)
5. **main.py** : Assembler l'application

**Tester** :
```bash
uvicorn exercises.exercise_01.main:app --reload
pytest tests/test_exercise_01.py -v
```

## Exercice 2 : API de tâches avec priorités (5 TODO)

**Objectif** : Créer une API de tâches avec calcul de label de priorité.

**Structure** : Même organisation que l'exercice 1

**Logique métier** : Calculer `priority_label` :
- 1-2 → "Basse"
- 3 → "Moyenne"  
- 4-5 → "Haute"

**TODO** :
1. **models.py** : Créer `TaskCreate` et `TaskResponse` (avec priority_label)
2. **repositories.py** : create, get_by_id, get_all, mark_completed
3. **services.py** : Méthodes avec calcul de priority_label
4. **routes.py** : 4 routes (POST, GET all, GET by id, PUT complete)
5. **main.py** : Assembler l'application

**Tester** :
```bash
uvicorn exercises.exercise_02.main:app --reload
pytest tests/test_exercise_02.py -v
```

## Avantages de l'architecture en couches

✅ **Maintenabilité** : Chaque fichier a une responsabilité claire  
✅ **Testabilité** : Chaque couche peut être testée indépendamment  
✅ **Réutilisabilité** : Les services peuvent être appelés depuis plusieurs routes  
✅ **Évolutivité** : Facile d'ajouter de nouvelles fonctionnalités  
✅ **Collaboration** : Plusieurs développeurs peuvent travailler sur des couches différentes  

## Pattern de communication entre couches
```
Route → Service → Repository → Database
  ↓        ↓          ↓
Valide   Logique   Accès
HTTP     métier    données
```

**Règle d'or** : Une couche ne peut appeler que la couche directement en dessous.

❌ **Mauvais** : Route appelle directement Repository  
✅ **Bon** : Route → Service → Repository

## Quand utiliser quelle couche ?

**Repository** : Manipulation de données brutes
```python
# Juste des requêtes SQL, pas de logique
def get_by_id(product_id: int) -> dict | None:
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    return dict(row) if row else None
```

**Service** : Règles métier et orchestration
```python
# Validation métier, calculs, orchestration
def sell_product(product_id: int, quantity: int):
    product = ProductRepository.get_by_id(product_id)
    if product["stock"] < quantity:  # ← Logique métier
        raise HTTPException(400, "Stock insuffisant")
    new_stock = product["stock"] - quantity
    ProductRepository.update_stock(product_id, new_stock)
```

**Route** : Simple délégation
```python
# Juste recevoir et déléguer
@router.put("/{product_id}/sell")
def sell_product(product_id: int, quantity: int):
    return ProductService.sell_product(product_id, quantity)
```

## Critères de validation

L'étape est validée quand :
- ✅ Vous comprenez le problème du code monolithique
- ✅ Vous savez quel code va dans quelle couche
- ✅ Tous les tests de `test_exercise_01.py` passent
- ✅ Tous les tests de `test_exercise_02.py` passent
- ✅ Votre code respecte la séparation des responsabilités

## Erreurs courantes

### Mettre de la logique métier dans les routes
```python
# ❌ MAUVAIS
@router.post("/products")
def create_product(product: ProductCreate):
    if ProductRepository.get_by_name(product.name):  # ← Logique dans route
        raise HTTPException(400, "Existe déjà")
    return ProductRepository.create(...)

# ✅ BON
@router.post("/products")
def create_product(product: ProductCreate):
    return ProductService.create_product(product)  # ← Délégation
```

### Mettre du SQL dans les services
```python
# ❌ MAUVAIS - SQL dans le service
def get_product(product_id: int):
    cursor.execute("SELECT * FROM products...")  # ← SQL dans service

# ✅ BON - Utiliser le repository
def get_product(product_id: int):
    product = ProductRepository.get_by_id(product_id)  # ← Via repository
```

## Dépannage

### ImportError avec les modules
- Vérifiez les fichiers `__init__.py` dans chaque dossier
- Utilisez des imports relatifs : `from .database import ...`

### "Module has no attribute 'app'"
- Vérifiez que `main.py` crée bien l'objet `app`
- Lancez depuis la racine : `uvicorn exercises.exercise_01.main:app`

## Pour aller plus loin

- Dependency Injection FastAPI
- Tests unitaires par couche
- Architecture hexagonale
- Domain-Driven Design (DDD)

**Prochaine étape** : Gestion des erreurs.