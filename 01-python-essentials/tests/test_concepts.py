"""
Tests pour les concepts Python de base.
Ces tests montrent comment utiliser pytest.
"""

import pytest
from concepts.concepts_01_functions import calculate_total_price, apply_discount, format_product_name
from concepts.concepts_02_classes import Product, Order
from concepts.concepts_03_error_handling import (
    validate_price, process_order, safe_divide,
    InvalidPriceError, InsufficientStockError
)


# Tests pour les fonctions
def test_calculate_total_price():
    assert calculate_total_price(10.0, 3) == 30.0
    assert calculate_total_price(5.5, 2) == 11.0


def test_apply_discount():
    assert apply_discount(100.0, 10) == 90.0
    assert apply_discount(50.0, 20) == 40.0


def test_apply_discount_invalid():
    with pytest.raises(ValueError):
        apply_discount(100.0, 150)
    
    with pytest.raises(ValueError):
        apply_discount(100.0, -10)


def test_format_product_name():
    assert format_product_name("  laptop  ") == "Laptop"
    assert format_product_name("PHONE") == "Phone"


# Tests pour les classes
def test_product_creation():
    product = Product("Laptop", 999.99, 5)
    assert product.name == "Laptop"
    assert product.price == 999.99
    assert product.stock == 5


def test_product_is_available():
    product = Product("Phone", 500.0, 3)
    assert product.is_available() is True
    
    empty_product = Product("Tablet", 300.0, 0)
    assert empty_product.is_available() is False


def test_product_update_stock():
    product = Product("Mouse", 25.0, 10)
    product.update_stock(5)
    assert product.stock == 15
    
    product.update_stock(-3)
    assert product.stock == 12


def test_product_update_stock_negative():
    product = Product("Keyboard", 50.0, 2)
    with pytest.raises(ValueError):
        product.update_stock(-5)


def test_product_get_total_value():
    product = Product("Monitor", 200.0, 4)
    assert product.get_total_value() == 800.0


def test_order_creation():
    order = Order("ORD001", "Alice")
    assert order.order_id == "ORD001"
    assert order.customer_name == "Alice"
    assert order.get_item_count() == 0


def test_order_add_item():
    product = Product("Book", 15.0, 10)
    order = Order("ORD002", "Bob")
    order.add_item(product, 2)
    assert order.get_item_count() == 1


def test_order_add_item_insufficient_stock():
    product = Product("Pen", 2.0, 1)
    order = Order("ORD003", "Charlie")
    with pytest.raises(ValueError):
        order.add_item(product, 5)


def test_order_calculate_total():
    product1 = Product("Item1", 10.0, 5)
    product2 = Product("Item2", 20.0, 3)
    order = Order("ORD004", "Diana")
    order.add_item(product1, 2)
    order.add_item(product2, 1)
    assert order.calculate_total() == 40.0


# Tests pour la gestion d'erreurs
def test_validate_price_valid():
    validate_price(10.0)  # Ne doit pas lever d'exception


def test_validate_price_invalid():
    with pytest.raises(InvalidPriceError):
        validate_price(0)
    
    with pytest.raises(InvalidPriceError):
        validate_price(-5.0)


def test_process_order_success():
    result = process_order("Laptop", 2, 5)
    assert result["product"] == "Laptop"
    assert result["quantity"] == 2
    assert result["remaining_stock"] == 3
    assert result["status"] == "success"


def test_process_order_insufficient_stock():
    with pytest.raises(InsufficientStockError):
        process_order("Phone", 10, 5)


def test_process_order_invalid_quantity():
    with pytest.raises(ValueError):
        process_order("Tablet", 0, 10)


def test_safe_divide():
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(10, 0) == 0.0