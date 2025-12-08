# Étape 9 : Templates Jinja2 (Optionnel)

## Objectifs

Cette étape optionnelle vous montre comment créer une interface web pour votre API :

- Générer du HTML dynamiquement avec Jinja2
- Créer des formulaires HTML
- Gérer l'authentification avec des cookies
- Combiner API et interface web

**Note** : Cette étape est optionnelle. Elle complète votre apprentissage FastAPI mais n'est pas obligatoire.

## Prérequis

- Python 3.8 ou supérieur installé
- Avoir validé au moins l'étape 6 (Architecture en couches)

## Installation
```bash
pip install -r requirements.txt
```

Nouveau package :
- `jinja2` : Moteur de templates pour générer du HTML

## API JSON vs Interface Web

**Jusqu'ici** : Votre API retournait du JSON
```python
@app.get("/users")
def get_users():
    return {"users": ["alice", "bob"]}
# → {"users": ["alice", "bob"]}
```

**Maintenant** : Vous pouvez retourner du HTML
```python
@app.get("/users")
def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})
# → Page HTML complète
```

## Concept 1 : Template de base
```bash
uvicorn concepts.concept_01_basic_template.main:app --reload
```

**Configuration Jinja2** :
```python
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="concepts/concept_01_basic_template/templates")
```

**Route qui retourne du HTML** :
```python
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,  # Obligatoire
            "title": "Bienvenue",
            "message": "Premier template !"
        }
    )
```

**Template HTML** :
```html
<h1>{{ title }}</h1>
<p>{{ message }}</p>
```

**Variables Jinja2** : `{{ variable }}` affiche une variable.

## Concept 2 : Données dynamiques
```bash
uvicorn concepts.concept_02_dynamic_data.main:app --reload
```

**Boucles** :
```html
{% for product in products %}
    <div>{{ product.name }} - {{ product.price }} €</div>
{% endfor %}
```

**Conditions** :
```html
{% if product.in_stock %}
    <span>✓ En stock</span>
{% else %}
    <span>✗ Rupture</span>
{% endif %}
```

**Héritage de templates** :
```html
<!-- base.html -->
<html>
    <body>
        {% block content %}{% endblock %}
    </body>
</html>

<!-- products.html -->
{% extends "base.html" %}
{% block content %}
    <h1>Produits</h1>
{% endblock %}
```

**Filtres** :
```html
{{ "%.2f"|format(product.price) }}  <!-- Format nombre -->
{{ products|length }}                <!-- Longueur liste -->
```

## Concept 3 : Formulaires HTML
```bash
uvicorn concepts.concept_03_forms.main:app --reload
```

**Afficher un formulaire** :
```python
@app.get("/contact", response_class=HTMLResponse)
def contact_form(request: Request):
    return templates.TemplateResponse("contact_form.html", {"request": request})
```

**Template du formulaire** :
```html
<form method="POST" action="/contact">
    <input type="text" name="name" required>
    <input type="email" name="email" required>
    <textarea name="message" required></textarea>
    <button type="submit">Envoyer</button>
</form>
```

**Traiter le formulaire** :
```python
from fastapi import Form

@app.post("/contact")
def submit_contact(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    # Traiter les données
    return RedirectResponse(url="/success", status_code=303)
```

**Form(...)** extrait les données du formulaire HTML.

## Application de démonstration
```bash
uvicorn demo_app.main:app --reload
```

**Application complète** : Gestionnaire de tâches avec interface web.

**Fonctionnalités** :
- 📝 Inscription / Connexion
- 🔒 Authentification avec cookies
- ✅ Créer, compléter, supprimer des tâches
- 🎨 Interface web complète (pas de JSON)

**Structure** :
```
demo_app/
├── main.py          # Point d'entrée
├── models.py        # Modèles Pydantic
├── database.py      # SQLite
├── repositories.py  # Accès données
├── services.py      # Logique métier
├── routes.py        # Routes avec templates
├── static/          # CSS
└── templates/       # HTML
```

**Workflow utilisateur** :
1. Ouvrir http://localhost:8000
2. Cliquer sur "Commencer"
3. Créer un compte (username + password)
4. Se connecter
5. Gérer ses tâches

## Authentification avec cookies

**Créer un cookie** :
```python
response = RedirectResponse(url="/tasks", status_code=303)
response.set_cookie(key="username", value=username)
return response
```

**Lire un cookie** :
```python
def get_current_user(request: Request) -> str | None:
    return request.cookies.get("username")
```

**Supprimer un cookie** :
```python
response = RedirectResponse(url="/", status_code=303)
response.delete_cookie(key="username")
return response
```

## Fichiers statiques (CSS/JS)

**Monter les fichiers statiques** :
```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="demo_app/static"), name="static")
```

**Utiliser dans le template** :
```html
<link rel="stylesheet" href="/static/style.css">
```

## Syntaxe Jinja2 essentielle

**Variables** :
```html
{{ username }}
{{ product.name }}
{{ products[0] }}
```

**Boucles** :
```html
{% for item in items %}
    {{ item }}
{% endfor %}
```

**Conditions** :
```html
{% if user %}
    Bonjour {{ user }}
{% else %}
    Invité
{% endif %}
```

**Héritage** :
```html
{% extends "base.html" %}
{% block content %}...{% endblock %}
```

**Commentaires** :
```html
{# Ceci est un commentaire #}
```

## API + Interface Web : Les deux approches

**Vous pouvez combiner les deux** :
```python
# Route API (retourne JSON)
@app.get("/api/tasks")
def get_tasks_api():
    return {"tasks": [...]}

# Route Web (retourne HTML)
@app.get("/tasks", response_class=HTMLResponse)
def get_tasks_web(request: Request):
    return templates.TemplateResponse("tasks.html", {...})
```

**Avantages** :
- API pour applications mobiles, JavaScript, etc.
- Interface web pour utilisateurs finaux
- Même logique métier partagée

## Différences clés avec les API JSON

| API JSON | Interface Web |
|----------|---------------|
| `return {"data": ...}` | `return templates.TemplateResponse(...)` |
| Client traite les données | Serveur génère le HTML |
| Pour apps/services | Pour navigateurs |
| Authentification JWT | Authentification cookies |
| Pas de redirection | `RedirectResponse` |

## Redirection HTTP

**Après un POST, toujours rediriger** :
```python
@app.post("/tasks/new")
def create_task(...):
    # Créer la tâche
    return RedirectResponse(url="/tasks", status_code=303)
```

**Codes de redirection** :
- `303 See Other` : Après POST (recommandé)
- `302 Found` : Redirection temporaire
- `301 Moved Permanently` : Redirection permanente

## Quand utiliser Jinja2 ?

**✅ Utilisez Jinja2 pour** :
- Sites web traditionnels
- Backoffice / Admin
- Prototypes rapides
- Applications simples

**❌ N'utilisez PAS Jinja2 pour** :
- APIs REST pures
- Applications mobiles
- Applications JavaScript (React, Vue)
- Microservices

## Bonnes pratiques

**1. Séparation base.html** :
Créez un template de base et étendez-le partout.

**2. Fichiers statiques séparés** :
CSS et JavaScript dans le dossier `static/`.

**3. Validation côté serveur** :
Même avec formulaires HTML, validez avec Pydantic.

**4. CSRF Protection** :
En production, ajoutez une protection CSRF.

**5. Templates par fonctionnalité** :
Un template par page/fonctionnalité.

## Pour aller plus loin

- Templates avec HTMX (interactivité)
- Pagination de listes
- Upload de fichiers
- Messages flash (notifications)
- Internationalisation (i18n)

## Ressources

- [Documentation Jinja2](https://jinja.palletsprojects.com/)
- [FastAPI Templates](https://fastapi.tiangolo.com/advanced/templates/)
- [Tailwind CSS](https://tailwindcss.com/) pour le style

**Félicitations !** Vous savez maintenant créer des interfaces web avec FastAPI. 🎨