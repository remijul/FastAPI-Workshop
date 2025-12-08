"""
Tests pour l'exercice 1 : API de notes d'étudiants.
"""

import os
from fastapi.testclient import TestClient


def setup_module():
    """Nettoie la base avant les tests."""
    db_path = "databases/exercise_01.db"
    if os.path.exists(db_path):
        os.remove(db_path)


def test_create_note():
    from exercises.exercise_01.main import app
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
    assert data["passed"] is True  # grade >= 10
    assert "id" in data


def test_create_note_failed():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    note_data = {
        "student_name": "Bob Martin",
        "subject": "Histoire",
        "grade": 8.0
    }
    response = client.post("/notes", json=note_data)
    assert response.status_code == 201
    data = response.json()
    assert data["passed"] is False  # grade < 10


def test_create_note_validation():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    # Grade invalide (> 20)
    note_data = {
        "student_name": "Charlie",
        "subject": "Sciences",
        "grade": 25.0
    }
    response = client.post("/notes", json=note_data)
    assert response.status_code == 422


def test_get_all_notes():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    response = client.get("/notes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Vérifier que passed est présent
    assert "passed" in data[0]


def test_get_note_by_id():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    # Créer une note
    note_data = {
        "student_name": "Diana Leroy",
        "subject": "Anglais",
        "grade": 12.5
    }
    create_response = client.post("/notes", json=note_data)
    note_id = create_response.json()["id"]
    
    # Récupérer la note
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["passed"] is True


def test_get_note_not_found():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    response = client.get("/notes/9999")
    assert response.status_code == 404