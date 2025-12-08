"""
Exercice 1 : API de gestion de tâches simple

Objectif : Créer une API FastAPI basique avec plusieurs routes.

TODO:
1. Créer une application FastAPI
2. Implémenter les 4 routes demandées
3. Faire passer tous les tests dans tests/test_exercise_01.py

Pour lancer l'API en développement :
    uvicorn exercises.exercise_01:app --reload

Pour tester l'API :
    pytest tests/test_exercise_01.py -v

ATTENTION À L'ORDRE DES ROUTES :
Les routes avec des chemins fixes (comme /tasks/search) doivent être
déclarées AVANT les routes avec des paramètres (comme /tasks/{task_id}).
"""

from fastapi import FastAPI

# TODO: Créer l'application FastAPI avec un titre et une description
app = FastAPI(
    title="API de gestion de tâches",
    description="Une API simple pour gérer des tâches",
    version="1.0.0"
)


# TODO: Route GET "/" qui retourne {"message": "API de gestion de tâches"}


# TODO: Route GET "/tasks" qui retourne une liste de 3 tâches
# Format de tâche: {"id": 1, "title": "Tâche 1", "completed": False}


# TODO: Route GET "/tasks/search" avec query parameters
# IMPORTANT: Cette route DOIT être déclarée AVANT /tasks/{task_id}
# Paramètres: status (str, optionnel, valeurs: "all", "completed", "pending")
# Par défaut: "all"
# Retourner: {"status": status, "count": 3}


# TODO: Route GET "/tasks/{task_id}" qui retourne une tâche spécifique
# IMPORTANT: Cette route DOIT être déclarée APRÈS /tasks/search
# Paramètre: task_id (int)
# Retourner: {"id": task_id, "title": f"Tâche {task_id}", "completed": False}