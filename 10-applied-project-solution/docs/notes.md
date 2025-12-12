```md
- supprimer le fichier `__init.py__` à la racine de `\10-applied-project`.
- utiliser les versions corrigées de `Dockerfile` et `docker-compose.yml`.
- supprimer l'ancien volume `docker-compose down -v`.
- build les nouveaux volumes `docker-compose build --no-cache`.
- lancer les tester depuis Docker `docker-compose run --rm test`.
- lancer l'API depuis Docker `docker-compose up api`.
```
