# 🎮 Mini-Projet : API de Gestion de Personnages de Jeu Vidéo

## Description

Ce projet est le projet de synthèse du workshop FastAPI. Il vous permet de mettre en pratique tous les concepts vus lors des étapes précédentes.

Vous allez développer une API complète pour gérer une base de données de personnages de jeu vidéo avec les fonctionnalités CRUD (Create, Read, Update, Delete).

## Objectifs pédagogiques

- ✅ Concevoir une API RESTful complète
- ✅ Appliquer l'architecture en couches
- ✅ Valider les données avec Pydantic
- ✅ Gérer une base de données SQLite
- ✅ Implémenter la gestion d'erreurs
- ✅ Écrire des tests
- ✅ (Optionnel) Ajouter l'authentification
- ✅ (Optionnel) Créer une interface web avec Jinja2
- ✅ (Optionnel) Conteneuriser avec Docker

## Structure du projet
```
mini-projet/
├── app/                 # Code source de l'application
├── tests/              # Tests automatisés
├── data/               # Données initiales
├── databases/          # Base de données SQLite
└── [fichiers config]   # Configuration et déploiement
```

## Installation

### Prérequis
- Python 3.8 ou supérieur
- pip

### Installation des dépendances
```bash
pip install -r requirements.txt
```

## Lancement
```bash
uvicorn app.main:app --reload
```

L'API sera accessible sur : http://localhost:8000

Documentation interactive : http://localhost:8000/docs

## Progression

Le projet est divisé en 3 niveaux de difficulté :

1. **Niveau Base** : CRUD simple + Validation
2. **Niveau Intermédiaire** : Filtres + Gestion d'erreurs + Statistiques
3. **Niveau Avancé** (Optionnel) : Authentification + Interface web + Docker

Consultez **CONSIGNES.md** pour les détails complets.

Consultez **GUIDE_DEMARRAGE.md** pour les premières actions à mener.

## Tests
```bash
# Lancer tous les tests
pytest

# Lancer avec verbosité
pytest -v

# Lancer un fichier spécifique
pytest tests/test_characters.py -v
```

## Docker (Optionnel - Niveau Avancé)
```bash
# Build de l'image
docker-compose build

# Lancement
docker-compose up

# Arrêt
docker-compose down
```

## Ressources

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation Pydantic](https://docs.pydantic.dev/)
- [Documentation pytest](https://docs.pytest.org/)

## Aide

En cas de blocage :
1. Relisez les étapes du workshop correspondantes
2. Consultez la documentation FastAPI
3. Testez vos endpoints avec `/docs`
4. Vérifiez les logs d'erreur dans la console

Bon courage ! 🚀