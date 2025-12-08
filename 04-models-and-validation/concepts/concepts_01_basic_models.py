"""
Concepts : Modèles Pydantic de base

Pydantic permet de définir des modèles avec validation automatique des types,
valeurs par défaut, et champs optionnels.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="API Modèles de base",
    description="Démonstration des modèles Pydantic de base",
    version="1.0.0"
)


# Modèle simple
class Book(BaseModel):
    """Modèle représentant un livre."""
    title: str
    author: str
    pages: int
    year: int


# Modèle avec valeurs par défaut
class BookWithDefaults(BaseModel):
    """Modèle de livre avec valeurs par défaut."""
    title: str
    author: str
    pages: int = 0
    year: int = 2024
    available: bool = True


# Modèle avec champs optionnels
class BookOptional(BaseModel):
    """Modèle de livre avec champs optionnels."""
    title: str
    author: str
    pages: Optional[int] = None
    year: Optional[int] = None
    isbn: Optional[str] = None


books_db = []


@app.post("/books/simple")
def create_simple_book(book: Book):
    """
    Crée un livre avec tous les champs obligatoires.
    
    Tous les champs doivent être fournis : title, author, pages, year
    """
    book_dict = book.model_dump()
    books_db.append(book_dict)
    return book_dict


@app.post("/books/with-defaults")
def create_book_with_defaults(book: BookWithDefaults):
    """
    Crée un livre avec des valeurs par défaut.
    
    Seuls title et author sont obligatoires.
    pages, year et available ont des valeurs par défaut.
    """
    book_dict = book.model_dump()
    return book_dict


@app.post("/books/optional")
def create_book_optional(book: BookOptional):
    """
    Crée un livre avec des champs optionnels.
    
    Seuls title et author sont obligatoires.
    Les autres champs peuvent être None.
    """
    book_dict = book.model_dump()
    return book_dict


@app.get("/books")
def get_all_books():
    """Retourne tous les livres créés."""
    return books_db


# Pour lancer ce serveur :
# uvicorn concepts.concepts_01_basic_models:app --reload
#
# Tester dans Swagger :
# 1. POST /books/simple - Tous les champs sont OBLIGATOIRES
#    {"title": "Python", "author": "Alice", "pages": 300, "year": 2023}
#
# 2. POST /books/with-defaults - Seuls title et author obligatoires
#    {"title": "FastAPI", "author": "Bob"}
#    → pages=0, year=2024, available=True par défaut
#
# 3. POST /books/optional - Seuls title et author obligatoires
#    {"title": "Django", "author": "Charlie"}
#    → pages=None, year=None, isbn=None