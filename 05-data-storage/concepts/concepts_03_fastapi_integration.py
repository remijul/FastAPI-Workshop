"""
Concepts : Intégration propre de SQLite avec FastAPI

Démontre les bonnes pratiques :
- Fonctions utilitaires pour la base
- Gestion des connexions
- Intégration avec Pydantic
"""

import sqlite3
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="API FastAPI + SQLite",
    description="Intégration propre SQLite/FastAPI",
    version="1.0.0"
)

DATABASE_PATH = "databases/concepts_03.db"


# Modèles Pydantic
class TaskCreate(BaseModel):
    """Modèle pour créer une tâche."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False


class TaskResponse(BaseModel):
    """Modèle de réponse pour une tâche."""
    id: int
    title: str
    description: Optional[str]
    completed: bool


# Fonctions utilitaires pour la base de données
def get_db_connection():
    """Crée une connexion à la base de données."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialise la base de données."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)
    
    conn.commit()
    conn.close()


init_database()


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    """Crée une nouvelle tâche."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
        (task.title, task.description, int(task.completed))
    )
    
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return TaskResponse(
        id=task_id,
        title=task.title,
        description=task.description,
        completed=task.completed
    )


@app.get("/tasks", response_model=list[TaskResponse])
def get_all_tasks():
    """Récupère toutes les tâches."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    
    return [
        TaskResponse(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            completed=bool(row["completed"])
        )
        for row in rows
    ]


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """Récupère une tâche par ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche non trouvée"
        )
    
    return TaskResponse(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        completed=bool(row["completed"])
    )


@app.put("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int):
    """Marque une tâche comme complétée."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche non trouvée"
        )
    
    conn.commit()
    
    # Récupérer la tâche mise à jour
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    
    return TaskResponse(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        completed=bool(row["completed"])
    )


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Supprime une tâche."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche non trouvée"
        )
    
    conn.commit()
    conn.close()
    
    return {"message": "Tâche supprimée"}


# Pour lancer ce serveur :
# uvicorn concepts.concepts_03_fastapi_integration:app --reload
#
# Cette approche est meilleure car :
# 1. Utilise Pydantic pour la validation
# 2. Utilise response_model pour la cohérence
# 3. Fonction get_db_connection() réutilisable
# 4. Gestion propre des booléens SQLite (0/1)