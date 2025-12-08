"""
Concept 2 : Templates avec données dynamiques

Démonstration des boucles, conditions et héritage de templates.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Concept 2 : Données dynamiques")

templates = Jinja2Templates(directory="concepts/concept_02_dynamic_data/templates")

# Base de données simulée
products = [
    {"id": 1, "name": "Laptop", "price": 999.99, "in_stock": True},
    {"id": 2, "name": "Mouse", "price": 29.99, "in_stock": True},
    {"id": 3, "name": "Keyboard", "price": 79.99, "in_stock": False},
    {"id": 4, "name": "Monitor", "price": 299.99, "in_stock": True},
]


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Page d'accueil."""
    return templates.TemplateResponse(
        "products.html",
        {
            "request": request,
            "products": products,
            "total_products": len(products)
        }
    )


# Pour lancer :
# uvicorn concepts.concept_02_dynamic_data.main:app --reload
#
# Le template affiche :
# - Une boucle pour lister tous les produits
# - Des conditions pour afficher "En stock" ou "Rupture"
# - Un calcul du nombre total de produits