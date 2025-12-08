"""
Tests pour les concepts FastAPI de base.
"""

from fastapi.testclient import TestClient
from concepts.concepts_01_hello_world import app as hello_app
from concepts.concepts_02_path_parameters import app as path_app
from concepts.concepts_03_query_parameters import app as query_app


# Tests pour Hello World
def test_hello_world():
    client = TestClient(hello_app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_health_check():
    client = TestClient(hello_app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_info():
    client = TestClient(hello_app)
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


# Tests pour les paramètres de chemin
def test_get_user():
    client = TestClient(path_app)
    response = client.get("/users/123")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 123
    assert "username" in data


def test_get_product():
    client = TestClient(path_app)
    response = client.get("/products/5")
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == 5
    assert data["price"] == 50.0


def test_get_item_by_name():
    client = TestClient(path_app)
    response = client.get("/items/laptop")
    assert response.status_code == 200
    data = response.json()
    assert data["item_name"] == "laptop"


# Tests pour les paramètres de requête
def test_search_items():
    client = TestClient(query_app)
    response = client.get("/search?query=laptop&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "laptop"
    assert data["limit"] == 5
    assert len(data["results"]) > 0


def test_search_items_default_limit():
    client = TestClient(query_app)
    response = client.get("/search?query=phone")
    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 10


def test_list_products_no_filter():
    client = TestClient(query_app)
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert len(data["products"]) > 0


def test_list_products_with_category():
    client = TestClient(query_app)
    response = client.get("/products?category=electronics")
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "electronics"


def test_calculate_add():
    client = TestClient(query_app)
    response = client.get("/calculate?a=10&b=5&operation=add")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 15.0


def test_calculate_divide():
    client = TestClient(query_app)
    response = client.get("/calculate?a=10&b=2&operation=divide")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 5.0