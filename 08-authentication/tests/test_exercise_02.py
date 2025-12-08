"""
Tests pour l'exercice 2 : Tâches avec rôles.
"""

import os
import sys
from fastapi.testclient import TestClient


def setup_module():
    """Nettoie la base avant les tests."""
    db_path = "databases/exercise_02.db"
    if os.path.exists(db_path):
        os.remove(db_path)


def test_register_user():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    user_data = {
        "username": "user1",
        "password": "secret123",
        "role": "user"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200


def test_register_admin():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    admin_data = {
        "username": "admin1",
        "password": "admin123",
        "role": "admin"
    }
    response = client.post("/auth/register", json=admin_data)
    assert response.status_code == 200


def test_create_task():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    # Enregistrer et login
    user_data = {"username": "user2", "password": "secret123", "role": "user"}
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/login", json={"username": "user2", "password": "secret123"})
    token = login_response.json()["access_token"]
    
    # Créer une tâche
    headers = {"Authorization": f"Bearer {token}"}
    task_data = {
        "title": "Ma tâche",
        "description": "Description de la tâche"
    }
    response = client.post("/tasks", json=task_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Ma tâche"
    assert data["owner"] == "user2"


def test_get_my_tasks():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    # Enregistrer et login
    user_data = {"username": "user3", "password": "secret123", "role": "user"}
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/login", json={"username": "user3", "password": "secret123"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Créer des tâches
    task1 = {"title": "Tâche 1", "description": "Description 1"}
    task2 = {"title": "Tâche 2", "description": "Description 2"}
    client.post("/tasks", json=task1, headers=headers)
    client.post("/tasks", json=task2, headers=headers)
    
    # Récupérer mes tâches
    response = client.get("/tasks/my-tasks", headers=headers)
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2


def test_get_all_tasks_user_forbidden():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    # Utilisateur normal
    user_data = {"username": "user4", "password": "secret123", "role": "user"}
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/login", json={"username": "user4", "password": "secret123"})
    token = login_response.json()["access_token"]
    
    # Essayer d'accéder à /tasks/all (admin only)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/tasks/all", headers=headers)
    assert response.status_code == 403


def test_get_all_tasks_admin_allowed():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    # Admin
    admin_data = {"username": "admin2", "password": "admin123", "role": "admin"}
    client.post("/auth/register", json=admin_data)
    login_response = client.post("/auth/login", json={"username": "admin2", "password": "admin123"})
    token = login_response.json()["access_token"]
    
    # Accéder à /tasks/all (admin only)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/tasks/all", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_task_admin():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    # Créer un utilisateur et une tâche
    user_data = {"username": "user5", "password": "secret123", "role": "user"}
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/login", json={"username": "user5", "password": "secret123"})
    user_token = login_response.json()["access_token"]
    
    task_data = {"title": "Tâche à supprimer", "description": "Description"}
    create_response = client.post("/tasks", json=task_data, headers={"Authorization": f"Bearer {user_token}"})
    task_id = create_response.json()["id"]
    
    # Admin supprime la tâche
    admin_data = {"username": "admin3", "password": "admin123", "role": "admin"}
    client.post("/auth/register", json=admin_data)
    login_response = client.post("/auth/login", json={"username": "admin3", "password": "admin123"})
    admin_token = login_response.json()["access_token"]
    
    response = client.delete(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200