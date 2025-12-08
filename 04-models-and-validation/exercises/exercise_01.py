"""
Exercice 1 : Système de gestion d'étudiants avec validation

Objectif : Créer une API simple avec validation Pydantic avancée.

TODO:
1. Créer le modèle StudentCreate avec validation des champs
2. Créer le modèle StudentResponse avec un champ calculé "status"
3. Implémenter la route POST /students qui calcule le status
4. Implémenter la route GET /students
5. Implémenter la route GET /students/{student_id}

Pour lancer l'API :
    uvicorn exercises.exercise_01:app --reload

Pour tester :
    pytest tests/test_exercise_01.py -v
"""

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, EmailStr, Field

# Application FastAPI
app = FastAPI(
    title="API Gestion d'Étudiants",
    description="API avec validation Pydantic",
    version="1.0.0"
)

# Base de données simulée
students_db = []
student_id_counter = 1


# TODO 1: Créer le modèle StudentCreate avec validation
# Champs obligatoires :
# - first_name: str (minimum 2 caractères)
# - last_name: str (minimum 2 caractères)
# - email: EmailStr
# - age: int (entre 16 et 100 inclus)
# - grade: float (entre 0 et 20 inclus)
class StudentCreate(BaseModel):
    pass


# TODO 2: Créer le modèle StudentResponse
# Tous les champs de StudentCreate +
# - id: int
# - status: str (champ qui sera calculé : "Admis" si grade >= 10, sinon "Refusé")
class StudentResponse(BaseModel):
    pass


# TODO 3: Route POST /students
# - response_model=StudentResponse
# - status_code=201
# - Créer un étudiant avec un ID
# - Calculer le champ status selon la note (>= 10 → "Admis", sinon "Refusé")
# - Ajouter à students_db
# - Retourner l'étudiant créé


# TODO 4: Route GET /students
# - response_model=list[StudentResponse]
# - Retourner tous les étudiants


# TODO 5: Route GET /students/{student_id}
# - response_model=StudentResponse
# - Retourner l'étudiant avec cet ID (200)
# - Si non trouvé, lever HTTPException(status_code=404, detail="Étudiant non trouvé")
# 
# Exemple d'utilisation de HTTPException :
# if not found:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message d'erreur")