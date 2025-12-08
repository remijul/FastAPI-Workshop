"""
Concepts : Première application FastAPI

NOTE IMPORTANTE - Documentation Swagger/ReDoc :
Dans cette première API, vous ne verrez PAS de section "Schemas" dans Swagger
car aucune route n'a de paramètres nécessitant une validation.
Les schémas apparaissent uniquement quand FastAPI doit valider des données.
"""

from fastapi import FastAPI

# Création de l'application FastAPI
app = FastAPI(
    title="Mon API Hello World",
    description="Une première API simple avec FastAPI",
    version="1.0.0"
)


@app.get("/")
def read_root():
    """
    Route racine de l'API.
    
    Returns:
        Un message de bienvenue
    """
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    """
    Vérifie que l'API est en ligne.
    
    Returns:
        Le statut de l'API
    """
    return {"status": "healthy"}


@app.get("/info")
def get_info():
    """
    Retourne des informations sur l'API.
    
    Returns:
        Informations sur l'API
    """
    return {
        "name": "Mon API",
        "version": "1.0.0",
        "description": "Une API de démonstration"
    }


# Pour lancer ce serveur :
# uvicorn concepts.concepts_01_hello_world:app --reload
#
# Puis ouvrir dans le navigateur :
# - http://127.0.0.1:8000 pour tester l'API
# - http://127.0.0.1:8000/docs pour Swagger UI
# - http://127.0.0.1:8000/redoc pour ReDoc