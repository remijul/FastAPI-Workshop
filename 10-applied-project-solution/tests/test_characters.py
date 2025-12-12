"""
Tests pour les endpoints de gestion des personnages.
SOLUTION COMPLÈTE
"""

import pytest


# ==================== NIVEAU 1 : TESTS CRUD DE BASE ====================

def test_read_root(client):
    """Test de la route racine."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_get_all_characters_initial(client):
    """Test GET /characters - Vérifier que 10 personnages sont chargés au démarrage."""
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
    assert "health_points" in first_character
    assert "attack" in first_character
    assert "defense" in first_character
    assert "speed" in first_character
    assert "created_at" in first_character


def test_create_character(client, sample_character_data):
    """Test POST /characters - Créer un personnage."""
    response = client.post("/characters", json=sample_character_data)
    
    # Note: Cette route est protégée en NIVEAU 3, donc on s'attend à un 401 sans auth
    # Pour tester avec auth, voir test_create_character_with_auth
    # En NIVEAU 1-2, cette route n'est pas protégée
    
    # Si pas d'auth implémentée (NIVEAU 1-2):
    if response.status_code == 201:
        data = response.json()
        assert "id" in data
        assert data["name"] == sample_character_data["name"]
        assert data["class"] == sample_character_data["class"]
        assert data["level"] == sample_character_data["level"]
    # Si auth implémentée (NIVEAU 3):
    else:
        assert response.status_code == 401


def test_create_character_invalid_level(client):
    """Test POST /characters - Niveau invalide (hors limites)."""
    invalid_character = {
        "name": "Invalid Char",
        "class": "warrior",
        "level": 150,  # Niveau > 100
        "health_points": 300,
        "attack": 75,
        "defense": 35,
        "speed": 50
    }
    
    response = client.post("/characters", json=invalid_character)
    
    # Peut être 422 (validation Pydantic) ou 401 (si auth protégée)
    assert response.status_code in [422, 401]


def test_create_character_invalid_class(client):
    """Test POST /characters - Classe invalide."""
    invalid_character = {
        "name": "Invalid Char",
        "class": "wizard",  # Classe non valide
        "level": 25,
        "health_points": 300,
        "attack": 75,
        "defense": 35,
        "speed": 50
    }
    
    response = client.post("/characters", json=invalid_character)
    assert response.status_code in [422, 401]


def test_get_character_by_id(client):
    """Test GET /characters/{id} - Récupérer un personnage existant."""
    # Récupérer le premier personnage des données initiales
    response = client.get("/characters/1")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "class" in data


def test_get_character_not_found(client):
    """Test GET /characters/{id} - Personnage non trouvé."""
    response = client.get("/characters/9999")
    assert response.status_code == 404
    
    data = response.json()
    assert "error" in data or "detail" in data


def test_update_character(client):
    """Test PUT /characters/{id} - Modifier un personnage."""
    # Modifier le premier personnage
    update_data = {
        "name": "Updated Name",
        "level": 60
    }
    
    response = client.put("/characters/1", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["level"] == 60


def test_update_character_partial(client):
    """Test PUT /characters/{id} - Mise à jour partielle."""
    # Récupérer le personnage avant modification
    original = client.get("/characters/2").json()
    
    # Modifier uniquement le niveau
    update_data = {"level": 75}
    response = client.put("/characters/2", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["level"] == 75
    # Vérifier que les autres champs n'ont pas changé
    assert data["name"] == original["name"]
    assert data["attack"] == original["attack"]


def test_update_character_not_found(client):
    """Test PUT /characters/{id} - Modifier un personnage inexistant."""
    update_data = {"name": "Ghost"}
    response = client.put("/characters/9999", json=update_data)
    assert response.status_code == 404


def test_delete_character_not_found(client):
    """Test DELETE /characters/{id} - Supprimer un personnage inexistant."""
    response = client.delete("/characters/9999")
    # Peut être 404 ou 401 (si auth protégée)
    assert response.status_code in [404, 401]


# ==================== NIVEAU 2 : TESTS AVANCÉS ====================

def test_filter_by_class(client):
    """Test GET /characters?class=warrior - Filtrer par classe."""
    response = client.get("/characters?class=warrior")
    assert response.status_code == 200
    
    data = response.json()
    # Vérifier que tous les personnages sont des warriors
    for character in data:
        assert character["class"] == "warrior"


def test_filter_by_class_mage(client):
    """Test GET /characters?class=mage - Filtrer par classe mage."""
    response = client.get("/characters?class=mage")
    assert response.status_code == 200
    
    data = response.json()
    for character in data:
        assert character["class"] == "mage"


def test_filter_by_level_min(client):
    """Test GET /characters?min_level=50 - Filtrer par niveau minimum."""
    response = client.get("/characters?min_level=50")
    assert response.status_code == 200
    
    data = response.json()
    for character in data:
        assert character["level"] >= 50


def test_filter_by_level_range(client):
    """Test GET /characters?min_level=50&max_level=80 - Filtrer par niveau."""
    response = client.get("/characters?min_level=50&max_level=80")
    assert response.status_code == 200
    
    data = response.json()
    for character in data:
        assert 50 <= character["level"] <= 80


def test_filter_combined(client):
    """Test GET /characters?class=mage&min_level=60 - Filtres combinés."""
    response = client.get("/characters?class=mage&min_level=60")
    assert response.status_code == 200
    
    data = response.json()
    for character in data:
        assert character["class"] == "mage"
        assert character["level"] >= 60


def test_get_statistics(client):
    """Test GET /characters/stats/global - Récupérer les statistiques."""
    response = client.get("/characters/stats/global")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_characters" in data
    assert "characters_by_class" in data
    assert "average_level" in data
    assert "min_level" in data
    assert "max_level" in data
    assert "average_attack_by_class" in data
    
    # Vérifier que le total correspond aux 10 personnages initiaux
    assert data["total_characters"] == 10


def test_get_classes(client):
    """Test GET /characters/metadata/classes - Liste des classes disponibles."""
    response = client.get("/characters/metadata/classes")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 5
    assert "warrior" in data
    assert "mage" in data
    assert "archer" in data
    assert "tank" in data
    assert "healer" in data


def test_level_up(client):
    """Test POST /characters/{id}/level-up - Augmenter le niveau."""
    # Récupérer un personnage
    character = client.get("/characters/1").json()
    original_level = character["level"]
    original_hp = character["health_points"]
    original_attack = character["attack"]
    original_defense = character["defense"]
    
    # Level up
    response = client.post("/characters/1/level-up")
    assert response.status_code == 200
    
    data = response.json()
    assert data["level"] == original_level + 1
    assert data["health_points"] == original_hp + 10
    assert data["attack"] == original_attack + 2
    assert data["defense"] == original_defense + 1


def test_level_up_not_found(client):
    """Test POST /characters/{id}/level-up - Personnage inexistant."""
    response = client.post("/characters/9999/level-up")
    assert response.status_code == 404


# ==================== NIVEAU 3 : TESTS OPTIONNELS ====================

# NIVEAU 3 - OPTION AUTH

def test_register_user(client):
    """Test POST /auth/register - Inscription."""
    user_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    response = client.post("/auth/register", json=user_data)
    
    # Si l'auth est implémentée
    if response.status_code == 200:
        data = response.json()
        assert "message" in data
    # Sinon, le endpoint n'existe pas
    else:
        assert response.status_code == 404


def test_register_duplicate_user(client):
    """Test POST /auth/register - Username déjà pris."""
    user_data = {
        "username": "duplicate",
        "password": "testpass123"
    }
    
    # Première inscription
    client.post("/auth/register", json=user_data)
    
    # Deuxième inscription (duplicate)
    response = client.post("/auth/register", json=user_data)
    
    if response.status_code == 400:
        data = response.json()
        assert "detail" in data


def test_login(client):
    """Test POST /auth/login - Connexion."""
    # D'abord s'inscrire
    user_data = {
        "username": "logintest",
        "password": "password123"
    }
    client.post("/auth/register", json=user_data)
    
    # Puis se connecter
    response = client.post("/auth/login", json=user_data)
    
    if response.status_code == 200:
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test POST /auth/login - Identifiants incorrects."""
    user_data = {
        "username": "nonexistent",
        "password": "wrongpass"
    }
    
    response = client.post("/auth/login", json=user_data)
    
    if response.status_code == 401:
        data = response.json()
        assert "detail" in data


def test_create_character_without_auth(client, sample_character_data):
    """Test POST /characters sans authentification (si protégé)."""
    response = client.post("/characters", json=sample_character_data)
    
    # Si l'auth est implémentée et la route protégée
    if response.status_code == 401:
        data = response.json()
        assert "detail" in data


def test_create_character_with_auth(client, sample_character_data):
    """Test POST /characters avec authentification."""
    # S'inscrire et se connecter
    user_data = {
        "username": "authuser",
        "password": "authpass123"
    }
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/login", json=user_data)
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Créer un personnage avec le token
        response = client.post("/characters", json=sample_character_data, headers=headers)
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == sample_character_data["name"]


def test_delete_character_with_auth(client):
    """Test DELETE /characters/{id} avec authentification."""
    # S'inscrire et se connecter
    user_data = {
        "username": "deleteuser",
        "password": "deletepass123"
    }
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/login", json=user_data)
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Supprimer un personnage avec le token
        response = client.delete("/characters/3", headers=headers)
        assert response.status_code == 204
        
        # Vérifier que le personnage est bien supprimé
        get_response = client.get("/characters/3")
        assert get_response.status_code == 404


# NIVEAU 3 - OPTION COMBAT

def test_battle_between_characters(client):
    """Test POST /characters/battle - Combat entre deux personnages."""
    battle_data = {
        "character1_id": 1,
        "character2_id": 2
    }
    
    response = client.post("/characters/battle", json=battle_data)
    
    if response.status_code == 200:
        data = response.json()
        assert "winner_id" in data
        assert "loser_id" in data
        assert "turns" in data
        assert "winner_remaining_hp" in data
        assert "battle_log" in data
        
        # Le gagnant doit être l'un des deux personnages
        assert data["winner_id"] in [1, 2]
        assert data["loser_id"] in [1, 2]
        assert data["winner_id"] != data["loser_id"]


def test_battle_character_not_found(client):
    """Test POST /characters/battle - Un des personnages n'existe pas."""
    battle_data = {
        "character1_id": 1,
        "character2_id": 9999
    }
    
    response = client.post("/characters/battle", json=battle_data)
    
    if response.status_code == 404:
        data = response.json()
        assert "error" in data or "detail" in data


# ==================== TESTS SUPPLÉMENTAIRES ====================

def test_create_multiple_characters(client, sample_character_data):
    """Test de création de plusieurs personnages."""
    # Créer 3 personnages (si pas d'auth)
    characters_created = 0
    
    for i in range(3):
        character_data = sample_character_data.copy()
        character_data["name"] = f"Character {i+1}"
        
        response = client.post("/characters", json=character_data)
        if response.status_code == 201:
            characters_created += 1
    
    # Si des personnages ont été créés
    if characters_created > 0:
        # Vérifier le nombre total
        all_characters = client.get("/characters").json()
        assert len(all_characters) >= 10 + characters_created


def test_invalid_class_in_filter(client):
    """Test GET /characters?class=invalid - Classe invalide dans filtre."""
    response = client.get("/characters?class=invalid_class")
    assert response.status_code == 200
    
    # Devrait retourner une liste vide
    data = response.json()
    assert len(data) == 0


def test_health_check(client):
    """Test de l'endpoint de santé."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_invalid_character_name_too_short(client):
    """Test POST /characters - Nom trop court."""
    invalid_character = {
        "name": "A",  # Moins de 2 caractères
        "class": "warrior",
        "level": 25,
        "health_points": 300,
        "attack": 75,
        "defense": 35,
        "speed": 50
    }
    
    response = client.post("/characters", json=invalid_character)
    assert response.status_code in [422, 401]


def test_character_with_special_ability(client, sample_character_data):
    """Test création avec capacité spéciale."""
    character_data = sample_character_data.copy()
    character_data["special_ability"] = "Super Strike"
    
    response = client.post("/characters", json=character_data)
    
    if response.status_code == 201:
        data = response.json()
        assert data["special_ability"] == "Super Strike"


def test_character_with_image_url(client, sample_character_data):
    """Test création avec URL d'image."""
    character_data = sample_character_data.copy()
    character_data["image_url"] = "https://example.com/image.jpg"
    
    response = client.post("/characters", json=character_data)
    
    if response.status_code == 201:
        data = response.json()
        assert data["image_url"] == "https://example.com/image.jpg"


def test_update_character_with_invalid_level(client):
    """Test PUT /characters/{id} - Niveau invalide."""
    update_data = {"level": 150}  # > 100
    
    response = client.put("/characters/1", json=update_data)
    assert response.status_code == 422


def test_get_all_characters_order(client):
    """Test que les personnages sont retournés dans l'ordre."""
    response = client.get("/characters")
    assert response.status_code == 200
    
    data = response.json()
    # Vérifier que les IDs sont dans l'ordre croissant
    ids = [char["id"] for char in data]
    assert ids == sorted(ids)


def test_statistics_after_operations(client):
    """Test des statistiques après plusieurs opérations."""
    # Récupérer les stats initiales
    stats_before = client.get("/characters/stats/global").json()
    initial_total = stats_before["total_characters"]
    
    # Level up un personnage
    client.post("/characters/1/level-up")
    
    # Récupérer les stats après
    stats_after = client.get("/characters/stats/global").json()
    
    # Le total ne devrait pas avoir changé
    assert stats_after["total_characters"] == initial_total
    
    # Mais la moyenne de niveau devrait avoir augmenté
    assert stats_after["average_level"] >= stats_before["average_level"]


def test_filter_no_results(client):
    """Test filtre qui ne retourne aucun résultat."""
    response = client.get("/characters?class=warrior&min_level=99")
    assert response.status_code == 200
    
    data = response.json()
    # Peut être vide ou contenir des résultats selon les données
    assert isinstance(data, list)


# ==================== TESTS DE COUVERTURE ====================

def test_all_initial_characters_have_required_fields(client):
    """Vérifier que tous les personnages initiaux ont les champs requis."""
    response = client.get("/characters")
    characters = response.json()
    
    required_fields = ["id", "name", "class", "level", "health_points", 
                      "attack", "defense", "speed", "created_at"]
    
    for character in characters:
        for field in required_fields:
            assert field in character, f"Champ {field} manquant pour le personnage {character.get('id')}"


def test_character_class_values(client):
    """Vérifier que toutes les classes sont valides."""
    response = client.get("/characters")
    characters = response.json()
    
    valid_classes = ["warrior", "mage", "archer", "tank", "healer"]
    
    for character in characters:
        assert character["class"] in valid_classes


def test_character_level_constraints(client):
    """Vérifier que tous les niveaux sont dans les limites."""
    response = client.get("/characters")
    characters = response.json()
    
    for character in characters:
        assert 1 <= character["level"] <= 100


def test_character_stats_constraints(client):
    """Vérifier que toutes les stats sont dans les limites."""
    response = client.get("/characters")
    characters = response.json()
    
    for character in characters:
        assert 50 <= character["health_points"] <= 500
        assert 10 <= character["attack"] <= 100
        assert 5 <= character["defense"] <= 50
        assert 10 <= character["speed"] <= 100