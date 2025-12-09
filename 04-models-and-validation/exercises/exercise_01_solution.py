"""
Solution de l'exercice 1 : Système de gestion d'étudiants avec validation
"""

from fastapi import FastAPI, Response, status, HTTPException
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


# Solution TODO 1: Modèle StudentCreate avec validation
class StudentCreate(BaseModel):
    """Modèle pour créer un étudiant avec validation."""
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    email: EmailStr
    age: int = Field(..., ge=16, le=100)
    grade: float = Field(..., ge=0.0, le=20.0)


# Solution TODO 2: Modèle StudentResponse avec champ calculé
class StudentResponse(BaseModel):
    """Modèle de réponse avec le statut de l'étudiant."""
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    age: int
    grade: float
    status: str


# Solution TODO 3: Route POST /students
@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    """
    Crée un nouvel étudiant avec calcul du statut.
    
    Le statut est calculé selon la note :
    - grade >= 10 : "Admis"
    - grade < 10 : "Refusé"
    """
    global student_id_counter
    
    # Calculer le statut selon la note
    student_status = "Admis" if student.grade >= 10 else "Refusé"
    
    # Créer l'étudiant complet
    new_student = {
        "id": student_id_counter,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "email": student.email,
        "age": student.age,
        "grade": student.grade,
        "status": student_status
    }
    
    students_db.append(new_student)
    student_id_counter += 1
    
    return new_student


# Solution TODO 4: Route GET /students
@app.get("/students", response_model=list[StudentResponse])
def get_all_students():
    """
    Retourne tous les étudiants.
    """
    return students_db


# Solution TODO 5: Route GET /students/{student_id}
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student_by_id(student_id: int):
    """
    Retourne un étudiant par son ID.
    
    Retourne 404 si l'étudiant n'existe pas.
    """
    for student in students_db:
        if student["id"] == student_id:
            return student
    
    # Lever une HTTPException pour retourner 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Étudiant non trouvé"
    )


# Pour lancer ce serveur :
# uvicorn exercises.exercise_01_solution:app --reload
#
# Tester dans Swagger :
# 1. POST /students avec un étudiant ayant grade >= 10 → status = "Admis"
# 2. POST /students avec un étudiant ayant grade < 10 → status = "Refusé"
# 3. Essayer de créer avec first_name d'1 caractère → Erreur 422
# 4. Essayer de créer avec age = 15 → Erreur 422
# 5. Essayer de créer avec grade = 25 → Erreur 422