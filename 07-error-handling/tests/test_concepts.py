"""
Tests pour les concepts de gestion d'erreurs.
"""

from fastapi.testclient import TestClient


def test_http_exception_404():
    """Test HTTPException 404."""
    from concepts.concepts_01_http_exceptions import app
    client = TestClient(app)
    
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "non trouvé" in response.json()["detail"].lower()


def test_http_exception_400():
    """Test HTTPException 400 pour username existant."""
    from concepts.concepts_01_http_exceptions import app
    client = TestClient(app)
    
    # Créer un utilisateur
    user_data = {"username": "alice", "email": "alice@example.com"}
    client.post("/users", json=user_data)
    
    # Essayer de créer le même
    response = client.post("/users", json=user_data)
    assert response.status_code == 400
    assert "existe déjà" in response.json()["detail"].lower()


def test_http_exception_403():
    """Test HTTPException 403 pour suppression admin."""
    from concepts.concepts_01_http_exceptions import app
    client = TestClient(app)
    
    # Créer l'admin (id=1)
    user_data = {"username": "admin", "email": "admin@example.com"}
    client.post("/users", json=user_data)
    
    # Essayer de supprimer
    response = client.delete("/users/1")
    assert response.status_code == 403
    assert "admin" in response.json()["detail"].lower()


def test_custom_exception_product_not_found():
    """Test exception personnalisée ProductNotFoundError."""
    from concepts.concepts_02_custom_exceptions import app
    client = TestClient(app)
    
    response = client.get("/products/999")
    assert response.status_code == 404
    assert response.json()["error"] == "Product Not Found"
    assert response.json()["product_id"] == 999


def test_custom_exception_insufficient_stock():
    """Test exception personnalisée InsufficientStockError."""
    from concepts.concepts_02_custom_exceptions import app
    client = TestClient(app)
    
    # Essayer de vendre plus que le stock disponible
    sell_data = {"quantity": 100}
    response = client.post("/products/1/sell", json=sell_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Insufficient Stock"
    assert "requested" in response.json()
    assert "available" in response.json()


def test_middleware_normal_request():
    """Test middleware avec requête normale."""
    from concepts.concepts_03_error_middleware import app
    client = TestClient(app)
    
    response = client.get("/")
    assert response.status_code == 200


def test_middleware_catches_errors():
    """Test que le middleware capture les erreurs."""
    from concepts.concepts_03_error_middleware import app
    client = TestClient(app)
    
    # Cette route déclenche volontairement une erreur
    response = client.get("/error")
    assert response.status_code == 500
    assert response.json()["error"] == "Internal Server Error"


def test_middleware_catches_key_error():
    """Test que le middleware capture les KeyError."""
    from concepts.concepts_03_error_middleware import app
    client = TestClient(app)
    
    # Item qui n'existe pas → KeyError
    response = client.get("/items/999")
    assert response.status_code == 500
    assert "error" in response.json()