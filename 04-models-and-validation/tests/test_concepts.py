"""
Tests pour les concepts de validation Pydantic.
"""

from fastapi.testclient import TestClient
from concepts.concepts_01_basic_models import app as basic_app
from concepts.concepts_02_field_validation import app as validation_app
from concepts.concepts_03_nested_models import app as nested_app
from concepts.concepts_04_response_models import app as response_app


# Tests modèles de base
def test_create_simple_book():
    client = TestClient(basic_app)
    book_data = {
        "title": "Python 101",
        "author": "Alice",
        "pages": 300,
        "year": 2023
    }
    response = client.post("/books/simple", json=book_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Python 101"


def test_create_simple_book_missing_field():
    client = TestClient(basic_app)
    book_data = {
        "title": "Python 101",
        "author": "Alice"
        # pages et year manquants
    }
    response = client.post("/books/simple", json=book_data)
    assert response.status_code == 422


def test_create_book_with_defaults():
    client = TestClient(basic_app)
    book_data = {
        "title": "FastAPI",
        "author": "Bob"
    }
    response = client.post("/books/with-defaults", json=book_data)
    assert response.status_code == 200
    data = response.json()
    assert data["pages"] == 0
    assert data["year"] == 2024
    assert data["available"] is True


def test_create_book_optional():
    client = TestClient(basic_app)
    book_data = {
        "title": "Django",
        "author": "Charlie"
    }
    response = client.post("/books/optional", json=book_data)
    assert response.status_code == 200
    data = response.json()
    assert data["pages"] is None


# Tests validation des champs
def test_create_user_valid():
    client = TestClient(validation_app)
    user_data = {
        "username": "alice",
        "email": "alice@example.com",
        "age": 25
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 200


def test_create_user_username_too_short():
    client = TestClient(validation_app)
    user_data = {
        "username": "ab",  # Trop court (min 3)
        "email": "alice@example.com",
        "age": 25
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 422


def test_create_user_invalid_email():
    client = TestClient(validation_app)
    user_data = {
        "username": "alice",
        "email": "not-an-email",
        "age": 25
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 422


def test_create_user_age_out_of_range():
    client = TestClient(validation_app)
    user_data = {
        "username": "alice",
        "email": "alice@example.com",
        "age": 150  # Trop élevé (max 120)
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 422


def test_create_product_valid():
    client = TestClient(validation_app)
    product_data = {
        "name": "Laptop",
        "price": 999.99,
        "stock": 10,
        "discount": 15.0
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 200


def test_create_product_negative_price():
    client = TestClient(validation_app)
    product_data = {
        "name": "Laptop",
        "price": 0,  # Doit être > 0
        "stock": 10
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 422


def test_create_article_tags_lowercase():
    client = TestClient(validation_app)
    article_data = {
        "title": "Mon article",
        "content": "Contenu de l'article",
        "tags": ["Python", "FastAPI", "WEB"]
    }
    response = client.post("/articles", json=article_data)
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == ["python", "fastapi", "web"]


# Tests modèles imbriqués
def test_create_customer_nested():
    client = TestClient(nested_app)
    customer_data = {
        "name": "Alice",
        "address": {
            "street": "10 rue de Paris",
            "city": "Lyon",
            "postal_code": "69000"
        },
        "contact": {
            "email": "alice@example.com",
            "phone": "0612345678"
        }
    }
    response = client.post("/customers", json=customer_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["address"]["city"] == "Lyon"


def test_create_order_with_items():
    client = TestClient(nested_app)
    order_data = {
        "customer_name": "Bob",
        "items": [
            {"product_name": "Laptop", "quantity": 1, "unit_price": 999.99},
            {"product_name": "Mouse", "quantity": 2, "unit_price": 25.50}
        ]
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1050.99


# Tests response models
def test_create_user_no_password_in_response():
    client = TestClient(response_app)
    user_data = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "secret123456",
        "age": 25
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert "password" not in data  # Le password est filtré !
    assert data["username"] == "alice"
    assert "id" in data


def test_get_all_users_no_passwords():
    client = TestClient(response_app)
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    for user in data:
        assert "password" not in user


def test_create_product_with_calculated_fields():
    client = TestClient(response_app)
    product_data = {
        "name": "Laptop",
        "price": 100.0,
        "stock": 5
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["total_value"] == 500.0
    assert data["in_stock"] is True