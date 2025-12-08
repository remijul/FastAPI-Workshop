"""
Concept 1 : Template Jinja2 de base

Jinja2 permet de générer du HTML dynamiquement.
Au lieu de retourner du JSON, on peut retourner des pages HTML complètes.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Concept 1 : Template de base")

# Configurer Jinja2
# Le dossier "templates" contient les fichiers HTML
templates = Jinja2Templates(directory="concepts/concept_01_basic_template/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Route qui retourne une page HTML.
    
    Le paramètre 'request' est obligatoire pour Jinja2.
    On passe des variables au template avec context.
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Bienvenue",
            "message": "Ceci est votre premier template Jinja2 !"
        }
    )


# Pour lancer :
# uvicorn concepts.concept_01_basic_template.main:app --reload
#
# Ouvrir dans le navigateur : http://localhost:8000
# Vous verrez une page HTML au lieu de JSON !