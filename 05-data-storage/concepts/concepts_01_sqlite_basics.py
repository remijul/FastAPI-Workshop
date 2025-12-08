"""
Concepts : Bases de SQLite avec Python

SQLite est une base de données légère intégrée à Python.
Aucun serveur n'est nécessaire, les données sont dans un fichier .db
"""

import sqlite3
from fastapi import FastAPI

app = FastAPI(
    title="API SQLite Basics",
    description="Démonstration des bases SQLite",
    version="1.0.0"
)

# Chemin vers la base de données
DATABASE_PATH = "databases/concepts_01.db"


def init_database():
    """Initialise la base de données avec une table products."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Créer la table si elle n'existe pas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
    """)
    
    conn.commit()
    conn.close()


# Initialiser la base au démarrage
init_database()


@app.get("/")
def read_root():
    """Route de test."""
    return {"message": "API SQLite Basics"}


@app.get("/products/count")
def count_products():
    """
    Compte le nombre de produits dans la base.
    
    Démontre une requête SELECT simple.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    
    conn.close()
    
    return {"count": count}


@app.post("/products/create")
def create_product(name: str, price: float, stock: int = 0):
    """
    Crée un produit dans la base.
    
    Démontre une requête INSERT.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
        (name, price, stock)
    )
    
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }


@app.get("/products/all")
def get_all_products():
    """
    Récupère tous les produits.
    
    Démontre SELECT avec fetchall().
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Pour avoir des dictionnaires
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    
    conn.close()
    
    # Convertir en liste de dictionnaires
    products = [dict(row) for row in rows]
    return products


# Pour lancer ce serveur :
# uvicorn concepts.concepts_01_sqlite_basics:app --reload
#
# Tester :
# 1. GET /products/count → Retourne 0 au début
# 2. POST /products/create?name=Laptop&price=999.99&stock=5
# 3. GET /products/count → Retourne 1
# 4. GET /products/all → Liste le produit créé
#
# Note : Le fichier databases/concepts_01.db est créé automatiquement