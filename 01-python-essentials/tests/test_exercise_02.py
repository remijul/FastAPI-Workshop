"""
Tests pour l'exercice 2 : Système de gestion d'utilisateurs
"""

import pytest
from exercises.exercise_02 import (
    UserManager, UserAlreadyExistsError, 
    UserNotFoundError, InvalidEmailError
)


def test_user_manager_creation():
    manager = UserManager()
    assert manager.count_users() == 0


def test_add_user():
    manager = UserManager()
    user = manager.add_user("Alice", "alice@example.com", 25)
    assert user["name"] == "Alice"
    assert user["email"] == "alice@example.com"
    assert user["age"] == 25
    assert manager.count_users() == 1


def test_add_multiple_users():
    manager = UserManager()
    manager.add_user("Alice", "alice@example.com", 25)
    manager.add_user("Bob", "bob@example.com", 30)
    assert manager.count_users() == 2


def test_add_user_empty_name():
    manager = UserManager()
    with pytest.raises(ValueError):
        manager.add_user("", "test@example.com", 20)


def test_add_user_invalid_email():
    manager = UserManager()
    with pytest.raises(InvalidEmailError):
        manager.add_user("Charlie", "invalidemail", 28)


def test_add_user_negative_age():
    manager = UserManager()
    with pytest.raises(ValueError):
        manager.add_user("Diana", "diana@example.com", -5)


def test_add_user_already_exists():
    manager = UserManager()
    manager.add_user("Eve", "eve@example.com", 22)
    with pytest.raises(UserAlreadyExistsError):
        manager.add_user("Eve Again", "eve@example.com", 23)


def test_get_user():
    manager = UserManager()
    manager.add_user("Frank", "frank@example.com", 35)
    user = manager.get_user("frank@example.com")
    assert user["name"] == "Frank"
    assert user["age"] == 35


def test_get_user_not_found():
    manager = UserManager()
    with pytest.raises(UserNotFoundError):
        manager.get_user("notfound@example.com")


def test_update_age():
    manager = UserManager()
    manager.add_user("Grace", "grace@example.com", 28)
    updated = manager.update_age("grace@example.com", 29)
    assert updated["age"] == 29


def test_update_age_user_not_found():
    manager = UserManager()
    with pytest.raises(UserNotFoundError):
        manager.update_age("notfound@example.com", 30)


def test_update_age_negative():
    manager = UserManager()
    manager.add_user("Henry", "henry@example.com", 40)
    with pytest.raises(ValueError):
        manager.update_age("henry@example.com", -1)