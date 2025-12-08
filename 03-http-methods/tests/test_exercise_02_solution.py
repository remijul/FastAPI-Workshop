"""
Tests pour l'exercice 2 : API de gestion d'inventaire
"""

from fastapi.testclient import TestClient
from exercises.exercise_02_solution import app

client = TestClient(app)


def test_get_inventory_empty():
    response = client.get("/inventory")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_product():
    product_data = {
        "name": "Laptop",
        "price": 999.99,
        "quantity": 10
    }
    response = client.post("/inventory", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["quantity"] == 10
    assert "id" in data


def test_get_product_by_id():
    # Créer un produit
    product_data = {
        "name": "Mouse",
        "price": 25.50,
        "quantity": 50
    }
    create_response = client.post("/inventory", json=product_data)
    product_id = create_response.json()["id"]
    
    # Récupérer le produit
    response = client.get(f"/inventory/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id


def test_get_product_not_found():
    response = client.get("/inventory/9999")
    assert response.status_code == 404


def test_restock_product():
    # Créer un produit
    product_data = {
        "name": "Keyboard",
        "price": 75.00,
        "quantity": 5
    }
    create_response = client.post("/inventory", json=product_data)
    product_id = create_response.json()["id"]
    
    # Réapprovisionner
    response = client.put(f"/inventory/{product_id}/restock?quantity=10")
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 15  # 5 + 10


def test_restock_product_not_found():
    response = client.put("/inventory/9999/restock?quantity=10")
    assert response.status_code == 404


def test_sell_product():
    # Créer un produit
    product_data = {
        "name": "Monitor",
        "price": 200.00,
        "quantity": 20
    }
    create_response = client.post("/inventory", json=product_data)
    product_id = create_response.json()["id"]
    
    # Vendre
    response = client.put(f"/inventory/{product_id}/sell?quantity=5")
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 15  # 20 - 5


def test_sell_product_insufficient_stock():
    # Créer un produit avec peu de stock
    product_data = {
        "name": "Headset",
        "price": 50.00,
        "quantity": 2
    }
    create_response = client.post("/inventory", json=product_data)
    product_id = create_response.json()["id"]
    
    # Essayer de vendre plus que le stock
    response = client.put(f"/inventory/{product_id}/sell?quantity=10")
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


def test_sell_product_not_found():
    response = client.put("/inventory/9999/sell?quantity=1")
    assert response.status_code == 404


def test_delete_product():
    # Créer un produit
    product_data = {
        "name": "Cable",
        "price": 10.00,
        "quantity": 100
    }
    create_response = client.post("/inventory", json=product_data)
    product_id = create_response.json()["id"]
    
    # Supprimer
    response = client.delete(f"/inventory/{product_id}")
    assert response.status_code == 200
    
    # Vérifier qu'il n'existe plus
    get_response = client.get(f"/inventory/{product_id}")
    assert get_response.status_code == 404


def test_delete_product_not_found():
    response = client.delete("/inventory/9999")
    assert response.status_code == 404