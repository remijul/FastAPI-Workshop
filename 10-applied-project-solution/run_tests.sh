#!/bin/bash

echo "🧪 Lancement des tests..."

# Tests de base
echo "📝 Tests NIVEAU 1 (CRUD)..."
pytest tests/test_characters.py::test_create_character -v
pytest tests/test_characters.py::test_get_all_characters_initial -v
pytest tests/test_characters.py::test_get_character_by_id -v
pytest tests/test_characters.py::test_update_character -v

# Tests avancés
echo "📝 Tests NIVEAU 2 (Filtres et Stats)..."
pytest tests/test_characters.py::test_filter_by_class -v
pytest tests/test_characters.py::test_get_statistics -v
pytest tests/test_characters.py::test_level_up -v

# Tous les tests
echo "📝 Tous les tests..."
pytest -v

# Couverture
echo "📊 Calcul de la couverture..."
pytest --cov=app --cov-report=html --cov-report=term

echo "✅ Tests terminés ! Voir htmlcov/index.html pour la couverture détaillée"