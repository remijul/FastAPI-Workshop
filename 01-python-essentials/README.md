# Étape 1 : Fondations Python

## Objectifs

Cette première étape vous permet de réviser et consolider les bases de Python nécessaires pour développer des API avec FastAPI :

- Écrire des fonctions avec des annotations de type
- Créer et utiliser des classes
- Gérer les erreurs avec des exceptions
- Écrire et exécuter des tests unitaires avec pytest

## Prérequis

- Python 3.8 ou supérieur installé
- pip (gestionnaire de packages Python)

## Installation

1. Installer pytest :
```bash
pip install pytest
```

## Structure du dossier
```
01-python-essentials/
├── concepts/
│   ├── concepts_01_functions.py       # Exemples de fonctions
│   ├── concepts_02_classes.py         # Exemples de classes
│   └── concepts_03_error_handling.py  # Gestion des erreurs
├── exercises/
│   ├── exercise_01.py                 # Exercice 1 : Panier d'achat
│   └── exercise_02.py                 # Exercice 2 : Gestion utilisateurs
└── tests/
    ├── test_concepts.py               # Tests des concepts
    ├── test_exercise_01.py            # Tests exercice 1
    └── test_exercise_02.py            # Tests exercice 2
```

## Étapes de travail

### 1. Découvrir les concepts

Lisez et exécutez les fichiers dans le dossier `concepts/` pour comprendre :
- Comment écrire des fonctions avec des paramètres typés
- Comment créer des classes avec des méthodes
- Comment lever et gérer des exceptions personnalisées

### 2. Exécuter les tests des concepts

Lancez les tests pour voir pytest en action :
```bash
# Depuis le dossier 01-python-essentials
pytest tests/test_concepts.py -v
```

Tous les tests doivent passer ✅

### 3. Compléter l'exercice 1

**Objectif** : Créer une classe `Cart` pour gérer un panier d'achat.

Ouvrez `exercises/exercise_01.py` et complétez les méthodes marquées `TODO`.

**Fonctionnalités à implémenter** :
- Ajouter des produits au panier
- Calculer le total du panier
- Appliquer un coupon de réduction
- Vérifier si le panier est vide

**Tester votre code** :
```bash
pytest tests/test_exercise_01.py -v
```

### 4. Compléter l'exercice 2

**Objectif** : Créer un système de gestion d'utilisateurs avec validation.

Ouvrez `exercises/exercise_02.py` et complétez les méthodes marquées `TODO`.

**Fonctionnalités à implémenter** :
- Ajouter un utilisateur avec validation (nom, email, âge)
- Récupérer un utilisateur par email
- Mettre à jour l'âge d'un utilisateur
- Gérer les exceptions personnalisées

**Tester votre code** :
```bash
pytest tests/test_exercise_02.py -v
```

## Commandes pytest utiles
```bash
# Exécuter tous les tests de l'étape
pytest tests/ -v

# Exécuter un fichier de test spécifique
pytest tests/test_exercise_01.py -v

# Exécuter un test spécifique
pytest tests/test_exercise_01.py::test_add_product -v

# Afficher les print() dans les tests
pytest tests/ -v -s

# Arrêter au premier échec
pytest tests/ -v -x

# Afficher un résumé des tests
pytest tests/ -v --tb=short
```

## Critères de validation

L'étape est validée quand :
- ✅ Tous les tests de `test_exercise_01.py` passent
- ✅ Tous les tests de `test_exercise_02.py` passent
- ✅ Votre code respecte les types annotés
- ✅ Vous comprenez comment fonctionnent les tests pytest

## Concepts clés à retenir

### Annotations de type
```python
def add(a: int, b: int) -> int:
    return a + b
```

### Exceptions personnalisées
```python
class MyError(Exception):
    pass

raise MyError("Message d'erreur")
```

### Tests avec pytest
```python
def test_something():
    assert 1 + 1 == 2

def test_exception():
    with pytest.raises(ValueError):
        raise ValueError("Erreur")
```

## Aide

Si vous êtes bloqué :
1. Relisez les exemples dans `concepts/`
2. Regardez les tests pour comprendre ce qui est attendu
3. Testez régulièrement avec pytest
4. Demandez de l'aide au formateur

## Pour aller plus loin

Une fois cette étape validée, vous pouvez explorer :
- La documentation pytest : https://docs.pytest.org/
- Les type hints Python : https://docs.python.org/3/library/typing.html
- Les exceptions Python : https://docs.python.org/3/tutorial/errors.html