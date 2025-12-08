"""
Solution de l'exercice 1 : API CRUD complète pour des articles de blog
"""

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

# Création de l'application FastAPI
app = FastAPI(
    title="API Articles de Blog",
    description="API CRUD pour gérer des articles de blog",
    version="1.0.0"
)

# Base de données simulée en mémoire
articles_db = []
article_id_counter = 1


# Modèle Pydantic Article
class Article(BaseModel):
    """Modèle représentant un article de blog."""
    title: str
    content: str
    author: str


@app.get("/articles", status_code=status.HTTP_200_OK)
def get_all_articles():
    """
    Récupère tous les articles.
    
    Returns:
        Liste de tous les articles
    """
    return articles_db


@app.get("/articles/{article_id}")
def get_article_by_id(article_id: int, response: Response):
    """
    Récupère un article par son ID.
    
    Args:
        article_id: L'identifiant de l'article
        response: Objet Response pour modifier le status code
        
    Returns:
        L'article trouvé ou un message d'erreur
    """
    for article in articles_db:
        if article["id"] == article_id:
            response.status_code = status.HTTP_200_OK
            return article
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Article non trouvé"}


@app.post("/articles", status_code=status.HTTP_201_CREATED)
def create_article(article: Article):
    """
    Crée un nouvel article.
    
    Args:
        article: Les données de l'article à créer
        
    Returns:
        L'article créé avec son ID
    """
    global article_id_counter
    
    new_article = {
        "id": article_id_counter,
        "title": article.title,
        "content": article.content,
        "author": article.author
    }
    
    articles_db.append(new_article)
    article_id_counter += 1
    
    return new_article


@app.put("/articles/{article_id}")
def update_article(article_id: int, article: Article, response: Response):
    """
    Met à jour un article existant.
    
    Args:
        article_id: L'ID de l'article à mettre à jour
        article: Les nouvelles données de l'article
        response: Objet Response pour modifier le status code
        
    Returns:
        L'article mis à jour ou un message d'erreur
    """
    for i, a in enumerate(articles_db):
        if a["id"] == article_id:
            updated_article = {
                "id": article_id,
                "title": article.title,
                "content": article.content,
                "author": article.author
            }
            articles_db[i] = updated_article
            response.status_code = status.HTTP_200_OK
            return updated_article
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Article non trouvé"}


@app.delete("/articles/{article_id}")
def delete_article(article_id: int, response: Response):
    """
    Supprime un article.
    
    Args:
        article_id: L'ID de l'article à supprimer
        response: Objet Response pour modifier le status code
        
    Returns:
        Message de confirmation ou d'erreur
    """
    for i, article in enumerate(articles_db):
        if article["id"] == article_id:
            articles_db.pop(i)
            response.status_code = status.HTTP_200_OK
            return {"message": "Article supprimé"}
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Article non trouvé"}


# Pour lancer ce serveur :
# uvicorn exercises.exercise_01_solution:app --reload
#
# Tester dans Swagger :
# 1. POST /articles pour créer un article
# 2. GET /articles pour voir tous les articles
# 3. GET /articles/{id} pour voir un article spécifique
# 4. PUT /articles/{id} pour modifier un article
# 5. DELETE /articles/{id} pour supprimer un article