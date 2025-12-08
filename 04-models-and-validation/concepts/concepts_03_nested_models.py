"""
Concepts : Modèles imbriqués

Les modèles Pydantic peuvent contenir d'autres modèles,
permettant de créer des structures de données complexes.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="API Modèles imbriqués",
    description="Démonstration des modèles imbriqués",
    version="1.0.0"
)


# Modèles de base
class Address(BaseModel):
    """Adresse."""
    street: str
    city: str
    postal_code: str
    country: str = "France"


class ContactInfo(BaseModel):
    """Informations de contact."""
    email: str
    phone: Optional[str] = None


# Modèle avec imbrication
class Customer(BaseModel):
    """Client avec adresse et contact."""
    name: str
    address: Address  # Modèle imbriqué
    contact: ContactInfo  # Modèle imbriqué
    vip: bool = False


# Modèles pour commande
class OrderItem(BaseModel):
    """Article dans une commande."""
    product_name: str
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class Order(BaseModel):
    """Commande avec articles."""
    customer_name: str
    items: list[OrderItem]  # Liste de modèles imbriqués
    notes: Optional[str] = None
    
    def calculate_total(self) -> float:
        """Calcule le total de la commande."""
        return sum(item.quantity * item.unit_price for item in self.items)


customers_db = []
orders_db = []


@app.post("/customers")
def create_customer(customer: Customer):
    """
    Crée un client avec adresse et contact.
    
    Exemple de données :
    {
        "name": "Alice",
        "address": {
            "street": "10 rue de Paris",
            "city": "Lyon",
            "postal_code": "69000"
        },
        "contact": {
            "email": "alice@example.com",
            "phone": "0612345678"
        }
    }
    """
    customer_dict = customer.model_dump()
    customers_db.append(customer_dict)
    return customer_dict


@app.post("/orders")
def create_order(order: Order):
    """
    Crée une commande avec plusieurs articles.
    
    Exemple de données :
    {
        "customer_name": "Bob",
        "items": [
            {"product_name": "Laptop", "quantity": 1, "unit_price": 999.99},
            {"product_name": "Mouse", "quantity": 2, "unit_price": 25.50}
        ],
        "notes": "Livraison urgente"
    }
    """
    order_dict = order.model_dump()
    order_dict["total"] = order.calculate_total()
    orders_db.append(order_dict)
    return order_dict


@app.get("/customers")
def get_customers():
    """Retourne tous les clients."""
    return customers_db


@app.get("/orders")
def get_orders():
    """Retourne toutes les commandes."""
    return orders_db


# Pour lancer ce serveur :
# uvicorn concepts.concepts_03_nested_models:app --reload
#
# Les modèles imbriqués permettent de :
# - Organiser les données de manière logique
# - Réutiliser des modèles (Address, ContactInfo)
# - Valider automatiquement toute la structure