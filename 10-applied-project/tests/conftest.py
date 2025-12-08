"""
Configuration pytest et fixtures partagées.

Les fixtures sont des fonctions réutilisables dans tous les tests.
"""

import pytest
import os
import sys
from pathlib import Path


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Configure l'environnement de test.
    
    Cette fixture s'exécute une seule fois au début de tous les tests.
    """
    # Utiliser une base de données de test séparée
    os.environ["DATABASE_PATH"] = "databases/test_characters.db"
    
    yield
    
    # Nettoyer après tous les tests
    test_db = Path("databases/test_characters.db")
    if test_db.exists():
        test_db.unlink()


@pytest.fixture(autouse=True)
def reset_database():
    """
    Réinitialise la base de données avant chaque test.
    
    Cette fixture s'exécute avant chaque test pour garantir l'isolation.
    """
    # Supprimer la base de test si elle existe
    test_db = Path("databases/test_characters.db")
    if test_db.exists():
        test_db.unlink()
    
    # Forcer le rechargement des modules pour réinitialiser la DB
    modules_to_reload = [
        'app.main',
        'app.database',
        'app.repositories',
        'app.services',
        'app.routes'
    ]
    
    for module in modules_to_reload:
        if module in sys.modules:
            del sys.modules[module]
    
    yield


@pytest.fixture
def client():
    """
    Fixture qui fournit un client de test FastAPI.
    
    Utilisation dans les tests:
        def test_something(client):
            response = client.get("/characters")
            assert response.status_code == 200
    """
    from fastapi.testclient import TestClient
    from app.main import app
    
    return TestClient(app)


@pytest.fixture
def sample_character_data():
    """
    Fixture qui fournit des données de personnage valides pour les tests.
    
    Utilisation:
        def test_create(client, sample_character_data):
            response = client.post("/characters", json=sample_character_data)
    """
    return {
        "name": "Test Warrior",
        "class": "warrior",
        "level": 25,
        "health_points": 300,
        "attack": 75,
        "defense": 35,
        "speed": 50,
        "special_ability": "Test Strike",
        "image_url": "https://example.com/warrior.jpg"
    }


@pytest.fixture
def create_test_character(client, sample_character_data):
    """
    Fixture qui crée un personnage de test et retourne ses données.
    
    Utilisation:
        def test_get_by_id(create_test_character):
            character_id = create_test_character["id"]
            # ... test avec cet ID
    """
    response = client.post("/characters", json=sample_character_data)
    return response.json()