"""
Solution de l'exercice 1 : API de gestion de tâches simple
"""

from fastapi import FastAPI

# Création de l'application FastAPI avec titre et description
app = FastAPI(
    title="API de gestion de tâches",
    description="Une API simple pour gérer des tâches",
    version="1.0.0"
)


@app.get("/")
def read_root():
    """
    Route racine de l'API.
    
    Returns:
        Message de bienvenue
    """
    return {"message": "API de gestion de tâches"}


@app.get("/tasks")
def get_all_tasks():
    """
    Retourne la liste de toutes les tâches.
    
    Returns:
        Liste de 3 tâches avec id, title et completed
    """
    return [
        {"id": 1, "title": "Tâche 1", "completed": False},
        {"id": 2, "title": "Tâche 2", "completed": False},
        {"id": 3, "title": "Tâche 3", "completed": False}
    ]


@app.get("/tasks/search")
def search_tasks(status: str = "all"):
    """
    Recherche des tâches par statut.
    
    Args:
        status: Le statut des tâches ("all", "completed", "pending")
        
    Returns:
        Le statut recherché et le nombre de tâches
        
    Note CRITIQUE:
        Cette route DOIT être déclarée AVANT /tasks/{task_id} !
        Sinon FastAPI pensera que "search" est un task_id et essaiera
        de le convertir en int, ce qui causera une erreur 422.
    """
    return {
        "status": status,
        "count": 3
    }


@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    """
    Retourne une tâche spécifique par son ID.
    
    Args:
        task_id: L'identifiant de la tâche
        
    Returns:
        La tâche avec l'ID demandé
        
    Note:
        Cette route avec paramètre doit être déclarée APRÈS
        les routes spécifiques comme /tasks/search
    """
    return {
        "id": task_id,
        "title": f"Tâche {task_id}",
        "completed": False
    }


# Pour lancer ce serveur :
# uvicorn exercises.exercise_01_solution:app --reload
#
# Puis tester :
# - http://127.0.0.1:8000/docs pour Swagger UI
# - http://127.0.0.1:8000/tasks
# - http://127.0.0.1:8000/tasks/5
# - http://127.0.0.1:8000/tasks/search?status=completed