"""
Concepts : Méthode GET - Récupération de données

La méthode GET est utilisée pour LIRE des données.
Elle ne doit JAMAIS modifier des données sur le serveur.
"""

from fastapi import FastAPI

app = FastAPI(
    title="API GET Methods",
    description="Démonstration de la méthode GET",
    version="1.0.0"
)

# Base de données simulée en mémoire
books_db = [
    {"id": 1, "title": "Python pour débutants", "author": "Alice", "year": 2020},
    {"id": 2, "title": "FastAPI en pratique", "author": "Bob", "year": 2022},
    {"id": 3, "title": "Data Science 101", "author": "Charlie", "year": 2021}
]


@app.get("/books")
def get_all_books():
    """
    Récupère tous les livres.
    
    Returns:
        Liste de tous les livres
    """
    return books_db


@app.get("/books/search")
def search_books(author: str = None, year: int = None):
    """
    Recherche des livres par auteur ou année.
    
    Args:
        author: Nom de l'auteur (optionnel)
        year: Année de publication (optionnel)
        
    Returns:
        Liste des livres correspondant aux critères
        
    Note CRITIQUE:
        Cette route DOIT être déclarée AVANT /books/{book_id} !
        Sinon FastAPI pensera que "search" est un book_id.
    """
    results = books_db
    
    if author:
        results = [book for book in results if book["author"].lower() == author.lower()]
    
    if year:
        results = [book for book in results if book["year"] == year]
    
    return results


@app.get("/books/{book_id}")
def get_book(book_id: int):
    """
    Récupère un livre par son ID.
    
    Args:
        book_id: L'identifiant du livre
        
    Returns:
        Le livre trouvé ou un message d'erreur
        
    Note:
        Cette route avec paramètre doit être déclarée APRÈS
        les routes spécifiques comme /books/search
    """
    for book in books_db:
        if book["id"] == book_id:
            return book
    
    return {"error": "Livre non trouvé"}


# Pour lancer ce serveur :
# uvicorn concepts.concepts_01_get_method:app --reload
#
# Tester :
# - http://127.0.0.1:8000/books
# - http://127.0.0.1:8000/books/1
# - http://127.0.0.1:8000/books/search?author=Alice
# - http://127.0.0.1:8000/docs pour Swagger UI
#
# RAPPEL IMPORTANT sur l'ordre des routes :
# ✅ /books/search AVANT /books/{book_id}
# ❌ /books/{book_id} AVANT /books/search (ne