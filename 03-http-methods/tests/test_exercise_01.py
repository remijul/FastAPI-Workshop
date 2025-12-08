"""
Tests pour l'exercice 1 : API CRUD d'articles de blog
"""

from fastapi.testclient import TestClient
from exercises.exercise_01 import app

client = TestClient(app)


def test_get_all_articles_empty():
    response = client.get("/articles")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_article():
    article_data = {
        "title": "Mon premier article",
        "content": "Contenu de l'article",
        "author": "Alice"
    }
    response = client.post("/articles", json=article_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Mon premier article"
    assert "id" in data


def test_get_article_by_id():
    # Créer d'abord un article
    article_data = {
        "title": "Article test",
        "content": "Contenu test",
        "author": "Bob"
    }
    create_response = client.post("/articles", json=article_data)
    article_id = create_response.json()["id"]
    
    # Récupérer l'article
    response = client.get(f"/articles/{article_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == article_id
    assert data["title"] == "Article test"


def test_get_article_not_found():
    response = client.get("/articles/9999")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data


def test_update_article():
    # Créer un article
    article_data = {
        "title": "Article original",
        "content": "Contenu original",
        "author": "Charlie"
    }
    create_response = client.post("/articles", json=article_data)
    article_id = create_response.json()["id"]
    
    # Mettre à jour l'article
    updated_data = {
        "title": "Article modifié",
        "content": "Contenu modifié",
        "author": "Charlie"
    }
    response = client.put(f"/articles/{article_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Article modifié"


def test_update_article_not_found():
    updated_data = {
        "title": "Article fantôme",
        "content": "Contenu fantôme",
        "author": "Ghost"
    }
    response = client.put("/articles/9999", json=updated_data)
    assert response.status_code == 404


def test_delete_article():
    # Créer un article
    article_data = {
        "title": "Article à supprimer",
        "content": "Sera supprimé",
        "author": "Diana"
    }
    create_response = client.post("/articles", json=article_data)
    article_id = create_response.json()["id"]
    
    # Supprimer l'article
    response = client.delete(f"/articles/{article_id}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    # Vérifier qu'il n'existe plus
    get_response = client.get(f"/articles/{article_id}")
    assert get_response.status_code == 404


def test_delete_article_not_found():
    response = client.delete("/articles/9999")
    assert response.status_code == 404