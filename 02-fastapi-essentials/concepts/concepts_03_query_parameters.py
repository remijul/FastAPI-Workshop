"""
Concepts : Paramètres de requête (query parameters)

NOTE IMPORTANTE - Validation des query parameters :
Comme pour les path parameters, vous verrez la section "Schemas" dans Swagger
car FastAPI valide automatiquement les types des paramètres de requête.

Différences avec les path parameters :
- Les query parameters peuvent avoir des valeurs par défaut
- Ils peuvent être optionnels (Optional[type])
- Ils apparaissent après le "?" dans l'URL

Exemples de validation :
- /search?query=laptop&limit=5 → ✅ Fonctionne
- /search?query=laptop&limit=abc → ❌ Erreur 422 (limit doit être un int)
- /search?query=laptop → ✅ Fonctionne (limit prend la valeur par défaut 10)
"""

from fastapi import FastAPI
from typing import Optional

app = FastAPI(
    title="API avec paramètres de requête",
    description="Démonstration des query parameters",
    version="1.0.0"
)


@app.get("/search")
def search_items(query: str, limit: int = 10):
    """
    Recherche des articles.
    
    Args:
        query: Le terme de recherche (obligatoire)
        limit: Nombre maximum de résultats (par défaut 10)
        
    Returns:
        Les résultats de la recherche
        
    Note:
        - query est OBLIGATOIRE (pas de valeur par défaut)
        - limit est OPTIONNEL (valeur par défaut = 10)
        - limit doit être un entier, sinon erreur 422
    """
    return {
        "query": query,
        "limit": limit,
        "results": [f"Résultat {i} pour '{query}'" for i in range(1, min(limit, 5) + 1)]
    }


@app.get("/products")
def list_products(category: Optional[str] = None, min_price: float = 0.0):
    """
    Liste les produits avec filtres optionnels.
    
    Args:
        category: Catégorie de produits (optionnel, peut être None)
        min_price: Prix minimum (par défaut 0.0)
        
    Returns:
        La liste des produits filtrés
        
    Note:
        - Optional[str] signifie que category peut être None ou un string
        - min_price est un float, FastAPI accepte aussi les entiers (3 → 3.0)
    """
    result = {
        "min_price": min_price,
        "products": []
    }
    
    if category:
        result["category"] = category
        result["products"] = [f"{category} Product 1", f"{category} Product 2"]
    else:
        result["products"] = ["Product 1", "Product 2", "Product 3"]
    
    return result


@app.get("/calculate")
def calculate(a: float, b: float, operation: str = "add"):
    """
    Effectue un calcul simple.
    
    Args:
        a: Premier nombre (obligatoire)
        b: Deuxième nombre (obligatoire)
        operation: Opération à effectuer (par défaut "add")
        
    Returns:
        Le résultat du calcul
        
    Note:
        - a et b sont des float (acceptent aussi les entiers)
        - operation est un string sans restriction de valeur
        - Dans une vraie API, on utiliserait Enum pour limiter les opérations
    """
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        result = a / b if b != 0 else 0
    else:
        result = 0
    
    return {
        "a": a,
        "b": b,
        "operation": operation,
        "result": result
    }


# Pour lancer ce serveur :
# uvicorn concepts.concepts_03_query_parameters:app --reload
#
# Puis ouvrir dans le navigateur :
# - http://127.0.0.1:8000/search?query=laptop&limit=5 pour tester
# - http://127.0.0.1:8000/docs pour Swagger UI
# - http://127.0.0.1:8000/redoc pour ReDoc
#
# EXERCICES dans Swagger :
# 1. Essayez /search sans le paramètre query → Erreur 422 (obligatoire)
# 2. Essayez /search?query=test&limit=abc → Erreur 422 (limit doit être un int)
# 3. Essayez /products?min_price=cinquante → Erreur 422 (doit être un nombre)