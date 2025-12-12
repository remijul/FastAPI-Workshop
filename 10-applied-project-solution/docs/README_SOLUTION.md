# 🎓 Solution Complète - Mini-Projet

Cette solution contient l'implémentation complète des 3 niveaux du mini-projet.

## Structure de la solution

- **Niveau 1 (Base)** : CRUD complet ✅
- **Niveau 2 (Intermédiaire)** : Filtres, statistiques, level-up, exceptions ✅
- **Niveau 3 (Avancé)** : Authentification JWT + Interface Jinja2 + Docker ✅

## Fichiers implémentés

### Niveau 1
- `app/models.py` : Tous les modèles Pydantic
- `app/database.py` : Initialisation DB + chargement données
- `app/repositories.py` : CRUD complet
- `app/services.py` : Logique métier CRUD
- `app/routes.py` : 5 endpoints CRUD
- `app/main.py` : Application configurée

### Niveau 2
- `app/exceptions.py` : Exceptions personnalisées
- `app/repositories.py` : Méthodes de filtrage et stats
- `app/services.py` : Filtres, statistiques, level-up
- `app/routes.py` : Endpoints avancés

### Niveau 3
- `app/auth.py` : Hachage mot de passe + JWT
- `app/dependencies.py` : Vérification authentification
- `app/routes.py` : Routes protégées + routes web Jinja2
- Templates et CSS fournis

## Lancement

### Mode développement
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Avec Docker
```bash
docker-compose build
docker-compose up
```

## Tests
```bash
# Tous les tests
pytest -v

# Couverture
pytest --cov=app tests/
```

## Points pédagogiques clés

### Architecture en couches
Respectée à 100% :
- **Routes** : Validation + délégation au service
- **Services** : Logique métier + appel repository
- **Repositories** : SQL uniquement

### Validation Pydantic
- Contraintes sur tous les champs
- Validateurs personnalisés
- Alias pour `class`

### Gestion d'erreurs
- Exceptions personnalisées
- Gestionnaires d'exceptions
- Messages clairs

### Authentification
- Hachage bcrypt
- JWT avec expiration
- Protection routes sensibles

### Tests
- Fixtures pytest
- Isolation des tests
- Couverture complète

## Notes pour les étudiants

### Erreurs fréquentes

1. **Oublier `alias="class"` dans les modèles**
```python
   # ❌ Mauvais
   class_name: str
   
   # ✅ Bon
   character_class: str = Field(..., alias="class")
```

2. **Mettre du SQL dans les services**
```python
   # ❌ Mauvais (service)
   cursor.execute("SELECT * FROM...")
   
   # ✅ Bon (service)
   CharacterRepository.get_all()
```

3. **Ne pas gérer les exceptions**
```python
   # ❌ Mauvais
   character = repository.get_by_id(id)
   return character  # Peut être None !
   
   # ✅ Bon
   character = repository.get_by_id(id)
   if not character:
       raise CharacterNotFoundError(id)
   return character
```

4. **Oublier `from_attributes = True` dans Config**
```python
   # Nécessaire pour convertir sqlite3.Row en Pydantic
   class Config:
       from_attributes = True
```

5. **Construire l'UPDATE dynamiquement**
```python
   # Ne pas oublier les champs optionnels
   updates = character_data.model_dump(exclude_unset=True)
```

## Variantes possibles

Les étudiants peuvent avoir des approches différentes mais valides :

### Repository pattern
```python
# Approche 1 : Méthodes statiques (solution fournie)
class CharacterRepository:
    @staticmethod
    def get_all():
        ...

# Approche 2 : Instance avec connexion
class CharacterRepository:
    def __init__(self):
        self.conn = get_db_connection()
```

### Gestion des exceptions
```python
# Approche 1 : Exceptions dans le service (solution fournie)
def get_character(id):
    char = repo.get_by_id(id)
    if not char:
        raise CharacterNotFoundError(id)

# Approche 2 : Exceptions dans les routes
@router.get("/{id}")
def get_character(id):
    char = service.get_character(id)
    if not char:
        raise HTTPException(404, ...)
```

Les deux approches sont valides, la première est préférable (séparation des responsabilités).

## Extensions possibles

### Combat système
Algorithme simple implémenté :
1. Le plus rapide attaque en premier
2. Dégâts = max(1, attack - defense)
3. Tour par tour jusqu'à 0 HP

### Interface web avancée
- Formulaire de création
- Édition inline
- Graphiques de stats
- Animations

### Base de données
- PostgreSQL au lieu de SQLite
- Migrations avec Alembic
- Relations (équipement, quêtes)

## Critères d'évaluation

### Niveau 1 (Base) - /10
- Architecture en couches : /3
- CRUD fonctionnel : /4
- Validation Pydantic : /2
- Tests de base : /1

### Niveau 2 (Intermédiaire) - /6
- Exceptions personnalisées : /2
- Filtres et statistiques : /2
- Level-up : /1
- Tests complets : /1

### Niveau 3 (Optionnel) - Bonus /4
- Authentification : /2
- Interface Jinja2 : /1
- Docker : /1

## Total : /20 points

Bon courage pour la correction ! 🎯