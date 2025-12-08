# Étape 5 : Persistance des Données avec SQLite

## Objectifs

Cette étape vous permet de persister vos données dans une base SQLite :

- Utiliser SQLite avec Python (module `sqlite3`)
- Créer et initialiser une base de données
- Effectuer les opérations CRUD (Create, Read, Update, Delete)
- Intégrer SQLite avec FastAPI et Pydantic
- Gérer les connexions à la base de données

## Prérequis

- Python 3.8 ou supérieur installé
- Avoir validé l'étape 4 (Modèles et Validation)

## Installation
```bash
pip install -r requirements.txt
```

**Nouveau** : SQLite est inclus nativement dans Python, pas de package supplémentaire !

## Structure du dossier
```
05-data-storage/
├── concepts/
│   ├── concepts_01_sqlite_basics.py       # Bases SQLite
│   ├── concepts_02_crud_operations.py     # Opérations CRUD
│   └── concepts_03_fastapi_integration.py # Intégration complète
├── exercises/
│   ├── exercise_01.py                     # Exercice 1 : Contacts
│   └── exercise_02.py                     # Exercice 2 : Blog
├── tests/
├── databases/                              # Dossier des fichiers .db
└── requirements.txt
```

**Important** : Créez le dossier `databases/` manuellement avant de commencer.

## Découvrir les concepts

### Concept 1 : Bases de SQLite
```bash
uvicorn concepts.concepts_01_sqlite_basics:app --reload
```

**Ce que vous allez apprendre** :
- Créer une base de données SQLite
- Créer une table avec `CREATE TABLE IF NOT EXISTS`
- Insérer des données avec `INSERT`
- Lire des données avec `SELECT`

**Commandes SQLite de base** :
```python
conn = sqlite3.connect("ma_base.db")  # Ouvre/crée la base
cursor = conn.cursor()                 # Créer un curseur
cursor.execute("SELECT ...")           # Exécuter une requête
conn.commit()                          # Valider les changements
conn.close()                           # Fermer la connexion
```

**Testez dans Swagger** :
1. `GET /products/count` → 0 produits
2. `POST /products/create?name=Laptop&price=999.99&stock=5`
3. `GET /products/count` → 1 produit
4. `GET /products/all` → Liste le produit

**Note** : Le fichier `databases/concepts_01.db` est créé automatiquement.

### Concept 2 : Opérations CRUD
```bash
uvicorn concepts.concepts_02_crud_operations:app --reload
```

**Ce que vous allez apprendre** :
- **CREATE** : `INSERT INTO table VALUES (...)`
- **READ** : `SELECT * FROM table WHERE ...`
- **UPDATE** : `UPDATE table SET ... WHERE ...`
- **DELETE** : `DELETE FROM table WHERE ...`
- Gérer les erreurs (contraintes, non trouvé)

**Astuce SQL** : Utiliser `?` pour les paramètres (protection contre les injections SQL) :
```python
cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
```

**Testez dans Swagger** : Créez, listez, modifiez et supprimez des utilisateurs.

### Concept 3 : Intégration FastAPI
```bash
uvicorn concepts.concepts_03_fastapi_integration:app --reload
```

**Ce que vous allez apprendre** :
- Fonction utilitaire `get_db_connection()`
- Intégration avec `response_model`
- Conversion SQLite ↔ Pydantic
- Gestion des booléens SQLite (0/1)

**Pattern recommandé** :
```python
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Pour avoir des dictionnaires
    return conn

@app.get("/items", response_model=list[ItemResponse])
def get_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    conn.close()
    return [ItemResponse(**dict(row)) for row in rows]
```

## Exercice 1 : API de contacts (5 TODO)

**Objectif** : Créer une API pour gérer des contacts avec SQLite.

**Ouvrez** `exercises/exercise_01.py`

**Table à créer** : `contacts(id, name, email, phone)`

**TODO** :
1. Créer la fonction `init_database()` avec la table
2. Créer les modèles `ContactCreate` et `ContactResponse`
3. `POST /contacts` : Créer un contact
4. `GET /contacts` : Lister tous les contacts
5. `DELETE /contacts/{id}` : Supprimer un contact

**Tester** :
```bash
uvicorn exercises.exercise_01:app --reload
pytest tests/test_exercise_01.py -v
```

## Exercice 2 : API de blog (5 TODO)

**Objectif** : Créer une API de blog avec articles et publication.

**Ouvrez** `exercises/exercise_02.py`

**Table à créer** : `articles(id, title, content, author, published, created_at)`

**TODO** :
1. Créer la fonction `init_database()` avec la table
2. Créer les modèles `ArticleCreate` et `ArticleResponse`
3. `POST /articles` : Créer un article (published=False par défaut)
4. `GET /articles/{id}` : Récupérer un article
5. `PUT /articles/{id}/publish` : Publier un article (published=True)

**Tester** :
```bash
uvicorn exercises.exercise_02:app --reload
pytest tests/test_exercise_02.py -v
```

## Concepts clés

### Créer une table
```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        active INTEGER DEFAULT 1
    )
""")
```

### Types SQLite

| Type SQLite | Type Python | Usage |
|-------------|-------------|-------|
| `INTEGER` | `int` | Nombres entiers |
| `REAL` | `float` | Nombres décimaux |
| `TEXT` | `str` | Texte |
| `INTEGER` | `bool` | Booléens (0=False, 1=True) |

### Opérations CRUD
```python
# CREATE
cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
user_id = cursor.lastrowid  # Récupérer l'ID généré

# READ
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
row = cursor.fetchone()  # Une seule ligne
rows = cursor.fetchall()  # Toutes les lignes

# UPDATE
cursor.execute("UPDATE users SET name = ? WHERE id = ?", (new_name, user_id))

# DELETE
cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
affected = cursor.rowcount  # Nombre de lignes affectées
```

### Conversion Row → Pydantic
```python
conn.row_factory = sqlite3.Row  # Activer le mode dictionnaire

cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
row = cursor.fetchone()

# Conversion manuelle
return UserResponse(
    id=row["id"],
    name=row["name"],
    email=row["email"]
)

# Ou avec dict()
return UserResponse(**dict(row))
```

### Gérer les booléens

SQLite stocke les booléens comme 0 (False) ou 1 (True) :
```python
# Lors de l'insertion
cursor.execute("INSERT INTO items (active) VALUES (?)", (int(is_active),))

# Lors de la lecture
active = bool(row["active"])  # Convertir 0/1 en False/True
```

## Bonnes pratiques

### 1. Toujours fermer les connexions
```python
conn = get_db_connection()
try:
    # Opérations sur la base
    cursor.execute(...)
    conn.commit()
finally:
    conn.close()
```

### 2. Utiliser les paramètres `?`
```python
# ✅ BON - Protection contre les injections SQL
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))

# ❌ MAUVAIS - Vulnérable aux injections SQL
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
```

### 3. Vérifier rowcount après UPDATE/DELETE
```python
cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
if cursor.rowcount == 0:
    raise HTTPException(status_code=404, detail="Non trouvé")
```

### 4. Utiliser conn.row_factory
```python
conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
```

## Critères de validation

L'étape est validée quand :
- ✅ Vous avez testé les 3 concepts
- ✅ Tous les tests de `test_exercise_01.py` passent
- ✅ Tous les tests de `test_exercise_02.py` passent
- ✅ Vous comprenez les opérations CRUD
- ✅ Les fichiers .db sont créés dans le dossier databases/

## Dépannage

### Erreur "unable to open database file"
- Créez le dossier `databases/` manuellement
- Vérifiez les permissions du dossier

### Erreur "table already exists"
- Utilisez `CREATE TABLE IF NOT EXISTS`
- Ou supprimez le fichier .db pour recommencer

### Erreur "no such column"
- Vérifiez l'orthographe des colonnes
- Vérifiez que la table a bien été créée

### Les modifications ne sont pas sauvegardées
- Ajoutez `conn.commit()` après INSERT/UPDATE/DELETE

## Différence avec une vraie base de données

SQLite est parfait pour :
- ✅ Développement et prototypes
- ✅ Applications desktop
- ✅ Petits volumes de données
- ✅ Apprentissage SQL

Pour la production avec volume important :
- PostgreSQL, MySQL : Bases relationnelles complètes
- Gestion des connexions concurrentes
- Transactions avancées

## Pour aller plus loin

- Transactions SQLite (`BEGIN`, `COMMIT`, `ROLLBACK`)
- Index pour optimiser les performances
- Relations entre tables (clés étrangères)
- Migration vers PostgreSQL/MySQL

**Prochaine étape** : Architecture en couches et déploiement