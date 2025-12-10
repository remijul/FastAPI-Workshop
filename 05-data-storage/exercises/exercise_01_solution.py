"""
Solution de l'exercice 1 : API de gestion de contacts avec SQLite
"""

import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

app = FastAPI(
    title="API Contacts",
    description="Gestion de contacts avec SQLite",
    version="1.0.0"
)

DATABASE_PATH = "databases/exercise_01.db"


def get_db_connection():
    """Crée une connexion à la base de données."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Solution TODO 1: Créer la fonction init_database()
def init_database():
    """Initialise la base de données avec la table contacts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT
        )
    """)
    
    conn.commit()
    conn.close()


# Initialiser la base au démarrage
init_database()


# Solution TODO 2: Créer les modèles Pydantic

class ContactCreate(BaseModel):
    """Modèle pour créer un contact."""
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: Optional[str] = None


class ContactResponse(BaseModel):
    """Modèle de réponse pour un contact."""
    id: int
    name: str
    email: str
    phone: Optional[str]


# Solution TODO 3: Route POST /contacts

@app.post("/contacts", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate):
    """Crée un nouveau contact."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)",
        (contact.name, contact.email, contact.phone)
    )
    
    contact_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return ContactResponse(
        id=contact_id,
        name=contact.name,
        email=contact.email,
        phone=contact.phone
    )


# Solution TODO 4: Route GET /contacts

@app.get("/contacts", response_model=list[ContactResponse])
def get_all_contacts():
    """Récupère tous les contacts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    
    return [
        ContactResponse(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            phone=row["phone"]
        )
        for row in rows
    ]


# Solution TODO 5: Route DELETE /contacts/{contact_id}

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    """Supprime un contact."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact non trouvé"
        )
    
    conn.commit()
    conn.close()
    
    return {"message": "Contact supprimé"}


# Pour lancer ce serveur :
# uvicorn exercises.exercise_01_solution:app --reload
#
# Tester dans Swagger :
# 1. POST /contacts avec un contact complet
# 2. GET /contacts pour voir tous les contacts
# 3. DELETE /contacts/{id} pour supprimer un contact