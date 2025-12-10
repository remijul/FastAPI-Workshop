"""
Tests pour l'exercice 1 : API de contacts.
"""

import os
from fastapi.testclient import TestClient


def setup_module():
    """Nettoie la base avant les tests."""
    db_path = "databases/exercise_01.db"
    if os.path.exists(db_path):
        os.remove(db_path)


def test_create_contact():
    from exercises.exercise_01_solution import app
    client = TestClient(app)
    
    contact_data = {
        "name": "Alice Dupont",
        "email": "alice@example.com",
        "phone": "0612345678"
    }
    response = client.post("/contacts", json=contact_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice Dupont"
    assert data["email"] == "alice@example.com"
    assert "id" in data


def test_create_contact_validation():
    from exercises.exercise_01_solution import app
    client = TestClient(app)
    
    # Nom trop court
    contact_data = {
        "name": "A",
        "email": "test@example.com"
    }
    response = client.post("/contacts", json=contact_data)
    assert response.status_code == 422


def test_get_all_contacts():
    from exercises.exercise_01_solution import app
    client = TestClient(app)
    
    response = client.get("/contacts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_delete_contact():
    from exercises.exercise_01_solution import app
    client = TestClient(app)
    
    # Créer un contact
    contact_data = {
        "name": "Bob Martin",
        "email": "bob@example.com"
    }
    create_response = client.post("/contacts", json=contact_data)
    contact_id = create_response.json()["id"]
    
    # Supprimer
    response = client.delete(f"/contacts/{contact_id}")
    assert response.status_code == 200
    
    # Vérifier la suppression
    response = client.get("/contacts")
    contacts = response.json()
    assert not any(c["id"] == contact_id for c in contacts)


def test_delete_contact_not_found():
    from exercises.exercise_01_solution import app
    client = TestClient(app)
    
    response = client.delete("/contacts/9999")
    assert response.status_code == 404