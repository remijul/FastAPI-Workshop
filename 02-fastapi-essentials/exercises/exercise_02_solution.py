"""
Solution de l'exercice 2 : API calculatrice avec validation
"""

from fastapi import FastAPI

# Création de l'application FastAPI
app = FastAPI(
    title="Calculatrice API",
    description="Une API pour effectuer des calculs mathématiques",
    version="1.0.0"
)


@app.get("/")
def read_root():
    """
    Route racine qui retourne les informations sur l'API.
    
    Returns:
        Informations sur l'API et les opérations disponibles
    """
    return {
        "name": "Calculatrice API",
        "version": "1.0.0",
        "operations": ["add", "subtract", "multiply", "divide", "power"]
    }


@app.get("/calculate/{operation}")
def calculate(operation: str, a: float, b: float):
    """
    Effectue un calcul selon l'opération demandée.
    
    Args:
        operation: L'opération à effectuer (add, subtract, multiply, divide, power)
        a: Premier nombre
        b: Deuxième nombre
        
    Returns:
        Le résultat du calcul ou une erreur en cas de division par zéro
    """
    result = None
    error = None
    
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            error = "Division par zéro"
        else:
            result = a / b
    elif operation == "power":
        result = a ** b
    
    response = {
        "operation": operation,
        "a": a,
        "b": b,
        "result": result
    }
    
    if error:
        response["error"] = error
    
    return response


@app.get("/square/{number}")
def calculate_square(number: float):
    """
    Calcule le carré d'un nombre.
    
    Args:
        number: Le nombre à élever au carré
        
    Returns:
        Le nombre et son carré
    """
    return {
        "number": number,
        "square": number * number
    }


# Pour lancer ce serveur :
# uvicorn exercises.exercise_02_solution:app --reload
#
# Puis tester :
# - http://127.0.0.1:8000/docs pour Swagger UI
# - http://127.0.0.1:8000/calculate/add?a=10&b=5
# - http://127.0.0.1:8000/calculate/divide?a=10&b=0 (teste la division par zéro)
# - http://127.0.0.1:8000/square/5