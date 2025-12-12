# 🐳 Guide Docker - Mini-Projet

## Installation de Docker

### Windows et Mac
Télécharger et installer Docker Desktop :
https://www.docker.com/products/docker-desktop

### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker

# Ajouter votre utilisateur au groupe docker
sudo usermod -aG docker $USER
```

## Utilisation

### 1. Build de l'image
```bash
docker-compose build
```

Cette commande :
- Crée l'image Docker à partir du Dockerfile
- Installe toutes les dépendances Python
- Prépare l'environnement

### 2. Lancer l'application
```bash
docker-compose up
```

Ou en mode détaché (arrière-plan) :
```bash
docker-compose up -d
```

L'API sera accessible sur : http://localhost:8000

### 3. Voir les logs
```bash
docker-compose logs -f
```

### 4. Arrêter l'application
```bash
docker-compose down
```

### 5. Supprimer tout (conteneurs + volumes)
```bash
docker-compose down -v
```

## Mode développement avec hot-reload

Pour développer avec rechargement automatique :
```bash
docker-compose -f docker-compose.dev.yml up
```

Dans ce mode, vos modifications de code sont immédiatement prises en compte.

## Accéder à Adminer (Interface DB)

Si vous utilisez le service `adminer` dans docker-compose.yml :

1. Ouvrir http://localhost:8080
2. Système : SQLite 3
3. Fichier : Laisser vide ou indiquer le chemin

**Note** : Adminer dans Docker peut avoir du mal à accéder directement à la DB SQLite. 
Utilisez plutôt un outil local comme DB Browser for SQLite pour visualiser la base.

## Commandes utiles

### Entrer dans le conteneur
```bash
docker-compose exec api bash
```

### Voir les conteneurs en cours
```bash
docker ps
```

### Voir toutes les images
```bash
docker images
```

### Nettoyer les images inutilisées
```bash
docker system prune -a
```

## Structure des volumes

La base de données SQLite est montée en volume :
```
./databases:/app/databases
```

Cela signifie que la base de données persiste même si vous supprimez le conteneur.

## Troubleshooting

### Port 8000 déjà utilisé

Si le port 8000 est occupé, modifiez dans docker-compose.yml :
```yaml
ports:
  - "8001:8000"  # Utiliser le port 8001 au lieu de 8000
```

### Permission denied sur Linux
```bash
sudo chown -R $USER:$USER databases/
```

### Rebuild complet

Si vous avez modifié requirements.txt ou le Dockerfile :
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Base de données corrompue
```bash
docker-compose down
rm databases/characters.db
docker-compose up
```

## Variables d'environnement

Vous pouvez créer un fichier `.env` :
```env
DATABASE_PATH=databases/characters.db
DEBUG=True
SECRET_KEY=your-secret-key-here
```

Docker Compose chargera automatiquement ces variables.

## Production

Pour la production, créer un `docker-compose.prod.yml` :
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./databases:/app/databases
    environment:
      - DATABASE_PATH=/app/databases/characters.db
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
    restart: always
```

Lancer avec :
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Multi-stage build (optimisation avancée)

Pour réduire la taille de l'image, vous pouvez utiliser un multi-stage build.

Modifier le Dockerfile :
```dockerfile
# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Cela réduit la taille de l'image finale.
