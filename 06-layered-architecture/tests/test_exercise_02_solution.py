"""
Tests pour la solution de l'exercice 2.
"""

import os
import sys
from fastapi.testclient import TestClient


def setup_module():
    """Nettoie la base avant les tests."""
    db_path = "databases/exercise_02.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Forcer le rechargement
    if 'exercises.exercise_02_solution.main' in sys.modules:
        del sys.modules['exercises.exercise_02_solution.main']
        del sys.modules['exercises.exercise_02_solution.database']
        del sys.modules['exercises.exercise_02_solution.repositories']
        del sys.modules['exercises.exercise_02_solution.services']
        del sys.modules['exercises.exercise_02_solution.routes']
        del sys.modules['exercises.exercise_02_solution.models']


def test_create_task():
    from exercises.exercise_02_solution.main import app
    client = TestClient(app)
    
    task_data = {
        "title": "Apprendre FastAPI",
        "priority": 5,
        "completed": False
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Apprendre FastAPI"
    assert data["priority_label"] == "Haute"
    assert data["completed"] is False


def test_create_task_priority_labels():
    from exercises.exercise_02_solution.main import app
    client = TestClient(app)
    
    task_data = {"title": "Tâche basse", "priority": 1, "completed": False}
    response = client.post("/tasks", json=task_data)
    assert response.json()["priority_label"] == "Basse"
    
    task_data = {"title": "Tâche moyenne", "priority": 3, "completed": False}
    response = client.post("/tasks", json=task_data)
    assert response.json()["priority_label"] == "Moyenne"


def test_get_all_tasks():
    from exercises.exercise_02_solution.main import app
    client = TestClient(app)
    
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "priority_label" in data[0]


def test_complete_task():
    from exercises.exercise_02_solution.main import app
    client = TestClient(app)
    
    task_data = {
        "title": "Tâche à compléter",
        "priority": 2,
        "completed": False
    }
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    response = client.put(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True