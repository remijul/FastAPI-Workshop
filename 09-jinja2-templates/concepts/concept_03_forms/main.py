"""
Concept 3 : Formulaires HTML

Démonstration de formulaires HTML avec FastAPI + Jinja2.
Les formulaires permettent aux utilisateurs d'envoyer des données.
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Concept 3 : Formulaires")

templates = Jinja2Templates(directory="concepts/concept_03_forms/templates")

# Liste pour stocker les messages de contact
contacts = []


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Page d'accueil."""
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )


@app.get("/contact", response_class=HTMLResponse)
def contact_form(request: Request):
    """Affiche le formulaire de contact."""
    return templates.TemplateResponse(
        "contact_form.html",
        {"request": request}
    )


@app.post("/contact")
def submit_contact(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
    ):
    """
    Traite le formulaire de contact.
    
    Form(...) extrait les données du formulaire HTML.
    """
    # Sauvegarder le message
    contacts.append({
        "name": name,
        "email": email,
        "message": message
    })
    
    # Rediriger vers la page de succès
    return RedirectResponse(url="/success", status_code=303)


@app.get("/success", response_class=HTMLResponse)
def success(request: Request):
    """Page de confirmation."""
    return templates.TemplateResponse(
        "success.html",
        {
            "request": request,
            "total_messages": len(contacts)
        }
    )


# Pour lancer :
# uvicorn concepts.concept_03_forms.main:app --reload
#
# Workflow :
# 1. Aller sur http://localhost:8000
# 2. Cliquer sur "Nous contacter"
# 3. Remplir le formulaire
# 4. Soumettre → Redirection vers page de succès