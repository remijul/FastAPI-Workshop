"""
Exercice 1 : API CRUD complète pour des articles de blog

Objectif : Créer une API avec les 4 opérations CRUD (Create, Read, Update, Delete)

TODO:
1. Créer une application FastAPI
2. Créer un modèle Pydantic Article avec : title (str), content (str), author (str)
3. Implémenter les 5 routes demandées
4. Utiliser les bons codes de statut HTTP
5. Faire passer tous les tests dans tests/test_exercise_01.py

Base de données simulée : liste articles_db en mémoire

Pour lancer l'API :
    uvicorn exercises.exercise_01:app --reload

Pour tester :
    pytest tests/test_exercise_01.py -v
"""

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

# TODO: Créer l'application FastAPI
app = None

# TODO: Créer la base de données simulée
articles_db = []
article_id_counter = 1


# TODO: Créer le modèle Pydantic Article
# Champs : title (str), content (str), author (str)
class Article(BaseModel):
    pass


# TODO: Route GET /articles - Retourne tous les articles
# Status code: 200


# TODO: Route GET /articles/{article_id} - Retourne un article par ID
# Status code: 200 si trouvé, 404 sinon
# Si non trouvé, retourner: {"error": "Article non trouvé"}


# TODO: Route POST /articles - Crée un nouvel article
# Status code: 201
# Paramètre: article (Article)
# Retourner: l'article créé avec son ID


# TODO: Route PUT /articles/{article_id} - Met à jour un article
# Status code: 200 si trouvé, 404 sinon
# Paramètres: article_id (int), article (Article)
# Si non trouvé, retourner: {"error": "Article non trouvé"}


# TODO: Route DELETE /articles/{article_id} - Supprime un article
# Status code: 200 si trouvé, 404 sinon
# Si trouvé, retourner: {"message": "Article supprimé"}
# Si non trouvé, retourner: {"error": "Article non trouvé"}