"""
Tests pour l'exercice 1 : Gestion de comptes bancaires.
"""

import os
import sys
from fastapi.testclient import TestClient


def setup_module():
    """Nettoie la base avant les tests."""
    db_path = "databases/exercise_01.db"
    if os.path.exists(db_path):
        os.remove(db_path)


def test_create_account():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    account_data = {
        "owner_name": "Alice Dupont",
        "initial_balance": 1000.0
    }
    response = client.post("/accounts", json=account_data)
    assert response.status_code == 201
    data = response.json()
    assert data["owner_name"] == "Alice Dupont"
    assert data["balance"] == 1000.0
    assert "id" in data


def test_get_account():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    # Créer un compte
    account_data = {"owner_name": "Bob Martin", "initial_balance": 500.0}
    create_response = client.post("/accounts", json=account_data)
    account_id = create_response.json()["id"]
    
    # Récupérer le compte
    response = client.get(f"/accounts/{account_id}")
    assert response.status_code == 200
    assert response.json()["balance"] == 500.0


def test_get_account_not_found():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    response = client.get("/accounts/9999")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"] == "Account Not Found"


def test_deposit():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    # Créer un compte
    account_data = {"owner_name": "Charlie", "initial_balance": 100.0}
    create_response = client.post("/accounts", json=account_data)
    account_id = create_response.json()["id"]
    
    # Déposer de l'argent
    transaction = {"amount": 50.0}
    response = client.post(f"/accounts/{account_id}/deposit", json=transaction)
    assert response.status_code == 200
    assert response.json()["balance"] == 150.0


def test_withdraw_success():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    # Créer un compte avec solde
    account_data = {"owner_name": "Diana", "initial_balance": 200.0}
    create_response = client.post("/accounts", json=account_data)
    account_id = create_response.json()["id"]
    
    # Retirer de l'argent
    transaction = {"amount": 50.0}
    response = client.post(f"/accounts/{account_id}/withdraw", json=transaction)
    assert response.status_code == 200
    assert response.json()["balance"] == 150.0


def test_withdraw_insufficient_funds():
    from exercises.exercise_01.main import app
    client = TestClient(app)
    
    # Créer un compte avec peu d'argent
    account_data = {"owner_name": "Eve", "initial_balance": 10.0}
    create_response = client.post("/accounts", json=account_data)
    account_id = create_response.json()["id"]
    
    # Essayer de retirer plus que le solde
    transaction = {"amount": 100.0}
    response = client.post(f"/accounts/{account_id}/withdraw", json=transaction)
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Insufficient Funds"
    assert "balance" in data