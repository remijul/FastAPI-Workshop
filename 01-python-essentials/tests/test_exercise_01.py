"""
Tests pour l'exercice 1 : Gestion d'un panier d'achat
"""

import pytest
from exercises.exercise_01 import Cart


def test_cart_creation():
    cart = Cart()
    assert cart.is_empty() is True


def test_add_product():
    cart = Cart()
    cart.add_product("Laptop", 999.99, 1)
    assert cart.is_empty() is False


def test_add_multiple_products():
    cart = Cart()
    cart.add_product("Mouse", 25.0, 2)
    cart.add_product("Keyboard", 75.0, 1)
    assert cart.is_empty() is False


def test_get_total():
    cart = Cart()
    cart.add_product("Item1", 10.0, 2)
    cart.add_product("Item2", 15.0, 1)
    assert cart.get_total() == 35.0


def test_get_total_empty_cart():
    cart = Cart()
    assert cart.get_total() == 0.0


def test_add_product_invalid_price():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add_product("Invalid", -10.0, 1)


def test_add_product_invalid_quantity():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add_product("Invalid", 10.0, 0)
    
    with pytest.raises(ValueError):
        cart.add_product("Invalid", 10.0, -5)


def test_apply_coupon():
    cart = Cart()
    cart.add_product("Product", 100.0, 1)
    discounted = cart.apply_coupon(10)
    assert discounted == 90.0


def test_apply_coupon_invalid():
    cart = Cart()
    cart.add_product("Product", 50.0, 1)
    
    with pytest.raises(ValueError):
        cart.apply_coupon(-10)
    
    with pytest.raises(ValueError):
        cart.apply_coupon(150)


def test_apply_coupon_empty_cart():
    cart = Cart()
    assert cart.apply_coupon(10) == 0.0