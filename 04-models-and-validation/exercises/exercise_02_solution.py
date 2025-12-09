"""
Solution de l'exercice 2 : Système de gestion de bibliothèque simplifié
"""

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel, Field
from datetime import date

# Application FastAPI
app = FastAPI(
    title="API Bibliothèque",
    description="API de gestion de bibliothèque avec emprunts",
    version="1.0.0"
)

# Bases de données simulées
books_db = []
members_db = []
loans_db = []
book_id_counter = 1
member_id_counter = 1
loan_id_counter = 1


# Solution TODO 1: Modèles de base

class BookCreate(BaseModel):
    """Modèle pour créer un livre."""
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    isbn: str = Field(..., min_length=13, max_length=13)
    available_copies: int = Field(..., ge=0)


class BookResponse(BaseModel):
    """Modèle de réponse pour un livre."""
    id: int
    title: str
    author: str
    isbn: str
    available_copies: int


class MemberCreate(BaseModel):
    """Modèle pour créer un membre."""
    name: str = Field(..., min_length=2)
    email: str


class MemberResponse(BaseModel):
    """Modèle de réponse pour un membre."""
    id: int
    name: str
    email: str


# Solution TODO 2: Routes de création

@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    """Crée un nouveau livre."""
    global book_id_counter
    
    new_book = {
        "id": book_id_counter,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "available_copies": book.available_copies
    }
    
    books_db.append(new_book)
    book_id_counter += 1
    
    return new_book


@app.post("/members", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(member: MemberCreate):
    """Crée un nouveau membre."""
    global member_id_counter
    
    new_member = {
        "id": member_id_counter,
        "name": member.name,
        "email": member.email
    }
    
    members_db.append(new_member)
    member_id_counter += 1
    
    return new_member


@app.get("/books", response_model=list[BookResponse])
def get_all_books():
    """Retourne tous les livres."""
    return books_db


# Solution TODO 3: Modèles d'emprunt

class LoanCreate(BaseModel):
    """Modèle pour créer un emprunt."""
    book_id: int
    member_id: int


class LoanResponse(BaseModel):
    """Modèle de réponse pour un emprunt."""
    id: int
    book_id: int
    member_id: int
    loan_date: str
    returned: bool


# Solution TODO 4: Route POST /loans

@app.post("/loans", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan(loan: LoanCreate):
    """
    Crée un nouvel emprunt.
    
    Validations :
    - Le livre doit exister (404)
    - Le membre doit exister (404)
    - Des exemplaires doivent être disponibles (400)
    """
    global loan_id_counter
    
    # Vérifier que le livre existe
    book = None
    book_index = None
    for i, b in enumerate(books_db):
        if b["id"] == loan.book_id:
            book = b
            book_index = i
            break
    
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livre non trouvé"
        )
    
    # Vérifier que le membre existe
    member_exists = False
    for m in members_db:
        if m["id"] == loan.member_id:
            member_exists = True
            break
    
    if not member_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membre non trouvé"
        )
    
    # Vérifier qu'il y a des exemplaires disponibles
    if book["available_copies"] <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aucun exemplaire disponible"
        )
    
    # Créer l'emprunt
    new_loan = {
        "id": loan_id_counter,
        "book_id": loan.book_id,
        "member_id": loan.member_id,
        "loan_date": str(date.today()),
        "returned": False
    }
    
    loans_db.append(new_loan)
    loan_id_counter += 1
    
    # Réduire le nombre d'exemplaires disponibles
    books_db[book_index]["available_copies"] -= 1
    
    return new_loan


# Solution TODO 5: Route PUT /loans/{loan_id}/return

@app.put("/loans/{loan_id}/return", response_model=LoanResponse)
def return_loan(loan_id: int):
    """
    Marque un emprunt comme retourné.
    
    Validations :
    - L'emprunt doit exister (404)
    - L'emprunt ne doit pas être déjà retourné (400)
    """
    # Trouver l'emprunt
    loan = None
    loan_index = None
    for i, l in enumerate(loans_db):
        if l["id"] == loan_id:
            loan = l
            loan_index = i
            break
    
    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emprunt non trouvé"
        )
    
    # Vérifier que l'emprunt n'est pas déjà retourné
    if loan["returned"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emprunt déjà retourné"
        )
    
    # Marquer comme retourné
    loans_db[loan_index]["returned"] = True
    
    # Augmenter le nombre d'exemplaires disponibles
    for i, book in enumerate(books_db):
        if book["id"] == loan["book_id"]:
            books_db[i]["available_copies"] += 1
            break
    
    return loans_db[loan_index]


# Pour lancer ce serveur :
# uvicorn exercises.exercise_02_solution:app --reload
#
# Scénario de test complet dans Swagger :
# 1. POST /books pour créer un livre avec available_copies = 2
# 2. POST /members pour créer un membre
# 3. POST /loans pour emprunter le livre → available_copies = 1
# 4. POST /loans pour emprunter à nouveau → available_copies = 0
# 5. POST /loans pour emprunter une 3ème fois → Erreur 400 (aucun exemplaire)
# 6. GET /books pour vérifier available_copies = 0
# 7. PUT /loans/1/return pour retourner le premier emprunt → available_copies = 1
# 8. PUT /loans/1/return à nouveau → Erreur 400 (déjà retourné)