"""
Tests pour l'exercice 2 : API calculatrice
"""

from fastapi.testclient import TestClient
from exercises.exercise_02_solution import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Calculatrice API"
    assert data["version"] == "1.0.0"
    assert "operations" in data
    assert len(data["operations"]) == 5


def test_calculate_add():
    response = client.get("/calculate/add?a=10&b=5")
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "add"
    assert data["a"] == 10
    assert data["b"] == 5
    assert data["result"] == 15


def test_calculate_subtract():
    response = client.get("/calculate/subtract?a=20&b=8")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 12


def test_calculate_multiply():
    response = client.get("/calculate/multiply?a=6&b=7")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 42


def test_calculate_divide():
    response = client.get("/calculate/divide?a=20&b=4")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 5


def test_calculate_divide_by_zero():
    response = client.get("/calculate/divide?a=10&b=0")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is None
    assert data["error"] == "Division par zéro"


def test_calculate_power():
    response = client.get("/calculate/power?a=2&b=3")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 8


def test_square():
    response = client.get("/square/5")
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == 5
    assert data["square"] == 25


def test_square_float():
    response = client.get("/square/2.5")
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == 2.5
    assert data["square"] == 6.25