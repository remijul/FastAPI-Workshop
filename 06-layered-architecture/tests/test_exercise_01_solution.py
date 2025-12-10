"""
Tests pour la solution de l'exercice 1.
"""

import os
import sys
from fastapi.testclient import TestClient


def setup_module():
    """Nettoie la base avant les tests."""
    db_path = "databases/exercise_01.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Forcer le rechargement
    if 'exercises.exercise_01_solution.main' in sys.modules:
        del sys.modules['exercises.exercise_01_solution.main']
        del sys.modules['exercises.exercise_01_solution.database']
        del sys.modules['exercises.exercise_01_solution.repositories']
        del sys.modules['exercises.exercise_01_solution.services']
        del sys.modules['exercises.exercise_01_solution.routes']
        del sys.modules['exercises.exercise_01_solution.models']


def test_create_note():
    from exercises.exercise_01_solution.main import app
    client = TestClient(app)
    
    note_data = {
        "student_name": "Alice Dupont",
        "subject": "Mathématiques",
        "grade": 15.5
    }
    response = client.post("/notes", json=note_data)
    assert response.status_code == 201
    data = response.json()
    assert data["student_name"] == "Alice Dupont"
    assert data["passed"] is True
    assert "id" in data


def test_create_note_failed():
    from exercises.exercise_01_solution.main import app
    client = TestClient(app)
    
    note_data = {
        "student_name": "Bob Martin",
        "subject": "Histoire",
        "grade": 8.0
    }
    response = client.post("/notes", json=note_data)
    assert response.status_code == 201
    data = response.json()
    assert data["passed"] is False


def test_get_all_notes():
    from exercises.exercise_01_solution.main import app
    client = TestClient(app)
    
    response = client.get("/notes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "passed" in data[0]


def test_get_note_by_id():
    from exercises.exercise_01_solution.main import app
    client = TestClient(app)
    
    note_data = {
        "student_name": "Diana Leroy",
        "subject": "Anglais",
        "grade": 12.5
    }
    create_response = client.post("/notes", json=note_data)
    note_id = create_response.json()["id"]
    
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["passed"] is True


def test_get_note_not_found():
    from exercises.exercise_01_solution.main import app
    client = TestClient(app)
    
    response = client.get("/notes/9999")
    assert response.status_code == 404