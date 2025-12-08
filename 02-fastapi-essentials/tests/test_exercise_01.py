"""
Tests pour l'exercice 1 : API de gestion de tâches
"""

from fastapi.testclient import TestClient
from exercises.exercise_01 import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API de gestion de tâches"}


def test_get_all_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]["id"] == 1
    assert "title" in data[0]
    assert "completed" in data[0]


def test_get_task_by_id():
    response = client.get("/tasks/5")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 5
    assert data["title"] == "Tâche 5"
    assert data["completed"] is False


def test_search_tasks_all():
    response = client.get("/tasks/search")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "all"
    assert data["count"] == 3


def test_search_tasks_completed():
    response = client.get("/tasks/search?status=completed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["count"] == 3


def test_search_tasks_pending():
    response = client.get("/tasks/search?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
    assert data["count"] == 3