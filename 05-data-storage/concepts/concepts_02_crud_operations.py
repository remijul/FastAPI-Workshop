"""
Concepts : Opérations CRUD complètes avec SQLite

Démontre les 4 opérations de base :
- CREATE : INSERT
- READ : SELECT
- UPDATE : UPDATE
- DELETE : DELETE
"""

import sqlite3
from fastapi import FastAPI, HTTPException, status

app = FastAPI(
    title="API CRUD SQLite",
    description="Démonstration des opérations CRUD",
    version="1.0.0"
)

DATABASE_PATH = "databases/concepts_02.db"


def init_database():
    """Initialise la base de données."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1
        )
    """)
    
    conn.commit()
    conn.close()


init_database()


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(username: str, email: str):
    """CREATE : Crée un utilisateur."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email)
        )
        user_id = cursor.lastrowid
        conn.commit()
        
        return {
            "id": user_id,
            "username": username,
            "email": email,
            "active": 1
        }
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username déjà existant"
        )
    finally:
        conn.close()


@app.get("/users")
def get_all_users():
    """READ : Récupère tous les utilisateurs."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE active = 1")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """READ : Récupère un utilisateur par ID."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ? AND active = 1", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    return dict(row)


@app.put("/users/{user_id}")
def update_user(user_id: int, username: str = None, email: str = None):
    """UPDATE : Met à jour un utilisateur."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Vérifier que l'utilisateur existe
    cursor.execute("SELECT id FROM users WHERE id = ? AND active = 1", (user_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    # Construire la requête UPDATE dynamiquement
    updates = []
    params = []
    
    if username is not None:
        updates.append("username = ?")
        params.append(username)
    
    if email is not None:
        updates.append("email = ?")
        params.append(email)
    
    if updates:
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
    
    # Retourner l'utilisateur mis à jour
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row)


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """DELETE : Supprime (désactive) un utilisateur."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Soft delete : on met active = 0 au lieu de supprimer
    cursor.execute("UPDATE users SET active = 0 WHERE id = ?", (user_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    conn.commit()
    conn.close()
    
    return {"message": "Utilisateur supprimé"}


# Pour lancer ce serveur :
# uvicorn concepts.concepts_02_crud_operations:app --reload
#
# Scénario de test :
# 1. POST /users avec username=alice&email=alice@example.com
# 2. GET /users → Liste avec alice
# 3. GET /users/1 → Détails d'alice
# 4. PUT /users/1 avec email=alice.new@example.com
# 5. DELETE /users/1
# 6. GET /users → Liste vide (alice est désactivée)