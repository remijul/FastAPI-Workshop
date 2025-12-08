"""
Tests pour l'exercice 2 : Réservation d'hôtel.
"""

import os
import sys
from fastapi.testclient import TestClient


def setup_module():
    """Nettoie la base avant les tests."""
    db_path = "databases/exercise_02.db"
    if os.path.exists(db_path):
        os.remove(db_path)


def test_create_room():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    room_data = {
        "name": "Chambre Deluxe",
        "capacity": 2,
        "price_per_night": 150.0
    }
    response = client.post("/rooms", json=room_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Chambre Deluxe"
    assert data["available"] is True
    assert "id" in data


def test_get_room():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    # Créer une chambre
    room_data = {"name": "Suite", "capacity": 4, "price_per_night": 300.0}
    create_response = client.post("/rooms", json=room_data)
    room_id = create_response.json()["id"]
    
    # Récupérer la chambre
    response = client.get(f"/rooms/{room_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Suite"


def test_get_room_not_found():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    response = client.get("/rooms/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "Room Not Found"


def test_create_reservation():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    # Créer une chambre
    room_data = {"name": "Chambre Standard", "capacity": 2, "price_per_night": 100.0}
    room_response = client.post("/rooms", json=room_data)
    room_id = room_response.json()["id"]
    
    # Créer une réservation
    reservation_data = {
        "room_id": room_id,
        "guest_name": "Alice Dupont",
        "nights": 3
    }
    response = client.post("/reservations", json=reservation_data)
    assert response.status_code == 201
    data = response.json()
    assert data["guest_name"] == "Alice Dupont"
    assert data["nights"] == 3
    assert data["total_price"] == 300.0  # 100 * 3


def test_reservation_room_not_found():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    reservation_data = {
        "room_id": 9999,
        "guest_name": "Bob Martin",
        "nights": 2
    }
    response = client.post("/reservations", json=reservation_data)
    assert response.status_code == 404
    assert response.json()["error"] == "Room Not Found"


def test_reservation_room_not_available():
    from exercises.exercise_02.main import app
    client = TestClient(app)
    
    # Créer une chambre
    room_data = {"name": "Chambre Test", "capacity": 2, "price_per_night": 80.0}
    room_response = client.post("/rooms", json=room_data)
    room_id = room_response.json()["id"]
    
    # Première réservation (marque la chambre comme indisponible)
    reservation_data = {
        "room_id": room_id,
        "guest_name": "Charlie",
        "nights": 1
    }
    client.post("/reservations", json=reservation_data)
    
    # Essayer une deuxième réservation
    reservation_data2 = {
        "room_id": room_id,
        "guest_name": "Diana",
        "nights": 1
    }
    response = client.post("/reservations", json=reservation_data2)
    assert response.status_code == 400
    assert response.json()["error"] == "Room Not Available"