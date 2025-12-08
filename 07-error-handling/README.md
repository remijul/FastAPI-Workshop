# Étape 7 : Gestion des Erreurs

## Objectifs

Cette étape vous apprend à gérer proprement les erreurs dans votre API :

- Utiliser HTTPException pour les erreurs standards
- Créer des exceptions personnalisées
- Implémenter des gestionnaires d'exceptions
- Ajouter un middleware pour logger et capturer les erreurs
- Retourner des réponses d'erreur cohérentes

## Prérequis

- Python 3.8 ou supérieur installé
- Avoir validé l'étape 6 (Architecture en couches)

## Installation
```bash
pip install -r requirements.txt
```

Pas de nouveaux packages requis !

## Les 3 niveaux de gestion d'erreurs

**Niveau 1** : HTTPException (erreurs standards)  
**Niveau 2** : Exceptions personnalisées (erreurs métier)  
**Niveau 3** : Middleware (erreurs inattendues)

## Concept 1 : HTTPException
```bash
uvicorn concepts.concepts_01_http_exceptions:app --reload
```

**HTTPException** : La manière standard de lever des erreurs dans FastAPI.
```python
from fastapi import HTTPException, status

# Ressource non trouvée
if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Utilisateur non trouvé"
    )

# Validation métier échouée
if username_exists:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Ce nom d'utilisateur existe déjà"
    )

# Action interdite
if user_id == 1:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Impossible de supprimer l'admin"
    )
```

**Codes HTTP principaux** :
- **200 OK** : Succès
- **201 Created** : Ressource créée
- **400 Bad Request** : Erreur de validation métier
- **403 Forbidden** : Action interdite
- **404 Not Found** : Ressource non trouvée
- **422 Unprocessable Entity** : Erreur de validation Pydantic
- **500 Internal Server Error** : Erreur serveur

## Concept 2 : Exceptions personnalisées
```bash
uvicorn concepts.concepts_02_custom_exceptions:app --reload
```

**Avantages** : Code plus lisible, réutilisable, gestion centralisée.

**1. Définir l'exception** :
```python
class ProductNotFoundError(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        self.message = f"Produit {product_id} non trouvé"
        super().__init__(self.message)
```

**2. Créer le gestionnaire** :
```python
@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(request: Request, exc: ProductNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Product Not Found",
            "message": exc.message,
            "product_id": exc.product_id
        }
    )
```

**3. Utiliser dans le code** :
```python
if not product:
    raise ProductNotFoundError(product_id)
```

## Concept 3 : Middleware d'erreurs
```bash
uvicorn concepts.concepts_03_error_middleware:app --reload
```

**Middleware** : Intercepte toutes les requêtes et capture les erreurs inattendues.
```python
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    start_time = time.time()
    
    try:
        logger.info(f"Request: {request.method} {request.url.path}")
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Completed in {process_time:.3f}s")
        return response
    
    except Exception as exc:
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "message": "Une erreur inattendue s'est produite"
            }
        )
```

**Testez** : `GET /error` déclenche une erreur capturée par le middleware.

## Exercice 1 : API de comptes bancaires (3 TODO)

**Objectif** : Créer une API bancaire avec gestion d'erreurs personnalisées.

**Structure** : Architecture en couches + fichier `exceptions.py`

**TODO 1** (`exceptions.py`) : Créer 3 exceptions personnalisées
- `AccountNotFoundError(account_id)`
- `InsufficientFundsError(account_id, amount, balance)`
- `NegativeAmountError(amount)`

**TODO 2** (`services.py`) : Implémenter les méthodes avec gestion d'erreurs
- `create_account` : Créer un compte
- `get_account` : Lever `AccountNotFoundError` si non trouvé
- `deposit` : Lever `NegativeAmountError` si montant <= 0
- `withdraw` : Lever `InsufficientFundsError` si solde insuffisant

**TODO 3** (`main.py`) : Configurer les gestionnaires d'exceptions
- Handler pour `AccountNotFoundError` → 404
- Handler pour `InsufficientFundsError` → 400
- Handler pour `NegativeAmountError` → 400

**Tester** :
```bash
uvicorn exercises.exercise_01.main:app --reload
pytest tests/test_exercise_01.py -v
```

## Exercice 2 : API de réservation d'hôtel (3 TODO)

**Objectif** : API de réservation avec middleware de logging.

**TODO 1** (`exceptions.py`) : Créer 3 exceptions
- `RoomNotFoundError(room_id)`
- `RoomNotAvailableError(room_id, room_name)`
- `InvalidDateError(message)`

**TODO 2** (`services.py`) : Implémenter avec validations
- `create_room` : Créer une chambre
- `get_room` : Lever `RoomNotFoundError` si non trouvé
- `create_reservation` : 
  * Vérifier `nights > 0` → `InvalidDateError`
  * Vérifier chambre existe → `RoomNotFoundError`
  * Vérifier disponibilité → `RoomNotAvailableError`
  * Calculer `total_price = price_per_night * nights`

**TODO 3** (`main.py`) : Middleware + gestionnaires
- Middleware qui log toutes les requêtes
- 3 gestionnaires d'exceptions

**Tester** :
```bash
uvicorn exercises.exercise_02.main:app --reload
pytest tests/test_exercise_02.py -v
```

## Bonnes pratiques

### 1. Hiérarchie des erreurs
```
Erreur Pydantic (422) ← Validation automatique
      ↓
HTTPException (400) ← Validation métier simple
      ↓
Exception personnalisée ← Logique métier complexe
      ↓
Middleware ← Erreurs inattendues
```

### 2. Messages d'erreur clairs
```python
# ❌ MAUVAIS
raise HTTPException(400, "Error")

# ✅ BON
raise InsufficientFundsError(
    account_id=1,
    amount=100.0,
    balance=50.0
)
# Retourne : {"error": "Insufficient Funds", "balance": 50.0, ...}
```

### 3. Ne pas exposer d'infos sensibles
```python
# ❌ MAUVAIS
except Exception as exc:
    return {"error": str(exc)}  # Peut exposer des détails internes

# ✅ BON
except Exception as exc:
    logger.error(f"Error: {exc}")  # Log en interne
    return {"error": "Internal Server Error"}  # Message générique
```

## Structure d'une réponse d'erreur

**Format cohérent** :
```json
{
  "error": "Nom de l'erreur",
  "message": "Description détaillée",
  "field_name": "valeur_additionnelle"
}
```

**Exemples** :
```json
// 404
{
  "error": "Account Not Found",
  "message": "Compte 123 non trouvé",
  "account_id": 123
}

// 400
{
  "error": "Insufficient Funds",
  "message": "Solde insuffisant...",
  "requested": 100.0,
  "balance": 50.0
}
```

## Différence HTTPException vs Exception personnalisée

**HTTPException** : Simple, directe
```python
raise HTTPException(404, "Non trouvé")
```

**Exception personnalisée** : Réutilisable, riche en données
```python
raise ProductNotFoundError(product_id)
# Contient automatiquement product_id, message formaté, etc.
```

## Critères de validation

L'étape est validée quand :
- ✅ Vous utilisez HTTPException pour les erreurs simples
- ✅ Vous créez des exceptions personnalisées pour la logique métier
- ✅ Vous implémentez des gestionnaires d'exceptions
- ✅ Tous les tests de `test_exercise_01.py` passent
- ✅ Tous les tests de `test_exercise_02.py` passent
- ✅ Vos réponses d'erreur sont cohérentes

## Dépannage

### L'exception n'est pas capturée
- Vérifiez que le gestionnaire est enregistré avant `app.include_router()`
- Utilisez `@app.exception_handler(VotreException)`

### Le middleware ne log pas
- Vérifiez la configuration du logging : `logging.basicConfig(level=logging.INFO)`
- Le middleware doit être ajouté avant les routes

### Erreur 500 au lieu de l'exception personnalisée
- L'exception est levée mais pas de gestionnaire → devient 500
- Ajoutez le `@app.exception_handler` correspondant

## Logging efficace
```python
import logging

logger = logging.getLogger(__name__)

# Dans le middleware
logger.info(f"Request: {request.method} {request.url.path}")

# Dans les gestionnaires
logger.warning(f"RoomNotFoundError: {exc.message}")

# Pour les erreurs graves
logger.error(f"Unexpected error: {exc}", exc_info=True)
```

## Pour aller plus loin

- Gestion des erreurs asynchrones
- Retry automatique avec tenacity
- Circuit breaker pattern
- Alertes sur erreurs critiques
- Monitoring avec Sentry

**Workshop terminé !** Vous maîtrisez maintenant FastAPI de bout en bout. 🎉