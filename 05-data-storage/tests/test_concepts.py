"""
Tests pour les concepts SQLite.
"""

import os
from fastapi.testclient import TestClient


def test_concepts_01_create_and_count():
    """Test du concept 1 : création et comptage."""
    # Nettoyer la base avant le test
    db_path = "databases/concepts_01.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    from concepts.concepts_01_sqlite_basics import app
    client = TestClient(app)
    
    # Compter (doit être 0)
    response = client.get("/products/count")
    assert response.status_code == 200
    assert response.json()["count"] == 0
    
    # Créer un produit
    response = client.post("/products/create?name=Laptop&price=999.99&stock=5")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["id"] > 0
    
    # Compter (doit être 1)
    response = client.get("/products/count")
    assert response.json()["count"] == 1


def test_concepts_02_crud():
    """Test du concept 2 : opérations CRUD."""
    db_path = "databases/concepts_02.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    from concepts.concepts_02_crud_operations import app
    client = TestClient(app)
    
    # CREATE
    response = client.post("/users?username=alice&email=alice@example.com")
    assert response.status_code == 201
    user_id = response.json()["id"]
    
    # READ all
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    # READ one
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "alice"
    
    # UPDATE
    response = client.put(f"/users/{user_id}?email=alice.new@example.com")
    assert response.status_code == 200
    assert response.json()["email"] == "alice.new@example.com"
    
    # DELETE
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    
    # READ all (doit être vide après suppression)
    response = client.get("/users")
    assert len(response.json()) == 0


def test_concepts_03_integration():
    """Test du concept 3 : intégration FastAPI."""
    db_path = "databases/concepts_03.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    from concepts.concepts_03_fastapi_integration import app
    client = TestClient(app)
    
    # Créer une tâche
    task_data = {
        "title": "Apprendre FastAPI",
        "description": "Suivre le workshop",
        "completed": False
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    task_id = response.json()["id"]
    
    # Lister les tâches
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    # Compléter la tâche
    response = client.put(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True