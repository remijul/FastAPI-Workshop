"""
Exercice 2 : API calculatrice avec validation

Objectif : Créer une API de calculatrice avec paramètres de chemin et de requête.

TODO:
1. Créer une application FastAPI
2. Implémenter les 3 routes demandées
3. Gérer les cas d'erreur (division par zéro)
4. Faire passer tous les tests dans tests/test_exercise_02.py

Pour lancer l'API en développement :
    uvicorn exercises.exercise_02:app --reload

Pour tester l'API :
    pytest tests/test_exercise_02.py -v
"""

from fastapi import FastAPI

# TODO: Créer l'application FastAPI
app = None  # Remplacer None par FastAPI(...)


# TODO: Route GET "/" qui retourne des informations sur l'API
# Retourner: {"name": "Calculatrice API", "version": "1.0.0", "operations": ["add", "subtract", "multiply", "divide", "power"]}


# TODO: Route GET "/calculate/{operation}"
# Paramètre de chemin: operation (str) - une des opérations: add, subtract, multiply, divide, power
# Paramètres de requête: a (float), b (float)
# Retourner: {"operation": operation, "a": a, "b": b, "result": result}
# IMPORTANT: Gérer la division par zéro (retourner result: None et "error": "Division par zéro")


# TODO: Route GET "/square/{number}"
# Paramètre de chemin: number (float)
# Retourner: {"number": number, "square": number * number}