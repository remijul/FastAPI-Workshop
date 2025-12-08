"""
Tests pour l'exercice 1 : Système de gestion d'étudiants
"""

from fastapi.testclient import TestClient
from exercises.exercise_01 import app

client = TestClient(app)


def test_create_student_valid():
    student_data = {
        "first_name": "Alice",
        "last_name": "Dupont",
        "email": "alice@example.com",
        "age": 20,
        "grade": 15.5
    }
    response = client.post("/students", json=student_data)
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Alice"
    assert data["status"] == "Admis"
    assert "id" in data


def test_create_student_failed_status():
    student_data = {
        "first_name": "Bob",
        "last_name": "Martin",
        "email": "bob@example.com",
        "age": 19,
        "grade": 8.0
    }
    response = client.post("/students", json=student_data)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "Refusé"


def test_create_student_first_name_too_short():
    student_data = {
        "first_name": "A",  # Trop court
        "last_name": "Dupont",
        "email": "test@example.com",
        "age": 20,
        "grade": 12.0
    }
    response = client.post("/students", json=student_data)
    assert response.status_code == 422


def test_create_student_age_too_young():
    student_data = {
        "first_name": "Charlie",
        "last_name": "Dubois",
        "email": "charlie@example.com",
        "age": 15,  # Trop jeune (min 16)
        "grade": 12.0
    }
    response = client.post("/students", json=student_data)
    assert response.status_code == 422


def test_create_student_grade_out_of_range():
    student_data = {
        "first_name": "Diana",
        "last_name": "Leroy",
        "email": "diana@example.com",
        "age": 20,
        "grade": 25.0  # Trop élevé (max 20)
    }
    response = client.post("/students", json=student_data)
    assert response.status_code == 422


def test_get_all_students():
    response = client.get("/students")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_student_by_id():
    # Créer un étudiant d'abord
    student_data = {
        "first_name": "Eve",
        "last_name": "Blanc",
        "email": "eve@example.com",
        "age": 22,
        "grade": 14.0
    }
    create_response = client.post("/students", json=student_data)
    student_id = create_response.json()["id"]
    
    # Récupérer l'étudiant
    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Eve"


def test_get_student_not_found():
    response = client.get("/students/9999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data