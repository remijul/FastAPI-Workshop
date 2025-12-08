"""
Tests pour l'exercice 2 : Système de gestion de bibliothèque
"""

from fastapi.testclient import TestClient
from exercises.exercise_02 import app

client = TestClient(app)


def test_create_book():
    book_data = {
        "title": "Python Programming",
        "author": "Alice Smith",
        "isbn": "1234567890123",
        "available_copies": 5
    }
    response = client.post("/books", json=book_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Python Programming"
    assert "id" in data


def test_create_book_isbn_invalid_length():
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "12345",  # Trop court
        "available_copies": 3
    }
    response = client.post("/books", json=book_data)
    assert response.status_code == 422


def test_get_all_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_member():
    member_data = {
        "name": "Bob Johnson",
        "email": "bob@example.com"
    }
    response = client.post("/members", json=member_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Bob Johnson"
    assert "id" in data


def test_create_loan():
    # Créer un livre
    book_data = {
        "title": "FastAPI Guide",
        "author": "Charlie Brown",
        "isbn": "9876543210987",
        "available_copies": 3
    }
    book_response = client.post("/books", json=book_data)
    book_id = book_response.json()["id"]
    
    # Créer un membre
    member_data = {
        "name": "Diana Prince",
        "email": "diana@example.com"
    }
    member_response = client.post("/members", json=member_data)
    member_id = member_response.json()["id"]
    
    # Créer un emprunt
    loan_data = {
        "book_id": book_id,
        "member_id": member_id
    }
    response = client.post("/loans", json=loan_data)
    assert response.status_code == 201
    data = response.json()
    assert data["book_id"] == book_id
    assert data["member_id"] == member_id
    assert data["returned"] is False
    assert "loan_date" in data
    
    # Vérifier que les exemplaires disponibles ont diminué
    book_check = client.get("/books")
    books = book_check.json()
    for book in books:
        if book["id"] == book_id:
            assert book["available_copies"] == 2


def test_create_loan_book_not_found():
    # Créer un membre
    member_data = {
        "name": "Eve Adams",
        "email": "eve@example.com"
    }
    member_response = client.post("/members", json=member_data)
    member_id = member_response.json()["id"]
    
    # Essayer d'emprunter un livre qui n'existe pas
    loan_data = {
        "book_id": 9999,
        "member_id": member_id
    }
    response = client.post("/loans", json=loan_data)
    assert response.status_code == 404


def test_create_loan_member_not_found():
    # Créer un livre
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "1111111111111",
        "available_copies": 2
    }
    book_response = client.post("/books", json=book_data)
    book_id = book_response.json()["id"]
    
    # Essayer d'emprunter avec un membre qui n'existe pas
    loan_data = {
        "book_id": book_id,
        "member_id": 9999
    }
    response = client.post("/loans", json=loan_data)
    assert response.status_code == 404


def test_create_loan_no_copies_available():
    # Créer un livre sans exemplaires
    book_data = {
        "title": "Rare Book",
        "author": "Frank Miller",
        "isbn": "2222222222222",
        "available_copies": 0
    }
    book_response = client.post("/books", json=book_data)
    book_id = book_response.json()["id"]
    
    # Créer un membre
    member_data = {
        "name": "Grace Lee",
        "email": "grace@example.com"
    }
    member_response = client.post("/members", json=member_data)
    member_id = member_response.json()["id"]
    
    # Essayer d'emprunter
    loan_data = {
        "book_id": book_id,
        "member_id": member_id
    }
    response = client.post("/loans", json=loan_data)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data


def test_return_loan():
    # Créer un livre
    book_data = {
        "title": "Return Test Book",
        "author": "Henry Ford",
        "isbn": "3333333333333",
        "available_copies": 1
    }
    book_response = client.post("/books", json=book_data)
    book_id = book_response.json()["id"]
    
    # Créer un membre
    member_data = {
        "name": "Iris West",
        "email": "iris@example.com"
    }
    member_response = client.post("/members", json=member_data)
    member_id = member_response.json()["id"]
    
    # Créer un emprunt
    loan_data = {
        "book_id": book_id,
        "member_id": member_id
    }
    loan_response = client.post("/loans", json=loan_data)
    loan_id = loan_response.json()["id"]
    
    # Retourner le livre
    response = client.put(f"/loans/{loan_id}/return")
    assert response.status_code == 200
    data = response.json()
    assert data["returned"] is True
    
    # Vérifier que les exemplaires disponibles ont augmenté
    book_check = client.get("/books")
    books = book_check.json()
    for book in books:
        if book["id"] == book_id:
            assert book["available_copies"] == 1


def test_return_loan_not_found():
    response = client.put("/loans/9999/return")
    assert response.status_code == 404


def test_return_loan_already_returned():
    # Créer livre, membre et emprunt
    book_data = {
        "title": "Double Return Book",
        "author": "Jack Black",
        "isbn": "4444444444444",
        "available_copies": 1
    }
    book_response = client.post("/books", json=book_data)
    book_id = book_response.json()["id"]
    
    member_data = {
        "name": "Kate Wilson",
        "email": "kate@example.com"
    }
    member_response = client.post("/members", json=member_data)
    member_id = member_response.json()["id"]
    
    loan_data = {
        "book_id": book_id,
        "member_id": member_id
    }
    loan_response = client.post("/loans", json=loan_data)
    loan_id = loan_response.json()["id"]
    
    # Retourner une première fois
    client.put(f"/loans/{loan_id}/return")
    
    # Essayer de retourner une deuxième fois
    response = client.put(f"/loans/{loan_id}/return")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data