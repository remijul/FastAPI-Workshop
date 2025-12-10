"""
Solution de l'exercice 2 : API de blog avec SQLite
"""

import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI(
    title="API Blog",
    description="Gestion d'articles de blog avec SQLite",
    version="1.0.0"
)

DATABASE_PATH = "databases/exercise_02.db"


def get_db_connection():
    """Crée une connexion à la base de données."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Solution TODO 1: Créer la fonction init_database()

def init_database():
    """Initialise la base de données avec la table articles."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            published INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()


# Initialiser la base au démarrage
init_database()


# Solution TODO 2: Créer les modèles Pydantic

class ArticleCreate(BaseModel):
    """Modèle pour créer un article."""
    title: str = Field(..., min_length=5)
    content: str = Field(..., min_length=10)
    author: str = Field(..., min_length=2)


class ArticleResponse(BaseModel):
    """Modèle de réponse pour un article."""
    id: int
    title: str
    content: str
    author: str
    published: bool
    created_at: str


# Solution TODO 3: Route POST /articles

@app.post("/articles", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def create_article(article: ArticleCreate):
    """Crée un nouvel article."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    created_at = datetime.now().isoformat()
    
    cursor.execute(
        "INSERT INTO articles (title, content, author, created_at) VALUES (?, ?, ?, ?)",
        (article.title, article.content, article.author, created_at)
    )
    
    article_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return ArticleResponse(
        id=article_id,
        title=article.title,
        content=article.content,
        author=article.author,
        published=False,
        created_at=created_at
    )


# Solution TODO 4: Route GET /articles/{article_id}

@app.get("/articles/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int):
    """Récupère un article par son ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article non trouvé"
        )
    
    return ArticleResponse(
        id=row["id"],
        title=row["title"],
        content=row["content"],
        author=row["author"],
        published=bool(row["published"]),
        created_at=row["created_at"]
    )


# Solution TODO 5: Route PUT /articles/{article_id}/publish

@app.put("/articles/{article_id}/publish", response_model=ArticleResponse)
def publish_article(article_id: int):
    """Publie un article."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE articles SET published = 1 WHERE id = ?", (article_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article non trouvé"
        )
    
    conn.commit()
    
    # Récupérer l'article mis à jour
    cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
    row = cursor.fetchone()
    conn.close()
    
    return ArticleResponse(
        id=row["id"],
        title=row["title"],
        content=row["content"],
        author=row["author"],
        published=bool(row["published"]),
        created_at=row["created_at"]
    )


# Pour lancer ce serveur :
# uvicorn exercises.exercise_02_solution:app --reload
#
# Tester dans Swagger :
# 1. POST /articles pour créer un article (published=False par défaut)
# 2. GET /articles/{id} pour récupérer l'article
# 3. PUT /articles/{id}/publish pour publier l'article
# 4. GET /articles/{id} à nouveau pour vérifier published=True