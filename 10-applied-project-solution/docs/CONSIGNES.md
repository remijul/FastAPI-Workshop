# 📋 Cahier des Charges - API de Gestion de Personnages

## Vue d'ensemble

Vous devez créer une API RESTful pour gérer des personnages de jeu vidéo. L'API permettra de créer, consulter, modifier et supprimer des personnages, avec différents niveaux de fonctionnalités.

## Modèle de données

### Personnage (Character)

Un personnage possède les attributs suivants :

| Attribut | Type | Contraintes | Description |
|----------|------|-------------|-------------|
| `id` | int | Auto-généré | Identifiant unique |
| `name` | str | min_length=2 | Nom du personnage |
| `class` | str | Valeurs: "warrior", "mage", "archer", "tank", "healer" | Classe du personnage |
| `level` | int | 1-100 | Niveau du personnage |
| `health_points` | int | 50-500 | Points de vie |
| `attack` | int | 10-100 | Points d'attaque |
| `defense` | int | 5-50 | Points de défense |
| `speed` | int | 10-100 | Vitesse |
| `special_ability` | str | Optionnel | Capacité spéciale |
| `image_url` | str | Optionnel | URL de l'image du personnage |
| `created_at` | datetime | Auto-généré | Date de création |

## Données initiales

Au démarrage de l'application, la base de données doit contenir 10 personnages pré-définis (fournis dans `data/initial_characters.json`).

---

## 🟢 NIVEAU 1 : BASE (Obligatoire)

### Objectifs
- Mettre en place l'architecture en couches
- Implémenter le CRUD complet
- Valider les données avec Pydantic
- Charger les données initiales

### Fonctionnalités à implémenter

#### 1. Architecture
- [ ] Structure en couches (models, database, repositories, services, routes)
- [ ] Configuration centralisée (`config.py`)
- [ ] Initialisation de la base de données SQLite

#### 2. Modèles Pydantic
- [ ] `CharacterCreate` : Modèle pour créer un personnage
- [ ] `CharacterUpdate` : Modèle pour modifier un personnage (tous les champs optionnels)
- [ ] `CharacterResponse` : Modèle de réponse (avec id et created_at)

#### 3. Endpoints CRUD

**POST /characters**
- Créer un nouveau personnage
- Validation automatique des contraintes
- Retour : 201 Created avec le personnage créé

**GET /characters**
- Liste tous les personnages
- Retour : 200 OK avec tableau de personnages

**GET /characters/{id}**
- Récupère un personnage par ID
- Retour : 200 OK avec le personnage
- Erreur : 404 si non trouvé

**PUT /characters/{id}**
- Met à jour un personnage existant
- Tous les champs sont optionnels
- Retour : 200 OK avec le personnage modifié
- Erreur : 404 si non trouvé

**DELETE /characters/{id}**
- Supprime un personnage
- Retour : 204 No Content
- Erreur : 404 si non trouvé

#### 4. Tests
- [ ] Écrire les tests pour tous les endpoints CRUD
- [ ] Utiliser les fixtures pytest

### Critères de validation Niveau 1
- ✅ Architecture en couches respectée
- ✅ Tous les endpoints CRUD fonctionnels
- ✅ Validation Pydantic en place
- ✅ 10 personnages chargés au démarrage
- ✅ Tests de base passants

---

## 🟡 NIVEAU 2 : INTERMÉDIAIRE (Obligatoire)

### Objectifs
- Ajouter des fonctionnalités avancées
- Gérer les erreurs avec exceptions personnalisées
- Implémenter des filtres et statistiques

### Fonctionnalités à implémenter

#### 1. Exceptions personnalisées
- [ ] `CharacterNotFoundError` : Personnage non trouvé
- [ ] `InvalidClassError` : Classe invalide
- [ ] `InvalidLevelError` : Niveau hors limites
- [ ] Gestionnaires d'exceptions (`@app.exception_handler`)

#### 2. Filtres de recherche

**GET /characters?class={class}**
- Filtre par classe
- Exemple : `/characters?class=mage`

**GET /characters?min_level={level}&max_level={level}**
- Filtre par niveau min et max
- Exemple : `/characters?min_level=10&max_level=50`

**GET /characters?class={class}&min_level={level}**
- Combinaison de filtres possible

#### 3. Statistiques

**GET /characters/stats**
- Statistiques globales :
  - Nombre total de personnages
  - Nombre de personnages par classe
  - Niveau moyen
  - Niveau min et max
  - Moyenne d'attaque par classe

**GET /classes**
- Liste des classes disponibles avec le nombre de personnages par classe

#### 4. Opérations spécifiques

**POST /characters/{id}/level-up**
- Augmente le niveau d'un personnage de 1
- Met à jour les statistiques en conséquence (health +10, attack +2, defense +1)
- Retour : 200 OK avec le personnage mis à jour
- Erreur : 400 si déjà niveau max (100)

### Critères de validation Niveau 2
- ✅ Exceptions personnalisées implémentées
- ✅ Filtres de recherche fonctionnels
- ✅ Endpoint de statistiques opérationnel
- ✅ Level-up fonctionnel avec mise à jour des stats
- ✅ Tests complets

---

## 🔴 NIVEAU 3 : AVANCÉ (Optionnel)

Ce niveau est optionnel. Choisissez les fonctionnalités qui vous intéressent.

### Option A : Authentification

#### Objectifs
- Protéger certaines routes
- Gérer des utilisateurs

#### Fonctionnalités
- [ ] Modèle `User` (username, hashed_password)
- [ ] POST /auth/register : Inscription
- [ ] POST /auth/login : Connexion (retourne un token JWT)
- [ ] Protection des routes POST et DELETE (nécessite authentification)
- [ ] Routes GET restent publiques

#### Implémentation
- Utiliser JWT pour l'authentification
- Hachage des mots de passe avec bcrypt
- Dependency injection pour vérifier l'authentification

### Option B : Interface Web (Jinja2)

#### Objectifs
- Créer une interface web pour visualiser les personnages

#### Fonctionnalités
- [ ] Page d'accueil : Liste des personnages avec filtres
- [ ] Page détail : Fiche complète d'un personnage
- [ ] Affichage des images des personnages
- [ ] Statistiques visuelles

#### Templates à créer
- `base.html` : Template de base
- `home.html` : Liste des personnages
- `character_detail.html` : Détail d'un personnage

#### Routes Web
- GET / : Page d'accueil (HTML)
- GET /characters/{id}/details : Détail personnage (HTML)

### Option C : Endpoint de Combat

#### Objectif
- Simuler un combat entre deux personnages

#### Fonctionnalités

**POST /battle**
- Body : `{"character1_id": 1, "character2_id": 2}`
- Simule un combat au tour par tour
- Calcul basé sur : attack, defense, speed, health_points
- Retour : Résultat du combat avec le gagnant et les détails

#### Algorithme de combat simplifié
1. Le personnage le plus rapide attaque en premier
2. Dégâts = max(1, attack_attaquant - defense_défenseur)
3. Alternance des tours jusqu'à ce qu'un personnage atteigne 0 HP
4. Retour du vainqueur avec détails (nombre de tours, HP restants)

### Option D : Docker

#### Objectifs
- Conteneuriser l'application
- Déploiement simplifié

#### Fichiers à créer
- [ ] `Dockerfile` : Image de l'application
- [ ] `docker-compose.yml` : Orchestration des services
- [ ] Volume pour persister la base de données

#### Commandes Docker
```bash
docker-compose build
docker-compose up
docker-compose down
```

### Critères de validation Niveau 3
- ✅ Au moins une option implémentée complètement
- ✅ Fonctionnalité testée et fonctionnelle
- ✅ Documentation claire de l'option choisie

---

## 📊 Récapitulatif des endpoints

### CRUD de base
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | /characters | Créer un personnage |
| GET | /characters | Lister tous les personnages |
| GET | /characters/{id} | Obtenir un personnage |
| PUT | /characters/{id} | Modifier un personnage |
| DELETE | /characters/{id} | Supprimer un personnage |

### Endpoints avancés
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | /characters?class={class} | Filtrer par classe |
| GET | /characters?min_level={level} | Filtrer par niveau min |
| GET | /characters?max_level={level} | Filtrer par niveau max |
| GET | /characters/stats | Statistiques globales |
| GET | /classes | Liste des classes |
| POST | /characters/{id}/level-up | Augmenter le niveau |

### Endpoints optionnels
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | /auth/register | Inscription (Niveau 3) |
| POST | /auth/login | Connexion (Niveau 3) |
| POST | /battle | Combat entre personnages (Niveau 3) |
| GET | / | Page d'accueil web (Niveau 3) |

---

## 💡 Conseils

### Organisation du travail
1. **Commencez simple** : Niveau 1 d'abord, puis progressez
2. **Testez régulièrement** : Utilisez `/docs` pour tester vos endpoints
3. **Committez souvent** : Sauvegardez votre progression
4. **Lisez les erreurs** : Les messages d'erreur FastAPI sont très clairs

### Bonnes pratiques
- Utilisez des noms de variables explicites
- Commentez les parties complexes
- Respectez la séparation des responsabilités par couche
- Écrivez les tests au fur et à mesure

### Ressources utiles
- Documentation FastAPI : https://fastapi.tiangolo.com/
- Rappel étape 6 : Architecture en couches
- Rappel étape 7 : Gestion d'erreurs
- Rappel étape 8 : Authentification JWT

---

## ✅ Check-list finale

### Niveau 1 (Base)
- [ ] Architecture en couches
- [ ] CRUD complet (5 endpoints)
- [ ] Modèles Pydantic avec validation
- [ ] Base de données initialisée avec 10 personnages
- [ ] Tests de base

### Niveau 2 (Intermédiaire)
- [ ] Exceptions personnalisées
- [ ] Filtres de recherche (classe, niveau)
- [ ] Endpoint de statistiques
- [ ] Endpoint level-up
- [ ] Tests complets

### Niveau 3 (Optionnel - au choix)
- [ ] Option A : Authentification JWT
- [ ] Option B : Interface Jinja2
- [ ] Option C : Combat entre personnages
- [ ] Option D : Docker

---

**Bonne chance et amusez-vous bien ! 🎮**