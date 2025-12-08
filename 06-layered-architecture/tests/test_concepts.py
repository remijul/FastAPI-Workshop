"""
Tests pour les concepts d'architecture en couches.
"""

import os
import sys
from fastapi.testclient import TestClient


def test_monolithic_api():
    """Test de l'API monolithique."""
    # Nettoyer la base
    db_path = "databases/monolithic.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    from concepts.concepts_01_monolithic import app
    client = TestClient(app)
    
    # Créer un produit
    product_data = {
        "name": "Laptop",
        "price": 999.99,
        "stock": 10
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 201
    product_id = response.json()["id"]
    
    # Récupérer le produit
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"


def test_layered_architecture():
    """Test de l'architecture en couches."""
    # Nettoyer la base
    db_path = "databases/layered.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Forcer le rechargement du module pour réinitialiser la base
    if 'concepts.concepts_02_layered.main' in sys.modules:
        del sys.modules['concepts.concepts_02_layered.main']
        del sys.modules['concepts.concepts_02_layered.database']
        del sys.modules['concepts.concepts_02_layered.repositories']
        del sys.modules['concepts.concepts_02_layered.services']
        del sys.modules['concepts.concepts_02_layered.routes']
        del sys.modules['concepts.concepts_02_layered.models']
    
    from concepts.concepts_02_layered.main import app
    client = TestClient(app)
    
    # Créer un produit
    product_data = {
        "name": "Mouse",
        "price": 25.50,
        "stock": 50
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 201
    product_id = response.json()["id"]
    
    # Lister les produits
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    # Vendre un produit
    response = client.put(f"/products/{product_id}/sell?quantity=5")
    assert response.status_code == 200
    assert response.json()["stock"] == 45


def test_layered_business_logic():
    """Test de la logique métier (stock insuffisant)."""
    db_path = "databases/layered.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Forcer le rechargement du module
    if 'concepts.concepts_02_layered.main' in sys.modules:
        del sys.modules['concepts.concepts_02_layered.main']
        del sys.modules['concepts.concepts_02_layered.database']
        del sys.modules['concepts.concepts_02_layered.repositories']
        del sys.modules['concepts.concepts_02_layered.services']
        del sys.modules['concepts.concepts_02_layered.routes']
        del sys.modules['concepts.concepts_02_layered.models']
    
    from concepts.concepts_02_layered.main import app
    client = TestClient(app)
    
    # Créer un produit avec peu de stock
    product_data = {
        "name": "Keyboard",
        "price": 75.00,
        "stock": 3
    }
    response = client.post("/products", json=product_data)
    product_id = response.json()["id"]
    
    # Essayer de vendre plus que le stock
    response = client.put(f"/products/{product_id}/sell?quantity=10")
    assert response.status_code == 400
    assert "insuffisant" in response.json()["detail"].lower()


def test_layered_duplicate_product():
    """Test de la validation métier (produit en double)."""
    db_path = "databases/layered.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Forcer le rechargement du module
    if 'concepts.concepts_02_layered.main' in sys.modules:
        del sys.modules['concepts.concepts_02_layered.main']
        del sys.modules['concepts.concepts_02_layered.database']
        del sys.modules['concepts.concepts_02_layered.repositories']
        del sys.modules['concepts.concepts_02_layered.services']
        del sys.modules['concepts.concepts_02_layered.routes']
        del sys.modules['concepts.concepts_02_layered.models']
    
    from concepts.concepts_02_layered.main import app
    client = TestClient(app)
    
    # Créer un produit
    product_data = {
        "name": "Monitor",
        "price": 200.00,
        "stock": 10
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 201
    
    # Essayer de créer le même produit
    response = client.post("/products", json=product_data)
    assert response.status_code == 400
    assert "existe déjà" in response.json()["detail"].lower()