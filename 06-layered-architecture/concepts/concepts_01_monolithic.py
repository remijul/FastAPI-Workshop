"""
Concepts : API monolithique (tout dans un seul fichier)

Problèmes de cette approche :
- Difficile à maintenir quand l'application grandit
- Difficile à tester unitairement
- Difficile à réutiliser le code
- Tout est mélangé : logique métier, accès données, routes
"""

import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="API Monolithique")

DATABASE_PATH = "databases/monolithic.db"


# Modèles Pydantic
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int


# Initialisation base de données
def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


# Routes avec TOUTE la logique mélangée
@app.post("/products", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate):
    """
    Route monolithique : tout est dans la route !
    - Accès à la base de données
    - Logique métier
    - Gestion des erreurs
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Logique métier : vérifier si le produit existe déjà
    cursor.execute("SELECT id FROM products WHERE name = ?", (product.name,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Produit déjà existant")
    
    # Insertion dans la base
    cursor.execute(
        "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
        (product.name, product.price, product.stock)
    )
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return ProductResponse(
        id=product_id,
        name=product.name,
        price=product.price,
        stock=product.stock
    )


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    """Route monolithique pour récupérer un produit."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    return ProductResponse(**dict(row))


# Pour lancer :
# uvicorn concepts.concepts_01_monolithic:app --reload
#
# Problèmes de cette approche :
# 1. Code difficile à tester (tout est couplé)
# 2. Code dupliqué (connexion DB répétée)
# 3. Difficile d'ajouter de nouvelles fonctionnalités
# 4. Pas de réutilisation possible