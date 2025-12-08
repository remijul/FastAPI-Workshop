"""
Tests pour les concepts d'authentification.
"""

from fastapi.testclient import TestClient


def test_password_hashing():
    """Test du hachage de mots de passe."""
    from concepts.concepts_01_password_hashing import app
    client = TestClient(app)
    
    # Enregistrer un utilisateur
    response = client.post("/register?username=alice&password=secret123")
    assert response.status_code == 200
    assert "créé" in response.json()["message"].lower()
    
    # Vérifier que le hash est différent du mot de passe
    debug_response = client.get("/debug/users")
    assert "secret123" not in str(debug_response.json())
    
    # Login avec bon mot de passe
    response = client.post("/login?username=alice&password=secret123")
    assert response.status_code == 200
    assert "réussie" in response.json()["message"].lower()
    
    # Login avec mauvais mot de passe
    response = client.post("/login?username=alice&password=wrongpass")
    assert response.status_code == 200
    assert "error" in response.json()


def test_jwt_basics():
    """Test des JWT."""
    from concepts.concepts_02_jwt_basics import app
    client = TestClient(app)
    
    # Enregistrer et login
    client.post("/register?username=bob&password=secret456")
    login_response = client.post("/login?username=bob&password=secret456")
    
    assert login_response.status_code == 200
    data = login_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    token = data["access_token"]
    
    # Accéder à la route protégée avec token
    response = client.get(f"/protected?token={token}")
    assert response.status_code == 200
    assert "bob" in response.json()["username"]
    
    # Accéder avec mauvais token
    response = client.get("/protected?token=invalid_token")
    assert response.status_code == 401


def test_dependency_injection():
    """Test de l'injection de dépendances."""
    from concepts.concepts_03_dependency_injection import app
    client = TestClient(app)
    
    # Enregistrer et login
    client.post("/register?username=charlie&password=secret789")
    login_response = client.post("/login?username=charlie&password=secret789")
    token = login_response.json()["access_token"]
    
    # Route publique sans token
    response = client.get("/public")
    assert response.status_code == 200
    
    # Route protégée sans token
    response = client.get("/me")
    assert response.status_code == 401
    
    # Route protégée avec token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "charlie"
    
    # Autre route protégée avec même token
    response = client.get("/profile", headers=headers)
    assert response.status_code == 200