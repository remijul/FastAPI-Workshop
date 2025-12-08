"""
Point d'entrée de l'application de démonstration.

Application complète de gestion de tâches avec :
- Interface web (templates Jinja2)
- Authentification (cookies)
- CRUD de tâches
- Architecture en couches
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import init_database
from .routes import router

# Initialiser la base
init_database()

# Créer l'application
app = FastAPI(
    title="Gestionnaire de Tâches",
    description="Application de démonstration avec templates Jinja2",
    version="1.0.0"
)

# Monter les fichiers statiques (CSS)
app.mount("/static", StaticFiles(directory="demo_app/static"), name="static")

# Inclure les routes
app.include_router(router)


# Pour lancer :
# uvicorn demo_app.main:app --reload
#
# Puis ouvrir : http://localhost:8000
#
# Workflow :
# 1. S'inscrire (/register)
# 2. Se connecter (/login)
# 3. Gérer ses tâches (/tasks)
# 4. Créer, compléter, supprimer des tâches