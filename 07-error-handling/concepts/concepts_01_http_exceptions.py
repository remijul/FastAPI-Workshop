"""
Concepts : HTTPException - La base de la gestion d'erreurs

HTTPException est la manière standard de lever des erreurs dans FastAPI.
Elle permet de retourner des codes HTTP appropriés avec des messages clairs.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="API HTTPException",
    description="Démonstration des HTTPException",
    version="1.0.0"
)

# Base de données simulée
users_db = {}
user_id_counter = 1


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    email: str


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """
    Crée un utilisateur.
    
    Démontre HTTPException 400 pour validation métier.
    """
    global user_id_counter
    
    # Vérifier si le username existe déjà (validation métier)
    for existing_user in users_db.values():
        if existing_user["username"] == user.username:
            # Lever une HTTPException avec code 400 (Bad Request)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce nom d'utilisateur existe déjà"
            )
    
    # Créer l'utilisateur
    new_user = {
        "id": user_id_counter,
        "username": user.username,
        "email": user.email
    }
    users_db[user_id_counter] = new_user
    user_id_counter += 1
    
    return new_user


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Récupère un utilisateur.
    
    Démontre HTTPException 404 pour ressource non trouvée.
    """
    user = users_db.get(user_id)
    
    if not user:
        # Lever une HTTPException avec code 404 (Not Found)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utilisateur {user_id} non trouvé"
        )
    
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """
    Supprime un utilisateur.
    
    Démontre HTTPException 403 pour action interdite.
    """
    user = users_db.get(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    # Interdire la suppression de l'utilisateur admin (id=1)
    if user_id == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Impossible de supprimer l'utilisateur admin"
        )
    
    del users_db[user_id]
    return {"message": "Utilisateur supprimé"}


# Pour lancer :
# uvicorn concepts.concepts_01_http_exceptions:app --reload
#
# Codes HTTP courants :
# 200 OK - Succès
# 201 Created - Ressource créée
# 204 No Content - Succès sans contenu
# 400 Bad Request - Erreur de validation métier
# 401 Unauthorized - Non authentifié
# 403 Forbidden - Authentifié mais pas autorisé
# 404 Not Found - Ressource non trouvée
# 422 Unprocessable Entity - Erreur de validation Pydantic
# 500 Internal Server Error - Erreur serveur