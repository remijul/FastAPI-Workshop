"""
Exercice 2 : API de blog avec SQLite

Objectif : Créer une API pour gérer des articles de blog avec persistance.

TODO:
1. Créer la fonction init_database() avec table articles
2. Créer les modèles Pydantic ArticleCreate et ArticleResponse
3. Implémenter POST /articles (créer un article)
4. Implémenter GET /articles/{article_id} (récupérer un article)
5. Implémenter PUT /articles/{article_id}/publish (publier un article)

Pour lancer l'API :
    uvicorn exercises.exercise_02:app --reload

Pour tester :
    pytest tests/test_exercise_02.py -v
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


# TODO 1: Créer la fonction init_database()
# Créer une table "articles" avec les colonnes :
# - id: INTEGER PRIMARY KEY AUTOINCREMENT
# - title: TEXT NOT NULL
# - content: TEXT NOT NULL
# - author: TEXT NOT NULL
# - published: INTEGER NOT NULL DEFAULT 0 (0=non publié, 1=publié)
# - created_at: TEXT NOT NULL (format ISO datetime)
#
# Appeler cette fonction après sa définition
def init_database():
    pass


# TODO 2: Créer les modèles Pydantic
#
# Modèle ArticleCreate :
# - title: str (minimum 5 caractères)
# - content: str (minimum 10 caractères)
# - author: str (minimum 2 caractères)
#
# Modèle ArticleResponse :
# - id: int
# - title: str
# - content: str
# - author: str
# - published: bool
# - created_at: str
class ArticleCreate(BaseModel):
    pass

class ArticleResponse(BaseModel):
    pass


# TODO 3: Route POST /articles
# - response_model=ArticleResponse, status_code=201
# - Paramètre: article (ArticleCreate)
# - created_at = datetime.now().isoformat()
# - Insérer : INSERT INTO articles (title, content, author, created_at) VALUES (?, ?, ?, ?)
# - published est par défaut à 0 (False)
# - Retourner l'article créé avec published=False


# TODO 4: Route GET /articles/{article_id}
# - response_model=ArticleResponse
# - Paramètre: article_id (int)
# - SELECT * FROM articles WHERE id = ?
# - Si non trouvé : lever HTTPException 404
# - Convertir published (0/1) en bool avant de retourner


# TODO 5: Route PUT /articles/{article_id}/publish
# - response_model=ArticleResponse
# - Paramètre: article_id (int)
# - UPDATE articles SET published = 1 WHERE id = ?
# - Si cursor.rowcount == 0 : lever HTTPException 404
# - Récupérer et retourner l'article mis à jour avec published=True