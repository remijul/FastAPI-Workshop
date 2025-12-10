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
    modules_to_delete = [
        'exercises.exercise_01_solution.main',
        'exercises.exercise_01_solution.database',
        'exercises.exercise_01_solution.repositories',
        'exercises.exercise_01_solution.services',
        'exercises.exercise_01_solution.routes',
        'exercises.exercise_01_solution.models',
        'exercises.exercise_01_solution.exceptions'
    ]
    for module in modules_to_delete:
        if module in sys.modules:
            del sys.modules[module]


def test_create_account():
    from exercises.exercise_01_solution.main import app
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


def test_get_account_not_found():
    from exercises.exercise_01_solution.main import app
    client = TestClient(app)
    
    response = client.get("/accounts/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "Account Not Found"


def test_deposit():
    from exercises.exercise_01_solution.main import app
    client = TestClient(app)
    
    account_data = {"owner_name": "Charlie", "initial_balance": 100.0}
    create_response = client.post("/accounts", json=account_data)
    account_id = create_response.json()["id"]
    
    transaction = {"amount": 50.0}
    response = client.post(f"/accounts/{account_id}/deposit", json=transaction)
    assert response.status_code == 200
    assert response.json()["balance"] == 150.0


def test_withdraw_insufficient_funds():
    from exercises.exercise_01_solution.main import app
    client = TestClient(app)
    
    account_data = {"owner_name": "Eve", "initial_balance": 10.0}
    create_response = client.post("/accounts", json=account_data)
    account_id = create_response.json()["id"]
    
    transaction = {"amount": 100.0}
    response = client.post(f"/accounts/{account_id}/withdraw", json=transaction)
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Insufficient Funds"
    assert data["balance"] == 10.0
    assert data["requested"] == 100.0