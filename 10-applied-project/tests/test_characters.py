"""
Tests pour les endpoints de gestion des personnages.

TODO:
- Compléter les tests marqués avec TODO
- Ajouter vos propres tests pour couvrir tous les cas

Rappel: Lancer les tests avec:
    pytest -v
    pytest tests/test_characters.py -v
"""

import pytest


# ==================== NIVEAU 1 : TESTS CRUD DE BASE ====================

def test_read_root(client):
    """
    Test de la route racine.
    
    EXEMPLE FOURNI - Ce test est complet.
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_get_all_characters_initial(client):
    """
    Test GET /characters - Vérifier que 10 personnages sont chargés au démarrage.
    
    EXEMPLE FOURNI - Ce test est complet.
    """
    response = client.get("/characters")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 10  # 10 personnages initiaux
    
    # Vérifier la structure d'un personnage
    first_character = data[0]
    assert "id" in first_character
    assert "name" in first_character
    assert "class" in first_character
    assert "level" in first_character
    assert "created_at" in first_character


# TODO NIVEAU 1: Compléter les tests suivants

def test_create_character(client, sample_character_data):
    """
    Test POST /characters - Créer un personnage.
    
    TODO:
    - Faire une requête POST /characters avec sample_character_data
    - Vérifier status_code = 201
    - Vérifier que la réponse contient un id
    - Vérifier que les données retournées correspondent aux données envoyées
    """
    # TODO: Implémenter ce test
    pass


def test_create_character_invalid_level(client):
    """
    Test POST /characters - Niveau invalide (hors limites).
    
    TODO:
    - Créer un personnage avec level = 150 (> 100)
    - Vérifier status_code = 422 (Validation Error)
    """
    # TODO: Implémenter ce test
    pass


def test_get_character_by_id(client, create_test_character):
    """
    Test GET /characters/{id} - Récupérer un personnage.
    
    TODO:
    - Utiliser create_test_character pour avoir un personnage existant
    - Faire GET /characters/{id}
    - Vérifier status_code = 200
    - Vérifier que les données correspondent
    """
    # TODO: Implémenter ce test
    pass


def test_get_character_not_found(client):
    """
    Test GET /characters/{id} - Personnage non trouvé.
    
    TODO:
    - Faire GET /characters/9999
    - Vérifier status_code = 404
    """
    # TODO: Implémenter ce test
    pass


def test_update_character(client, create_test_character):
    """
    Test PUT /characters/{id} - Modifier un personnage.
    
    TODO:
    - Utiliser create_test_character
    - Faire PUT /characters/{id} avec de nouvelles données
    - Vérifier status_code = 200
    - Vérifier que les données ont été mises à jour
    """
    # TODO: Implémenter ce test
    pass


def test_update_character_partial(client, create_test_character):
    """
    Test PUT /characters/{id} - Mise à jour partielle.
    
    TODO:
    - Modifier uniquement le level
    - Vérifier que les autres champs n'ont pas changé
    """
    # TODO: Implémenter ce test
    pass


def test_delete_character(client, create_test_character):
    """
    Test DELETE /characters/{id} - Supprimer un personnage.
    
    TODO:
    - Supprimer le personnage créé
    - Vérifier status_code = 204
    - Vérifier que GET /characters/{id} retourne 404
    """
    # TODO: Implémenter ce test
    pass


def test_delete_character_not_found(client):
    """
    Test DELETE /characters/{id} - Supprimer un personnage inexistant.
    
    TODO:
    - Essayer de supprimer le personnage 9999
    - Vérifier status_code = 404
    """
    # TODO: Implémenter ce test
    pass


# ==================== NIVEAU 2 : TESTS AVANCÉS ====================

def test_filter_by_class(client):
    """
    Test GET /characters?class=warrior - Filtrer par classe.
    
    TODO NIVEAU 2:
    - Faire GET /characters?class=warrior
    - Vérifier que tous les personnages retournés sont des warriors
    """
    # TODO NIVEAU 2: Implémenter
    pass


def test_filter_by_level_range(client):
    """
    Test GET /characters?min_level=50&max_level=80 - Filtrer par niveau.
    
    TODO NIVEAU 2:
    - Faire GET /characters avec min_level et max_level
    - Vérifier que tous les personnages sont dans la plage
    """
    # TODO NIVEAU 2: Implémenter
    pass


def test_filter_combined(client):
    """
    Test GET /characters?class=mage&min_level=60 - Filtres combinés.
    
    TODO NIVEAU 2:
    - Combiner filtres de classe et niveau
    - Vérifier les résultats
    """
    # TODO NIVEAU 2: Implémenter
    pass


def test_get_statistics(client):
    """
    Test GET /characters/stats - Récupérer les statistiques.
    
    TODO NIVEAU 2:
    - Faire GET /characters/stats
    - Vérifier la structure de la réponse
    - Vérifier que total = 10 (personnages initiaux)
    """
    # TODO NIVEAU 2: Implémenter
    pass


def test_get_classes(client):
    """
    Test GET /classes - Liste des classes disponibles.
    
    TODO NIVEAU 2:
    - Faire GET /classes
    - Vérifier que la liste contient les 5 classes
    """
    # TODO NIVEAU 2: Implémenter
    pass


def test_level_up(client, create_test_character):
    """
    Test POST /characters/{id}/level-up - Augmenter le niveau.
    
    TODO NIVEAU 2:
    - Créer un personnage de niveau 25
    - Faire POST /characters/{id}/level-up
    - Vérifier que level = 26
    - Vérifier que health_points augmente de 10
    - Vérifier que attack augmente de 2
    - Vérifier que defense augmente de 1
    """
    # TODO NIVEAU 2: Implémenter
    pass


def test_level_up_max_level(client):
    """
    Test POST /characters/{id}/level-up - Personnage déjà niveau max.
    
    TODO NIVEAU 2:
    - Créer un personnage de niveau 100
    - Essayer de faire level-up
    - Vérifier status_code = 400
    """
    # TODO NIVEAU 2: Implémenter
    pass


# ==================== NIVEAU 3 : TESTS OPTIONNELS ====================

# TODO NIVEAU 3 - Option Auth: Tests d'authentification

@pytest.mark.skipif(True, reason="Implémenter si vous faites l'authentification")
def test_create_character_without_auth(client):
    """
    Test POST /characters sans authentification.
    
    TODO NIVEAU 3:
    - Essayer de créer un personnage sans token
    - Vérifier status_code = 401
    """
    pass


@pytest.mark.skipif(True, reason="Implémenter si vous faites l'authentification")
def test_create_character_with_auth(client):
    """
    Test POST /characters avec authentification.
    
    TODO NIVEAU 3:
    - S'inscrire et se connecter pour obtenir un token
    - Créer un personnage avec le token
    - Vérifier succès
    """
    pass


# TODO NIVEAU 3 - Option Combat: Tests de combat

@pytest.mark.skipif(True, reason="Implémenter si vous faites le combat")
def test_battle_between_characters(client):
    """
    Test POST /battle - Combat entre deux personnages.
    
    TODO NIVEAU 3:
    - Créer deux personnages
    - Lancer un combat
    - Vérifier le résultat
    """
    pass


# ==================== TESTS SUPPLÉMENTAIRES ====================

# TODO: Ajoutez vos propres tests ici au fur et à mesure du développement

def test_create_multiple_characters(client):
    """
    Test de création de plusieurs personnages.
    
    TODO:
    - Créer 5 personnages
    - Vérifier que GET /characters retourne 15 personnages (10 + 5)
    """
    # TODO: Implémenter
    pass


def test_invalid_class(client):
    """
    Test création avec une classe invalide.
    
    TODO:
    - Essayer de créer un personnage avec class="invalid"
    - Vérifier l'erreur de validation
    """
    # TODO: Implémenter
    pass