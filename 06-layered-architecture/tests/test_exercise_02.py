"""
Tests pour l'exercice 2 : API de gestion de tâches.
"""

import os
from fastapi.testclient import TestClient


def setup_module():
    """Nettoie la base avant les tests."""
    db_path = "databases/exercise_02.db"
    if os.path.exists(db_path):
        os.remove(db_path)


def test_create_task():
    from exercises.exercise_02.main import app
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
    assert data["priority"] == 5
    assert data["priority_label"] == "Haute"  # 4-5 = Haute
    assert data["completed"] is False
    assert "id" in data


def test_create_task_priority_labels():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    # Priorité basse (1-2)
    task_data = {"title": "Tâche basse", "priority": 1, "completed": False}
    response = client.post("/tasks", json=task_data)
    assert response.json()["priority_label"] == "Basse"
    
    # Priorité moyenne (3)
    task_data = {"title": "Tâche moyenne", "priority": 3, "completed": False}
    response = client.post("/tasks", json=task_data)
    assert response.json()["priority_label"] == "Moyenne"
    
    # Priorité haute (4-5)
    task_data = {"title": "Tâche haute", "priority": 4, "completed": False}
    response = client.post("/tasks", json=task_data)
    assert response.json()["priority_label"] == "Haute"


def test_create_task_validation():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    # Priorité invalide (> 5)
    task_data = {
        "title": "Tâche invalide",
        "priority": 10,
        "completed": False
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 422


def test_get_all_tasks():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Vérifier que priority_label est présent
    assert "priority_label" in data[0]


def test_get_task_by_id():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    # Créer une tâche
    task_data = {
        "title": "Tâche de test",
        "priority": 3,
        "completed": False
    }
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Récupérer la tâche
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["priority_label"] == "Moyenne"


def test_get_task_not_found():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    response = client.get("/tasks/9999")
    assert response.status_code == 404


def test_complete_task():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    # Créer une tâche
    task_data = {
        "title": "Tâche à compléter",
        "priority": 2,
        "completed": False
    }
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    assert create_response.json()["completed"] is False
    
    # Compléter la tâche
    response = client.put(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["priority_label"] == "Basse"


def test_complete_task_not_found():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    response = client.put("/tasks/9999/complete")
    assert response.status_code == 404