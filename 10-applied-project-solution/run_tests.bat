@echo off

echo Lancement des tests...

echo Tests NIVEAU 1 (CRUD)...
pytest tests/test_characters.py::test_create_character -v
pytest tests/test_characters.py::test_get_all_characters_initial -v
pytest tests/test_characters.py::test_get_character_by_id -v
pytest tests/test_characters.py::test_update_character -v

echo Tests NIVEAU 2 (Filtres et Stats)...
pytest tests/test_characters.py::test_filter_by_class -v
pytest tests/test_characters.py::test_get_statistics -v
pytest tests/test_characters.py::test_level_up -v

echo Tous les tests...
pytest -v

echo Calcul de la couverture...
pytest --cov=app --cov-report=html --cov-report=term

echo Tests termines ! Voir htmlcov/index.html pour la couverture detaillee

pause