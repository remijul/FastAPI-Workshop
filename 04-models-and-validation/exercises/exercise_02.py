"""
Exercice 2 : Système de gestion de bibliothèque simplifié

Objectif : Créer une API avec modèles imbriqués et logique métier.

TODO:
1. Créer les modèles Book et Member
2. Implémenter POST /books et POST /members
3. Créer le modèle LoanCreate et LoanResponse
4. Implémenter POST /loans avec validation (livre et membre existent, copies disponibles)
5. Implémenter PUT /loans/{loan_id}/return

Pour lancer l'API :
    uvicorn exercises.exercise_02:app --reload

Pour tester :
    pytest tests/test_exercise_02.py -v
"""

from fastapi import FastAPI, status, HTTPException
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


# TODO 1: Créer les modèles de base
# 
# Modèle BookCreate :
# - title: str (minimum 1 caractère)
# - author: str (minimum 1 caractère)
# - isbn: str (exactement 13 caractères, utiliser min_length et max_length)
# - available_copies: int (>= 0)
#
# Modèle BookResponse :
# - Tous les champs de BookCreate + id: int
#
# Modèle MemberCreate :
# - name: str (minimum 2 caractères)
# - email: str
#
# Modèle MemberResponse :
# - Tous les champs de MemberCreate + id: int

class BookCreate(BaseModel):
    pass

class BookResponse(BaseModel):
    pass

class MemberCreate(BaseModel):
    pass

class MemberResponse(BaseModel):
    pass


# TODO 2: Implémenter les routes de création
#
# Route POST /books
# - response_model=BookResponse, status_code=201
# - Créer un livre avec ID et l'ajouter à books_db
#
# Route POST /members
# - response_model=MemberResponse, status_code=201
# - Créer un membre avec ID et l'ajouter à members_db
#
# Route GET /books (pour faciliter les tests)
# - response_model=list[BookResponse]
# - Retourner tous les livres


# TODO 3: Créer les modèles d'emprunt
#
# Modèle LoanCreate :
# - book_id: int
# - member_id: int
#
# Modèle LoanResponse :
# - id: int
# - book_id: int
# - member_id: int
# - loan_date: str
# - returned: bool

class LoanCreate(BaseModel):
    pass

class LoanResponse(BaseModel):
    pass


# TODO 4: Route POST /loans
# - response_model=LoanResponse, status_code=201
# - Vérifier que le livre existe (lever HTTPException 404 si non, detail="Livre non trouvé")
# - Vérifier que le membre existe (lever HTTPException 404 si non, detail="Membre non trouvé")
# - Vérifier que available_copies > 0 (lever HTTPException 400 si non, detail="Aucun exemplaire disponible")
# - Créer l'emprunt avec :
#   * id auto-incrémenté
#   * loan_date = str(date.today())
#   * returned = False
# - Réduire available_copies du livre de 1
# - Ajouter l'emprunt à loans_db
# - Retourner l'emprunt créé
#
# Rappel HTTPException :
# raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message")


# TODO 5: Route PUT /loans/{loan_id}/return
# - response_model=LoanResponse
# - Trouver l'emprunt (lever HTTPException 404 si non trouvé, detail="Emprunt non trouvé")
# - Vérifier que l'emprunt n'est pas déjà retourné (lever HTTPException 400 si oui, detail="Emprunt déjà retourné")
# - Marquer returned = True
# - Augmenter available_copies du livre de 1
# - Retourner l'emprunt mis à jour