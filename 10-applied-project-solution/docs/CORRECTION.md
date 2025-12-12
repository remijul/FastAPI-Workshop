# 📝 Guide de Correction - Mini-Projet

## Grille d'évaluation

### NIVEAU 1 : Base (/10 points)

#### Architecture en couches (/3 points)
- [ ] Séparation claire routes/services/repositories (1 pt)
- [ ] Pas de SQL dans les services (1 pt)
- [ ] Pas de logique métier dans les repositories (1 pt)

#### CRUD complet (/4 points)
- [ ] POST /characters fonctionnel (1 pt)
- [ ] GET /characters et GET /characters/{id} fonctionnels (1 pt)
- [ ] PUT /characters/{id} fonctionnel (1 pt)
- [ ] DELETE /characters/{id} fonctionnel (1 pt)

#### Validation Pydantic (/2 points)
- [ ] Modèles avec contraintes (Field, ge, le, min_length) (1 pt)
- [ ] Alias pour "class" correctement utilisé (0.5 pt)
- [ ] Config avec from_attributes = True (0.5 pt)

#### Tests de base (/1 point)
- [ ] Au moins 5 tests écrits et passants (1 pt)

---

### NIVEAU 2 : Intermédiaire (/6 points)

#### Exceptions personnalisées (/2 points)
- [ ] 3+ exceptions créées (CharacterNotFoundError, etc.) (1 pt)
- [ ] Gestionnaires d'exceptions dans main.py (1 pt)

#### Filtres et statistiques (/2 points)
- [ ] Filtres par classe et niveau fonctionnels (1 pt)
- [ ] Endpoint de statistiques avec calculs corrects (1 pt)

#### Level-up (/1 point)
- [ ] Endpoint level-up fonctionnel avec mise à jour stats (0.5 pt)
- [ ] Vérification niveau max (0.5 pt)

#### Tests complets (/1 point)
- [ ] 10+ tests couvrant les fonctionnalités niveau 2 (1 pt)

---

### NIVEAU 3 : Avancé - BONUS (/4 points)

#### Option A : Authentification (/2 points)
- [ ] Register + Login fonctionnels (0.5 pt)
- [ ] JWT créés et vérifiés (0.5 pt)
- [ ] Routes POST/DELETE protégées (0.5 pt)
- [ ] Dependency injection pour vérifier auth (0.5 pt)

#### Option B : Interface Jinja2 (/1 point)
- [ ] Page d'accueil avec liste personnages (0.5 pt)
- [ ] Page de détail avec stats visuelles (0.5 pt)

#### Option C : Docker (/1 point)
- [ ] Dockerfile fonctionnel (0.5 pt)
- [ ] docker-compose fonctionnel avec volumes (0.5 pt)

---

## Total : /20 points

---

## Points de vérification rapide

### ✅ Checklist minimale (Niveau 1)
```bash
# L'application démarre
uvicorn app.main:app --reload

# 10 personnages chargés au démarrage
curl http://localhost:8000/characters | jq length
# Devrait retourner: 10

# CRUD fonctionne
# POST
curl -X POST http://localhost:8000/characters \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","class":"warrior","level":25,"health_points":300,"attack":75,"defense":35,"speed":50}'

# GET
curl http://localhost:8000/characters/1

# PUT
curl -X PUT http://localhost:8000/characters/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated"}'

# DELETE (si pas protégé)
curl -X DELETE http://localhost:8000/characters/11

# Tests passent
pytest tests/test_characters.py -v
```

---

## Erreurs fréquentes à surveiller

### 1. Oublier l'alias "class"
```python
# ❌ Erreur fréquente
class: str  # SyntaxError

# ✅ Correct
character_class: str = Field(..., alias="class")
```

### 2. SQL dans les services
```python
# ❌ Mauvais
def get_character(id):
    cursor.execute("SELECT * FROM...")  # SQL dans le service !

# ✅ Bon
def get_character(id):
    return CharacterRepository.get_by_id(id)  # Déléguer au repository
```

### 3. Ne pas gérer les None
```python
# ❌ Risqué
def get_character(id):
    char = repository.get_by_id(id)
    return CharacterResponse(**char)  # char peut être None !

# ✅ Sûr
def get_character(id):
    char = repository.get_by_id(id)
    if not char:
        raise CharacterNotFoundError(id)
    return CharacterResponse(**char)
```

### 4. Oublier from_attributes
```python
# ❌ Erreur de conversion sqlite3.Row
class CharacterResponse(CharacterBase):
    id: int
    # Manque Config !

# ✅ Correct
class CharacterResponse(CharacterBase):
    id: int
    
    class Config:
        from_attributes = True
```

### 5. Update dynamique mal construit
```python
# ❌ Mauvais (met à jour même les champs non fournis)
updates = character_data.model_dump()

# ✅ Bon (seulement les champs fournis)
updates = character_data.model_dump(exclude_unset=True)
```

---

## Variantes acceptables

### Repository pattern

**Variante 1 : Static methods (recommandé)**
```python
class CharacterRepository:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        # ...
```

**Variante 2 : Instance**
```python
class CharacterRepository:
    def __init__(self):
        self.conn = get_db_connection()
    
    def get_all(self):
        # ...
```

Les deux sont valides.

### Gestion des filtres

**Variante 1 : Dans le service (recommandé)**
```python
def get_characters(filters):
    if filters:
        return get_characters_filtered(filters)
    return get_all_characters()
```

**Variante 2 : Dans la route**
```python
@router.get("/characters")
def get_characters(class=None, min_level=None):
    if class or min_level:
        return service.get_filtered(...)
    return service.get_all()
```

Les deux sont valides.

---

## Conseils pour la correction

1. **Tester d'abord** : Lancez l'app et testez manuellement
2. **Lire les tests** : Vérifiez quels tests passent
3. **Architecture** : Vérifiez la séparation des couches
4. **Code quality** : Regardez la lisibilité, les commentaires
5. **Bonus** : Valorisez les initiatives personnelles

---

## Questions fréquentes des étudiants

**Q: Dois-je utiliser Pydantic pour la réponse ?**
R: Oui, toujours définir les modèles de réponse avec Pydantic.

**Q: Comment tester avec authentification ?**
R: Créer un utilisateur, login, récupérer le token, l'utiliser dans les headers.

**Q: Le level-up doit-il être protégé ?**
R: Non requis, mais valorisé comme bonus.

**Q: Puis-je utiliser PostgreSQL au lieu de SQLite ?**
R: Oui, mais SQLite est plus simple pour le projet pédagogique.

**Q: Dois-je gérer les permissions (admin/user) ?**
R: Non requis pour ce projet.

---

Bonne correction ! 🎓