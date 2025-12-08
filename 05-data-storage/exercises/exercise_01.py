"""
Exercice 1 : API de gestion de contacts avec SQLite

Objectif : Créer une API CRUD simple pour gérer des contacts.

TODO:
1. Créer la fonction init_database() qui crée la table contacts
2. Créer les modèles Pydantic ContactCreate et ContactResponse
3. Implémenter POST /contacts (créer un contact)
4. Implémenter GET /contacts (lister tous les contacts)
5. Implémenter DELETE /contacts/{contact_id} (supprimer un contact)

Pour lancer l'API :
    uvicorn exercises.exercise_01:app --reload

Pour tester :
    pytest tests/test_exercise_01.py -v
"""

import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

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


# TODO 1: Créer la fonction init_database()
# Créer une table "contacts" avec les colonnes :
# - id: INTEGER PRIMARY KEY AUTOINCREMENT
# - name: TEXT NOT NULL
# - email: TEXT NOT NULL
# - phone: TEXT
# 
# Utiliser CREATE TABLE IF NOT EXISTS
# Appeler cette fonction après sa définition
def init_database():
    pass


# TODO 2: Créer les modèles Pydantic
#
# Modèle ContactCreate :
# - name: str (minimum 2 caractères)
# - email: EmailStr
# - phone: str (optionnel)
#
# Modèle ContactResponse :
# - id: int
# - name: str
# - email: str
# - phone: str | None
class ContactCreate(BaseModel):
    pass

class ContactResponse(BaseModel):
    pass


# TODO 3: Route POST /contacts
# - response_model=ContactResponse, status_code=201
# - Paramètre: contact (ContactCreate)
# - Insérer dans la base : INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)
# - Utiliser cursor.lastrowid pour récupérer l'ID
# - Retourner le contact créé


# TODO 4: Route GET /contacts
# - response_model=list[ContactResponse]
# - SELECT * FROM contacts
# - Retourner tous les contacts sous forme de liste


# TODO 5: Route DELETE /contacts/{contact_id}
# - Paramètre: contact_id (int)
# - DELETE FROM contacts WHERE id = ?
# - Si cursor.rowcount == 0 : lever HTTPException 404
# - Retourner {"message": "Contact supprimé"}