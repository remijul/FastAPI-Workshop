# Utiliser une image Python officielle légère
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application
COPY . .

# Créer le dossier pour la base de données
RUN mkdir -p databases

# ==================== IMPORTANT ====================
# Définir PYTHONPATH pour que Python trouve le module 'app'
ENV PYTHONPATH=/app

# Exposer le port 8000
EXPOSE 8000

# Commande pour lancer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]