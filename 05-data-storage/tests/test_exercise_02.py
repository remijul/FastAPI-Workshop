"""
Tests pour l'exercice 2 : API de blog.
"""

import os
from fastapi.testclient import TestClient


def setup_module():
    """Nettoie la base avant les tests."""
    db_path = "databases/exercise_02.db"
    if os.path.exists(db_path):
        os.remove(db_path)


def test_create_article():
    from exercises.exercise_02 import app
    client = TestClient(app)
    
    article_data = {
        "title": "Mon premier article",
        "content": "Contenu de l'article de blog",
        "author": "Alice"
    }
    response = client.post("/articles", json=article_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Mon premier article"
    assert data["published"] is False
    assert "id" in data
    assert "created_at" in data


def test_create_article_validation():
    from exercises.exercise_02 import app
    client = TestClient(app)
    
    # Title trop court
    article_data = {
        "title": "Test",
        "content": "Contenu valide",
        "author": "Bob"
    }
    response = client.post("/articles", json=article_data)
    assert response.status_code == 422


def test_get_article():
    from exercises.exercise_02 import app
    client = TestClient(app)
    
    # Créer un article
    article_data = {
        "title": "Article de test",
        "content": "Contenu de test pour l'article",
        "author": "Charlie"
    }
    create_response = client.post("/articles", json=article_data)
    article_id = create_response.json()["id"]
    
    # Récupérer l'article
    response = client.get(f"/articles/{article_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == article_id
    assert data["title"] == "Article de test"


def test_get_article_not_found():
    from exercises.exercise_02 import app
    client = TestClient(app)
    
    response = client.get("/articles/9999")
    assert response.status_code == 404


def test_publish_article():
    from exercises.exercise_02 import app
    client = TestClient(app)
    
    # Créer un article
    article_data = {
        "title": "Article à publier",
        "content": "Contenu de l'article à publier",
        "author": "Diana"
    }
    create_response = client.post("/articles", json=article_data)
    article_id = create_response.json()["id"]
    assert create_response.json()["published"] is False
    
    # Publier
    response = client.put(f"/articles/{article_id}/publish")
    assert response.status_code == 200
    data = response.json()
    assert data["published"] is True


def test_publish_article_not_found():
    from exercises.exercise_02 import app
    client = TestClient(app)
    
    response = client.put("/articles/9999/publish")
    assert response.status_code == 404

'''
**databases/.gitkeep**
'''
# Ce fichier permet de versionner le dossier databases vide
# Les fichiers .db seront créés automatiquement