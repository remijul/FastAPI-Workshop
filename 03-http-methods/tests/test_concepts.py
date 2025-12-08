"""
Tests pour les concepts des méthodes HTTP.
"""

from fastapi.testclient import TestClient
from concepts.concepts_01_get_method import app as get_app
from concepts.concepts_02_post_method import app as post_app
from concepts.concepts_03_put_delete_methods import app as put_delete_app
from concepts.concepts_04_status_codes import app as status_app


# Tests GET method
def test_get_all_books():
    client = TestClient(get_app)
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


def test_get_book_by_id():
    client = TestClient(get_app)
    response = client.get("/books/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "title" in data


def test_get_book_not_found():
    client = TestClient(get_app)
    response = client.get("/books/999")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data


def test_search_books_by_author():
    client = TestClient(get_app)
    response = client.get("/books/search?author=Alice")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["author"] == "Alice"


# Tests POST method
def test_create_user():
    client = TestClient(post_app)
    user_data = {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 25
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert "id" in data


def test_create_user_validation():
    client = TestClient(post_app)
    # Données invalides (age manquant)
    user_data = {
        "name": "Bob",
        "email": "bob@example.com"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 422  # Validation error


def test_create_multiple_users():
    client = TestClient(post_app)
    users_data = [
        {"name": "Charlie", "email": "charlie@example.com", "age": 30},
        {"name": "Diana", "email": "diana@example.com", "age": 28}
    ]
    response = client.post("/users/bulk", json=users_data)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


# Tests PUT and DELETE methods
def test_update_product():
    client = TestClient(put_delete_app)
    updated_data = {
        "name": "Gaming Laptop",
        "price": 1299.99,
        "stock": 5
    }
    response = client.put("/products/1", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Gaming Laptop"
    assert data["price"] == 1299.99


def test_update_product_not_found():
    client = TestClient(put_delete_app)
    updated_data = {
        "name": "Ghost Product",
        "price": 99.99,
        "stock": 1
    }
    response = client.put("/products/999", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert "error" in data


def test_delete_product():
    client = TestClient(put_delete_app)
    response = client.delete("/products/2")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


# Tests status codes
def test_create_item_status_201():
    client = TestClient(status_app)
    response = client.post("/items?name=Test&price=10.0")
    assert response.status_code == 201


def test_get_item_not_found_status_404():
    client = TestClient(status_app)
    response = client.get("/items/999")
    assert response.status_code == 404


def test_delete_item_status_204():
    client = TestClient(status_app)
    # Créer d'abord un item
    client.post("/items?name=ToDelete&price=5.0")
    # Le supprimer
    response = client.delete("/items/1")
    assert response.status_code == 204