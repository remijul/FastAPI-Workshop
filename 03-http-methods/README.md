# Étape 3 : Méthodes HTTP

## Objectifs

Cette étape vous permet de maîtriser les différentes méthodes HTTP pour créer des API complètes :

- Comprendre les 4 méthodes HTTP principales (GET, POST, PUT, DELETE)
- Créer des API CRUD (Create, Read, Update, Delete)
- Utiliser Pydantic pour valider les données entrantes
- Utiliser les codes de statut HTTP appropriés (200, 201, 404, 400)
- Gérer les erreurs avec les bons codes HTTP

## Prérequis

- Python 3.8 ou supérieur installé
- Avoir validé l'étape 2 (FastAPI Essentials)

## Installation

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

Les packages installés :
- `fastapi` : Framework web pour créer des API
- `uvicorn` : Serveur ASGI
- `pytest` : Framework de tests
- `httpx` : Client HTTP pour les tests
- `pydantic` : Validation des données

## Structure du dossier
```
03-http-methods/
├── concepts/
│   ├── concepts_01_get_method.py          # Méthode GET
│   ├── concepts_02_post_method.py         # Méthode POST
│   ├── concepts_03_put_delete_methods.py  # Méthodes PUT & DELETE
│   └── concepts_04_status_codes.py        # Codes de statut HTTP
├── exercises/
│   ├── exercise_01.py                     # Exercice 1 : API blog
│   └── exercise_02.py                     # Exercice 2 : Inventaire
├── tests/
│   ├── test_concepts.py                   # Tests des concepts
│   ├── test_exercise_01.py                # Tests exercice 1
│   └── test_exercise_02.py                # Tests exercice 2
├── requirements.txt                        # Dépendances
└── README.md                              # Ce fichier
```

## Étapes de travail

### 1. Découvrir les concepts

#### Concept 1 : Méthode GET (Lecture)

Lisez le fichier `concepts/concepts_01_get_method.py` puis lancez :
```bash
uvicorn concepts.concepts_01_get_method:app --reload
```

**Ce que fait GET** :
- Récupère des données
- Ne modifie JAMAIS les données sur le serveur
- Peut utiliser des paramètres de chemin et de requête

**Testez dans Swagger** :
- `GET /books` : Liste tous les livres
- `GET /books/1` : Récupère un livre par ID
- `GET /books/search?author=Alice` : Recherche par auteur

**Important** : Notez l'ordre des routes !
```python
@app.get("/books")           # 1. Route de base
@app.get("/books/search")    # 2. Route fixe spécifique
@app.get("/books/{book_id}") # 3. Route avec paramètre (EN DERNIER)
```

#### Concept 2 : Méthode POST (Création)

Lisez le fichier `concepts/concepts_02_post_method.py` puis lancez :
```bash
uvicorn concepts.concepts_02_post_method:app --reload
```

**Ce que fait POST** :
- Crée de nouvelles ressources
- Envoie des données dans le corps de la requête (body)
- Utilise Pydantic pour valider les données

**Testez dans Swagger** :
1. `GET /users` : Liste vide au départ
2. `POST /users` avec le JSON :
```json
   {
     "name": "Alice",
     "email": "alice@example.com",
     "age": 25
   }
```
3. `GET /users` : Voir l'utilisateur créé

**Validation automatique** : Essayez de créer un utilisateur sans le champ `age` → Erreur 422 !

#### Concept 3 : Méthodes PUT et DELETE (Mise à jour et Suppression)

Lisez le fichier `concepts/concepts_03_put_delete_methods.py` puis lancez :
```bash
uvicorn concepts.concepts_03_put_delete_methods:app --reload
```

**Ce que fait PUT** :
- Met à jour une ressource existante
- Remplace TOUTES les données de la ressource
- Nécessite tous les champs

**Ce que fait DELETE** :
- Supprime une ressource
- Ne nécessite que l'ID

**Testez dans Swagger** :
1. `GET /products` : Voir les produits initiaux
2. `PUT /products/1` avec :
```json
   {
     "name": "Gaming Laptop",
     "price": 1299.99,
     "stock": 5
   }
```
3. `GET /products/1` : Voir la modification
4. `DELETE /products/2` : Supprimer un produit
5. `GET /products` : Vérifier la suppression

#### Concept 4 : Codes de statut HTTP

Lisez le fichier `concepts/concepts_04_status_codes.py` puis lancez :
```bash
uvicorn concepts.concepts_04_status_codes:app --reload
```

**Codes de statut principaux** :
- `200 OK` : Requête réussie (GET, PUT par défaut)
- `201 Created` : Ressource créée (POST)
- `204 No Content` : Succès sans contenu à retourner (DELETE)
- `404 Not Found` : Ressource non trouvée
- `400 Bad Request` : Requête invalide (ex: données incorrectes)
- `422 Unprocessable Entity` : Validation échouée (automatique avec Pydantic)

**Testez dans Swagger et observez les codes** :
- `POST /items` : Code 201
- `GET /items/999` : Code 404
- `DELETE /items/1` : Code 204

### 2. Exécuter les tests des concepts

Vérifiez votre compréhension :
```bash
pytest tests/test_concepts.py -v
```

Tous les tests doivent passer ✅

### 3. Compléter l'exercice 1 : API CRUD d'articles de blog

**Objectif** : Créer une API complète pour gérer des articles de blog.

Ouvrez `exercises/exercise_01.py` et complétez les TODO.

**Modèle à créer** :
```python
class Article(BaseModel):
    title: str
    content: str
    author: str
```

**Routes à implémenter** :
- `GET /articles` : Liste tous les articles (200)
- `GET /articles/{article_id}` : Récupère un article (200 ou 404)
- `POST /articles` : Crée un article (201)
- `PUT /articles/{article_id}` : Met à jour un article (200 ou 404)
- `DELETE /articles/{article_id}` : Supprime un article (200 ou 404)

**Gestion des erreurs** :
- Si article non trouvé : retourner `{"error": "Article non trouvé"}` avec code 404

**Tester votre code** :
```bash
# Lancer le serveur
uvicorn exercises.exercise_01:app --reload

# Dans un autre terminal
pytest tests/test_exercise_01.py -v
```

### 4. Compléter l'exercice 2 : API de gestion d'inventaire

**Objectif** : Créer une API pour gérer un inventaire avec logique métier.

Ouvrez `exercises/exercise_02.py` et complétez les TODO.

**Modèle à créer** :
```python
class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int
```

**Routes à implémenter** :
- `GET /inventory` : Liste tous les produits (200)
- `GET /inventory/{product_id}` : Récupère un produit (200 ou 404)
- `POST /inventory` : Ajoute un produit (201)
- `PUT /inventory/{product_id}/restock?quantity=X` : Réapprovisionne (200 ou 404)
- `PUT /inventory/{product_id}/sell?quantity=X` : Vend (200, 400 ou 404)
- `DELETE /inventory/{product_id}` : Supprime un produit (200 ou 404)

**Logique métier importante** :
- Pour `/restock` : AJOUTER la quantité au stock existant
- Pour `/sell` : 
  - Vérifier que le stock est suffisant
  - Si insuffisant : retourner `{"error": "Stock insuffisant"}` avec code 400
  - Sinon : réduire le stock

**Tester votre code** :
```bash
# Lancer le serveur
uvicorn exercises.exercise_02:app --reload

# Dans un autre terminal
pytest tests/test_exercise_02.py -v
```

## Résumé des méthodes HTTP

| Méthode | Usage | Code succès | Modifie données |
|---------|-------|-------------|-----------------|
| GET | Lire des données | 200 | Non |
| POST | Créer une ressource | 201 | Oui |
| PUT | Mettre à jour (remplacer) | 200 | Oui |
| DELETE | Supprimer | 200 ou 204 | Oui |

## Utilisation de Pydantic

### Définir un modèle
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int
```

### Utiliser dans une route
```python
@app.post("/users")
def create_user(user: User):
    # Pydantic valide automatiquement les données
    return {"name": user.name, "email": user.email}
```

### Validation automatique
Pydantic vérifie automatiquement :
- Que tous les champs requis sont présents
- Que les types sont corrects (str, int, float...)
- Retourne une erreur 422 si invalide

## Codes de statut HTTP

### Définir un code fixe
```python
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item():
    return {"message": "Created"}
```

### Modifier le code dynamiquement
```python
@app.get("/items/{item_id}")
def get_item(item_id: int, response: Response):
    if not found:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Not found"}
    return item
```

## Critères de validation

L'étape est validée quand :
- ✅ Vous avez testé les 4 concepts dans Swagger
- ✅ Tous les tests de `test_exercise_01.py` passent
- ✅ Tous les tests de `test_exercise_02.py` passent
- ✅ Vous comprenez la différence entre GET, POST, PUT, DELETE
- ✅ Vous utilisez les bons codes de statut HTTP
- ✅ Vous gérez les erreurs correctement (404, 400)

## Concepts clés à retenir

### Structure CRUD complète
```python
# READ
@app.get("/items")
def get_all_items():
    return items_db

@app.get("/items/{item_id}")
def get_item(item_id: int):
    # Retourner l'item ou 404

# CREATE
@app.post("/items", status_code=201)
def create_item(item: Item):
    # Créer et retourner l'item

# UPDATE
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    # Mettre à jour et retourner l'item ou 404

# DELETE
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    # Supprimer et retourner confirmation ou 404
```

### Gestion des erreurs
```python
@app.get("/items/{item_id}")
def get_item(item_id: int, response: Response):
    item = find_item(item_id)
    
    if item is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Item non trouvé"}
    
    return item
```

### Validation métier
```python
@app.put("/products/{product_id}/sell")
def sell_product(product_id: int, quantity: int, response: Response):
    product = find_product(product_id)
    
    if product is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Produit non trouvé"}
    
    if product["stock"] < quantity:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Stock insuffisant"}
    
    product["stock"] -= quantity
    return product
```

## Dépannage

### Les tests POST/PUT échouent
- Vérifiez que vous utilisez bien `json=data` dans les tests
- Vérifiez que votre modèle Pydantic a tous les champs requis
- Regardez l'erreur 422 pour voir quel champ pose problème

### Code de statut incorrect
- Utilisez `status_code=` dans le décorateur pour un code fixe
- Utilisez `response.status_code =` pour un code dynamique
- Importez `from fastapi import status` pour les constantes

### Erreur 422 inattendue
- Vérifiez que tous les champs du modèle Pydantic sont fournis
- Vérifiez les types (str, int, float)
- Consultez le détail de l'erreur dans la réponse JSON

## Différences importantes

### POST vs PUT
- **POST** : Crée une NOUVELLE ressource, le serveur génère l'ID
- **PUT** : Met à jour une ressource EXISTANTE avec un ID connu

### PUT vs PATCH
- **PUT** : Remplace TOUTES les données (tous les champs requis)
- **PATCH** : Met à jour partiellement (sera vu plus tard)

### Codes 200 vs 201 vs 204
- **200** : Succès avec contenu dans la réponse
- **201** : Ressource créée (utilisé pour POST)
- **204** : Succès sans contenu (parfois utilisé pour DELETE)

### Codes 400 vs 404 vs 422
- **400** : Erreur de logique métier (ex: stock insuffisant)
- **404** : Ressource non trouvée
- **422** : Validation Pydantic échouée (automatique)

## Pour aller plus loin

Une fois cette étape validée, vous pouvez explorer :
- Les autres méthodes HTTP (PATCH, OPTIONS, HEAD)
- La validation avancée avec Pydantic (contraintes, validateurs personnalisés)
- Les codes de statut HTTP complets : https://httpstatuses.com/
- Les middlewares pour gérer les erreurs globalement

**Prochaine étape** : Modèles et validation Pydantic avancée
