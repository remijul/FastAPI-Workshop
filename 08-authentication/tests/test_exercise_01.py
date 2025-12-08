"""
Tests pour l'exercice 1 : Blog avec authentification.
"""

import os
import sys
from fastapi.testclient import TestClient


def setup_module():
    """Nettoie la base avant les tests."""
    db_path = "databases/exercise_01.db"
    if os.path.exists(db_path):
        os.remove(db_path)


def test_register():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    user_data = {
        "username": "alice",
        "password": "secret123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    assert "créé" in response.json()["message"].lower()


def test_register_duplicate():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    user_data = {"username": "bob", "password": "secret123"}
    client.post("/auth/register", json=user_data)
    
    # Essayer de créer le même
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400


def test_login():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    # Enregistrer
    user_data = {"username": "charlie", "password": "secret123"}
    client.post("/auth/register", json=user_data)
    
    # Login
    response = client.post("/auth/login", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    user_data = {"username": "diana", "password": "wrongpass"}
    response = client.post("/auth/login", json=user_data)
    assert response.status_code == 401


def test_get_articles_public():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    # Route publique (pas besoin de token)
    response = client.get("/articles")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_article_protected():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    # Essayer sans token
    article_data = {
        "title": "Mon article",
        "content": "Contenu de l'article"
    }
    response = client.post("/articles", json=article_data)
    assert response.status_code == 401


def test_create_article_with_auth():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    # Enregistrer et login
    user_data = {"username": "eve", "password": "secret123"}
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/login", json=user_data)
    token = login_response.json()["access_token"]
    
    # Créer article avec token
    headers = {"Authorization": f"Bearer {token}"}
    article_data = {
        "title": "Mon premier article",
        "content": "Contenu de mon premier article"
    }
    response = client.post("/articles", json=article_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Mon premier article"
    assert data["author"] == "eve"


def test_get_my_articles():
    from exercises.exercise_01_solution.main import app
    client = TestClient(app)
    
    # Enregistrer et login
    user_data = {"username": "frank", "password": "secret123"}
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/login", json=user_data)
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Créer 2 articles (avec contenu >= 10 caractères)
    article1 = {"title": "Article 1", "content": "Contenu de l'article 1"}
    article2 = {"title": "Article 2", "content": "Contenu de l'article 2"}
    client.post("/articles", json=article1, headers=headers)
    client.post("/articles", json=article2, headers=headers)
    
    # Récupérer mes articles
    response = client.get("/articles/my-articles", headers=headers)
    assert response.status_code == 200
    articles = response.json()
    assert len(articles) == 2
    assert all(a["author"] == "frank" for a in articles)