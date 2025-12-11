# Architecture API Gestion de Personnages - Mini-Projet Final
## Module 10 - Applied Project (Solution Complète)

---

## 🏗️ Vue d'ensemble de l'architecture complète (3 niveaux)

```mermaid
graph TB
    subgraph "🌐 COUCHE PRÉSENTATION"
        R1[routes.py<br/>Router API /characters]
        R2[auth_router<br/>Router /auth]
        R3[Routes Web<br/>Jinja2 Templates]
    end
    
    subgraph "🔐 COUCHE SÉCURITÉ"
        D1[dependencies.py<br/>get_current_user]
        A1[auth.py<br/>JWT + Bcrypt]
    end
    
    subgraph "💼 COUCHE MÉTIER - Services"
        S1[CharacterService<br/>CRUD + Level-up]
        S2[BattleService<br/>Simulate battle]
        S3[AuthService<br/>Register + Authenticate]
    end
    
    subgraph "🗄️ COUCHE DONNÉES - Repositories"
        REP1[CharacterRepository<br/>SQL Characters]
        REP2[UserRepository<br/>SQL Users]
    end
    
    subgraph "🔧 COUCHE UTILITAIRES"
        U1[database.py<br/>Connexions + Init]
        U2[config.py<br/>Configuration]
        U3[exceptions.py<br/>4 Exceptions custom]
    end
    
    subgraph "📦 COUCHE MODÈLES"
        M1[models.py<br/>13 Modèles Pydantic]
    end
    
    subgraph "🎨 COUCHE PRÉSENTATION WEB"
        T1[templates/<br/>HTML Jinja2]
        ST1[static/<br/>CSS + JS]
    end
    
    subgraph "💾 BASE DE DONNÉES"
        DB[(SQLite<br/>characters table<br/>users table)]
    end
    
    R1 --> D1
    R2 --> S3
    R3 --> S1
    
    D1 --> A1
    
    R1 --> S1
    R1 --> S2
    R2 --> S3
    
    S1 --> REP1
    S2 --> REP1
    S3 --> REP2
    S3 --> A1
    
    REP1 --> U1
    REP2 --> U1
    
    U1 --> DB
    U1 --> U2
    
    R1 -.utilise.-> M1
    R2 -.utilise.-> M1
    R3 -.utilise.-> M1
    S1 -.utilise.-> M1
    S2 -.utilise.-> M1
    S3 -.utilise.-> M1
    
    S1 -.lève.-> U3
    S2 -.lève.-> U3
    
    R3 --> T1
    R3 --> ST1
    
    style R1 fill:#e1f5ff
    style R2 fill:#e1f5ff
    style R3 fill:#bbdefb
    style D1 fill:#fff4e6
    style A1 fill:#fce4ec
    style S1 fill:#e8f5e9
    style S2 fill:#e8f5e9
    style S3 fill:#e8f5e9
    style REP1 fill:#f3e5f5
    style REP2 fill:#f3e5f5
    style U1 fill:#fff3e0
    style U2 fill:#fff3e0
    style U3 fill:#ffcdd2
    style M1 fill:#fff9c4
    style T1 fill:#e0f2f1
    style ST1 fill:#e0f2f1
    style DB fill:#ffebee
```

---

## 📊 Architecture en 3 niveaux de complexité

```mermaid
graph LR
    subgraph "🟢 NIVEAU 1 - CRUD Basique"
        N1_1[5 Endpoints CRUD]
        N1_2[CharacterBase Models]
        N1_3[SQLite + 10 personnages]
        N1_4[Validation Pydantic]
        N1_5[Architecture 3 couches]
    end
    
    subgraph "🟡 NIVEAU 2 - Fonctionnalités Avancées"
        N2_1[Filtres query params]
        N2_2[Statistiques globales]
        N2_3[Level-up endpoint]
        N2_4[4 Exceptions custom]
        N2_5[Gestionnaires exceptions]
    end
    
    subgraph "🔴 NIVEAU 3 - Extensions Complètes"
        N3_1[JWT Authentication]
        N3_2[Combat système]
        N3_3[Interface web Jinja2]
        N3_4[Protection endpoints]
        N3_5[Templates + CSS]
    end
    
    N1_1 --> N2_1
    N1_2 --> N2_2
    N1_3 --> N2_3
    N1_4 --> N2_4
    N1_5 --> N2_5
    
    N2_1 --> N3_1
    N2_2 --> N3_2
    N2_3 --> N3_3
    N2_4 --> N3_4
    N2_5 --> N3_5
    
    style N1_1 fill:#c8e6c9
    style N1_2 fill:#c8e6c9
    style N1_3 fill:#c8e6c9
    style N1_4 fill:#c8e6c9
    style N1_5 fill:#c8e6c9
    
    style N2_1 fill:#fff59d
    style N2_2 fill:#fff59d
    style N2_3 fill:#fff59d
    style N2_4 fill:#fff59d
    style N2_5 fill:#fff59d
    
    style N3_1 fill:#ffccbc
    style N3_2 fill:#ffccbc
    style N3_3 fill:#ffccbc
    style N3_4 fill:#ffccbc
    style N3_5 fill:#ffccbc
```

---

## 🔄 Flux CRUD complet (Niveau 1)

```mermaid
sequenceDiagram
    participant Client
    participant Routes as routes.py
    participant Service as CharacterService
    participant Repo as CharacterRepository
    participant DB as SQLite

    rect rgb(240, 255, 240)
        Note over Client,DB: ✅ CREATE - POST /characters
        Client->>Routes: POST /characters<br/>{name, class, level, ...}
        Routes->>Service: create_character(CharacterCreate)
        Service->>Repo: create(name, class, level, ...)
        Repo->>DB: INSERT INTO characters (...)
        DB-->>Repo: character_id = 11
        Repo-->>Service: 11
        Service->>Repo: get_by_id(11)
        Repo->>DB: SELECT * WHERE id = 11
        DB-->>Repo: character_data
        Repo-->>Service: dict
        Service-->>Routes: CharacterResponse.model_validate()
        Routes-->>Client: 201 Created + character
    end

    rect rgb(255, 250, 240)
        Note over Client,DB: 📖 READ - GET /characters
        Client->>Routes: GET /characters
        Routes->>Service: get_all_characters()
        Service->>Repo: get_all()
        Repo->>DB: SELECT * FROM characters
        DB-->>Repo: [char1, char2, ...]
        Repo-->>Service: [dict, dict, ...]
        Service-->>Routes: [CharacterResponse, ...]
        Routes-->>Client: 200 OK + characters
    end

    rect rgb(230, 240, 255)
        Note over Client,DB: 🔍 READ ONE - GET /characters/{id}
        Client->>Routes: GET /characters/5
        Routes->>Service: get_character(5)
        Service->>Repo: get_by_id(5)
        Repo->>DB: SELECT * WHERE id = 5
        
        alt Personnage trouvé
            DB-->>Repo: character_data
            Repo-->>Service: dict
            Service-->>Routes: CharacterResponse
            Routes-->>Client: 200 OK + character
        else Personnage non trouvé
            DB-->>Repo: None
            Repo-->>Service: None
            Service-->>Routes: CharacterNotFoundError
            Routes-->>Client: 404 Not Found
        end
    end

    rect rgb(255, 245, 230)
        Note over Client,DB: ✏️ UPDATE - PUT /characters/{id}
        Client->>Routes: PUT /characters/5<br/>{level: 50}
        Routes->>Service: update_character(5, CharacterUpdate)
        Service->>Repo: get_by_id(5)
        Repo-->>Service: character exists ✅
        Service->>Service: extract updates (exclude_unset)
        Service->>Repo: update(5, level=50)
        Repo->>DB: UPDATE characters SET level = 50 WHERE id = 5
        DB-->>Repo: rowcount = 1
        Repo-->>Service: True
        Service->>Repo: get_by_id(5)
        Repo->>DB: SELECT * WHERE id = 5
        DB-->>Repo: updated_character
        Repo-->>Service: dict
        Service-->>Routes: CharacterResponse
        Routes-->>Client: 200 OK + updated character
    end

    rect rgb(255, 235, 238)
        Note over Client,DB: ❌ DELETE - DELETE /characters/{id}
        Client->>Routes: DELETE /characters/5
        Routes->>Service: delete_character(5)
        Service->>Repo: get_by_id(5)
        Repo-->>Service: character exists ✅
        Service->>Repo: delete(5)
        Repo->>DB: DELETE FROM characters WHERE id = 5
        DB-->>Repo: rowcount = 1
        Repo-->>Service: True
        Service-->>Routes: None
        Routes-->>Client: 204 No Content
    end
```

---

## 🔍 Flux de filtrage avancé (Niveau 2)

```mermaid
sequenceDiagram
    participant Client
    participant Routes as routes.py
    participant Service as CharacterService
    participant Repo as CharacterRepository
    participant DB as SQLite

    rect rgb(240, 248, 255)
        Note over Client,DB: 🔎 FILTRAGE - GET /characters?class=warrior&min_level=30
        Client->>Routes: GET /characters?class=warrior&min_level=30
        Routes->>Routes: Extraire query params
        Routes->>Service: get_characters_filtered(class="warrior", min_level=30)
        Service->>Repo: get_by_filters(class="warrior", min_level=30)
        Repo->>Repo: Construire query dynamique
        Repo->>DB: SELECT * WHERE class = 'warrior'<br/>AND level >= 30
        DB-->>Repo: [warrior1, warrior2]
        Repo-->>Service: [dict, dict]
        Service-->>Routes: [CharacterResponse, CharacterResponse]
        Routes-->>Client: 200 OK + filtered characters
    end

    rect rgb(245, 255, 245)
        Note over Client,DB: 📊 STATISTIQUES - GET /characters/stats/global
        Client->>Routes: GET /characters/stats/global
        Routes->>Service: get_statistics()
        Service->>Repo: get_stats()
        Repo->>DB: SELECT COUNT(*) FROM characters
        DB-->>Repo: total = 10
        Repo->>DB: SELECT class, COUNT(*) GROUP BY class
        DB-->>Repo: {warrior: 3, mage: 2, ...}
        Repo->>DB: SELECT AVG(level), MIN(level), MAX(level)
        DB-->>Repo: avg=45, min=10, max=80
        Repo->>DB: SELECT class, AVG(attack) GROUP BY class
        DB-->>Repo: {warrior: 75, mage: 65, ...}
        Repo-->>Service: stats dict
        Service-->>Routes: stats dict
        Routes-->>Client: 200 OK + statistics
    end

    rect rgb(255, 250, 240)
        Note over Client,DB: ⬆️ LEVEL UP - POST /characters/{id}/level-up
        Client->>Routes: POST /characters/5/level-up
        Routes->>Service: level_up(5)
        Service->>Repo: get_by_id(5)
        Repo-->>Service: {level: 49, hp: 300, attack: 70, defense: 30}
        
        alt Niveau < 100
            Service->>Service: Calculer nouvelles stats<br/>level+1, hp+10, attack+2, defense+1
            Service->>Repo: update(5, level=50, hp=310, attack=72, defense=31)
            Repo->>DB: UPDATE characters SET ...
            DB-->>Repo: success
            Service->>Repo: get_by_id(5)
            Repo-->>Service: updated character
            Service-->>Routes: CharacterResponse
            Routes-->>Client: 200 OK + leveled up character
        else Niveau = 100
            Service-->>Routes: MaxLevelReachedError
            Routes-->>Client: 400 Bad Request
        end
    end
```

---

## 🛡️ Flux d'authentification JWT (Niveau 3)

```mermaid
sequenceDiagram
    participant Client
    participant AuthRouter as auth_router
    participant AuthService
    participant UserRepo as UserRepository
    participant Auth as auth.py
    participant DB as SQLite

    rect rgb(230, 245, 255)
        Note over Client,DB: 📝 INSCRIPTION - POST /auth/register
        Client->>AuthRouter: POST /auth/register<br/>{username, password}
        AuthRouter->>AuthService: register(username, password)
        AuthService->>UserRepo: get_by_username(username)
        UserRepo->>DB: SELECT * FROM users WHERE username = ?
        DB-->>UserRepo: None (nouveau user)
        UserRepo-->>AuthService: None
        AuthService->>Auth: hash_password(password)
        Auth-->>AuthService: hashed_password
        AuthService->>UserRepo: create(username, hashed_password)
        UserRepo->>DB: INSERT INTO users (...)
        DB-->>UserRepo: user_id
        UserRepo-->>AuthService: user_id
        AuthService-->>AuthRouter: True
        AuthRouter-->>Client: 200 OK {"message": "Utilisateur créé"}
    end

    rect rgb(240, 255, 240)
        Note over Client,DB: 🔐 CONNEXION - POST /auth/login
        Client->>AuthRouter: POST /auth/login<br/>{username, password}
        AuthRouter->>AuthService: authenticate(username, password)
        AuthService->>UserRepo: get_by_username(username)
        UserRepo->>DB: SELECT * FROM users WHERE username = ?
        DB-->>UserRepo: {id, username, hashed_password}
        UserRepo-->>AuthService: user dict
        AuthService->>Auth: pwd_context.verify(password, hashed)
        Auth-->>AuthService: True
        AuthService-->>AuthRouter: True
        AuthRouter->>Auth: create_access_token({"sub": username})
        Auth-->>AuthRouter: JWT token
        AuthRouter-->>Client: {"access_token": "eyJ...", "token_type": "bearer"}
    end

    rect rgb(255, 245, 230)
        Note over Client,DB: 🔒 ENDPOINT PROTÉGÉ - POST /characters
        Client->>Router: POST /characters<br/>Authorization: Bearer eyJ...
        Router->>Dependencies: get_current_user(authorization)
        Dependencies->>Dependencies: Extraire Bearer token
        Dependencies->>Auth: decode_access_token(token)
        
        alt Token valide
            Auth-->>Dependencies: {"sub": "alice", "exp": ...}
            Dependencies-->>Router: username = "alice"
            Router->>Service: create_character(data)
            Service-->>Router: CharacterResponse
            Router-->>Client: 201 Created + character
        else Token invalide/expiré
            Auth-->>Dependencies: JWTError
            Dependencies-->>Router: HTTPException(401)
            Router-->>Client: 401 Unauthorized
        end
    end
```

---

## ⚔️ Système de combat (Niveau 3)

```mermaid
sequenceDiagram
    participant Client
    participant Routes
    participant BattleService
    participant CharRepo as CharacterRepository
    participant DB

    Client->>Routes: POST /characters/battle<br/>{character1_id: 3, character2_id: 7}
    Routes->>BattleService: simulate_battle(3, 7)
    
    BattleService->>CharRepo: get_by_id(3)
    CharRepo->>DB: SELECT * WHERE id = 3
    DB-->>CharRepo: Gandalf {speed: 85, attack: 80, defense: 30, hp: 350}
    CharRepo-->>BattleService: char1_data
    
    BattleService->>CharRepo: get_by_id(7)
    CharRepo->>DB: SELECT * WHERE id = 7
    DB-->>CharRepo: Legolas {speed: 95, attack: 75, defense: 25, hp: 300}
    CharRepo-->>BattleService: char2_data
    
    BattleService->>BattleService: Comparer speed<br/>Legolas attaque en premier (95 > 85)
    
    loop Combat tour par tour
        BattleService->>BattleService: Tour N: Attaquant calcule dégâts<br/>damage = max(1, attack - defense)
        BattleService->>BattleService: Appliquer dégâts au défenseur<br/>defender_hp -= damage
        BattleService->>BattleService: Ajouter au battle_log
        
        alt Défenseur HP > 0
            BattleService->>BattleService: Inverser attaquant/défenseur<br/>Continuer
        else Défenseur HP <= 0
            BattleService->>BattleService: Combat terminé<br/>Déterminer gagnant
        end
    end
    
    BattleService-->>Routes: BattleResult {<br/>winner: Legolas,<br/>turns: 8,<br/>remaining_hp: 120,<br/>battle_log: [...]<br/>}
    Routes-->>Client: 200 OK + battle result
```

---

## 📊 Relations entre classes et méthodes

```mermaid
classDiagram
    class main {
        +FastAPI app
        +init_database()
        +init_users_table()
        +mount("/static")
        +include_router(router)
        +include_router(auth_router)
        +4 exception_handlers()
        +root() dict
        +health_check() dict
    }
    
    class config {
        <<Configuration>>
        +DATABASE_PATH str
        +DATA_DIR Path
        +VALID_CLASSES list
        +SECRET_KEY str
        +ALGORITHM str
        +ACCESS_TOKEN_EXPIRE_MINUTES int
        +APP_NAME str
        +VERSION str
        +DEBUG bool
    }
    
    class routes {
        <<APIRouter>>
        +router /characters
        +auth_router /auth
        --NIVEAU 1 CRUD--
        +create_character(CharacterCreate) CharacterResponse
        +get_characters(filters) list~CharacterResponse~
        +get_character(id) CharacterResponse
        +update_character(id, update) CharacterResponse
        +delete_character(id) None
        --NIVEAU 2--
        +get_statistics() dict
        +level_up_character(id) CharacterResponse
        +get_classes() list~str~
        --NIVEAU 3 COMBAT--
        +battle(BattleRequest) BattleResult
        --NIVEAU 3 WEB--
        +home_page(filters) HTMLResponse
        +character_detail_page(id) HTMLResponse
        +battle_page() HTMLResponse
        --NIVEAU 3 AUTH--
        +register(UserRegister) dict
        +login(UserLogin) Token
    }
    
    class dependencies {
        <<Security>>
        +get_current_user(authorization) str
    }
    
    class auth {
        <<Utilities>>
        +pwd_context CryptContext
        +hash_password(password) str
        +verify_password(plain, hashed) bool
        +create_access_token(data) str
        +decode_access_token(token) dict
    }
    
    class CharacterService {
        <<Service>>
        --NIVEAU 1--
        +create_character(CharacterCreate) CharacterResponse
        +get_character(id) CharacterResponse
        +get_all_characters() list~CharacterResponse~
        +update_character(id, update) CharacterResponse
        +delete_character(id) None
        --NIVEAU 2--
        +get_characters_filtered(filters) list~CharacterResponse~
        +get_statistics() dict
        +level_up(id) CharacterResponse
    }
    
    class BattleService {
        <<Service - Niveau 3>>
        +simulate_battle(char1_id, char2_id) dict
    }
    
    class AuthService {
        <<Service - Niveau 3>>
        +pwd_context CryptContext
        +register(username, password) bool
        +authenticate(username, password) bool
    }
    
    class CharacterRepository {
        <<Repository>>
        --NIVEAU 1--
        +create(...) int
        +get_by_id(id) dict | None
        +get_all() list~dict~
        +update(id, **updates) bool
        +delete(id) bool
        --NIVEAU 2--
        +get_by_filters(class, min, max) list~dict~
        +get_stats() dict
    }
    
    class UserRepository {
        <<Repository - Niveau 3>>
        +create(username, hashed_pwd) int
        +get_by_username(username) dict | None
    }
    
    class database {
        <<Utilities>>
        +get_db_connection() Connection
        +init_database() None
        +load_initial_data(cursor) None
        +init_users_table() None
    }
    
    class exceptions {
        <<Custom Exceptions>>
        +CharacterNotFoundError
        +InvalidClassError
        +InvalidLevelError
        +MaxLevelReachedError
    }
    
    class models {
        <<Pydantic Models>>
        --NIVEAU 1--
        +CharacterBase
        +CharacterCreate
        +CharacterUpdate
        +CharacterResponse
        --NIVEAU 2--
        +CharacterStats
        +ClassInfo
        --NIVEAU 3 COMBAT--
        +BattleRequest
        +BattleResult
        --NIVEAU 3 AUTH--
        +UserRegister
        +UserLogin
        +Token
    }
    
    main --> routes
    main --> database
    main --> exceptions
    
    routes --> dependencies : Depends()
    routes --> CharacterService
    routes --> BattleService
    routes --> AuthService
    routes ..> models : uses
    
    dependencies --> auth
    
    CharacterService --> CharacterRepository
    CharacterService ..> exceptions : raises
    CharacterService ..> models : uses
    
    BattleService --> CharacterRepository
    BattleService ..> exceptions : raises
    BattleService ..> models : uses
    
    AuthService --> UserRepository
    AuthService --> auth
    AuthService ..> models : uses
    
    CharacterRepository --> database
    UserRepository --> database
    
    database --> config
    database --> SQLite
    
    auth --> config
```

---

## 🎯 Matrice des responsabilités détaillée

```mermaid
graph TB
    subgraph "📄 main.py"
        MA1[Init FastAPI app]
        MA2[Init database]
        MA3[Mount static files]
        MA4[Include routers]
        MA5[4 Exception handlers]
        MA6[Root + Health endpoints]
    end
    
    subgraph "📄 config.py"
        CO1[DATABASE_PATH]
        CO2[VALID_CLASSES]
        CO3[JWT SECRET_KEY]
        CO4[APP_NAME + VERSION]
    end
    
    subgraph "📄 routes.py"
        RO1[15 Endpoints API]
        RO2[3 Endpoints Web HTML]
        RO3[2 Endpoints Auth]
        RO4[Query parameters]
        RO5[Depends injection]
    end
    
    subgraph "📄 dependencies.py"
        DE1[get_current_user]
        DE2[Extract Bearer token]
        DE3[Decode JWT]
        DE4[Return username]
        DE5[Raise 401 errors]
    end
    
    subgraph "📄 auth.py"
        AU1[pwd_context bcrypt]
        AU2[hash_password]
        AU3[verify_password]
        AU4[create_access_token JWT]
        AU5[decode_access_token]
    end
    
    subgraph "📄 services.py"
        SE1[CharacterService<br/>8 méthodes]
        SE2[BattleService<br/>simulate_battle]
        SE3[AuthService<br/>register + authenticate]
        SE4[Logique métier]
        SE5[Validation business]
        SE6[Lever exceptions]
    end
    
    subgraph "📄 repositories.py"
        RE1[CharacterRepository<br/>7 méthodes SQL]
        RE2[UserRepository<br/>2 méthodes SQL]
        RE3[Requêtes INSERT]
        RE4[Requêtes SELECT]
        RE5[Requêtes UPDATE]
        RE6[Requêtes DELETE]
        RE7[Agrégations stats]
    end
    
    subgraph "📄 database.py"
        DA1[get_db_connection]
        DA2[init_database]
        DA3[load_initial_data JSON]
        DA4[init_users_table]
        DA5[CREATE TABLE characters]
        DA6[CREATE TABLE users]
    end
    
    subgraph "📄 exceptions.py"
        EX1[CharacterNotFoundError]
        EX2[InvalidClassError]
        EX3[InvalidLevelError]
        EX4[MaxLevelReachedError]
    end
    
    subgraph "📄 models.py"
        MO1[CharacterBase]
        MO2[CharacterCreate + validators]
        MO3[CharacterUpdate]
        MO4[CharacterResponse]
        MO5[CharacterStats]
        MO6[BattleRequest + Result]
        MO7[UserRegister + Login]
        MO8[Token]
    end
    
    style MA1 fill:#e3f2fd
    style MA2 fill:#e3f2fd
    style MA3 fill:#e3f2fd
    style MA4 fill:#e3f2fd
    style MA5 fill:#e3f2fd
    style MA6 fill:#e3f2fd
    
    style CO1 fill:#fff3e0
    style CO2 fill:#fff3e0
    style CO3 fill:#fff3e0
    style CO4 fill:#fff3e0
    
    style RO1 fill:#e1f5ff
    style RO2 fill:#e1f5ff
    style RO3 fill:#e1f5ff
    style RO4 fill:#e1f5ff
    style RO5 fill:#e1f5ff
    
    style DE1 fill:#fff4e6
    style DE2 fill:#fff4e6
    style DE3 fill:#fff4e6
    style DE4 fill:#fff4e6
    style DE5 fill:#fff4e6
    
    style AU1 fill:#fce4ec
    style AU2 fill:#fce4ec
    style AU3 fill:#fce4ec
    style AU4 fill:#fce4ec
    style AU5 fill:#fce4ec
    
    style SE1 fill:#e8f5e9
    style SE2 fill:#e8f5e9
    style SE3 fill:#e8f5e9
    style SE4 fill:#e8f5e9
    style SE5 fill:#e8f5e9
    style SE6 fill:#e8f5e9
    
    style RE1 fill:#f3e5f5
    style RE2 fill:#f3e5f5
    style RE3 fill:#f3e5f5
    style RE4 fill:#f3e5f5
    style RE5 fill:#f3e5f5
    style RE6 fill:#f3e5f5
    style RE7 fill:#f3e5f5
    
    style DA1 fill:#fff9c4
    style DA2 fill:#fff9c4
    style DA3 fill:#fff9c4
    style DA4 fill:#fff9c4
    style DA5 fill:#fff9c4
    style DA6 fill:#fff9c4
    
    style EX1 fill:#ffccbc
    style EX2 fill:#ffccbc
    style EX3 fill:#ffccbc
    style EX4 fill:#ffccbc
    
    style MO1 fill:#c5e1a5
    style MO2 fill:#c5e1a5
    style MO3 fill:#c5e1a5
    style MO4 fill:#c5e1a5
    style MO5 fill:#c5e1a5
    style MO6 fill:#c5e1a5
    style MO7 fill:#c5e1a5
    style MO8 fill:#c5e1a5
```

---

## 🗺️ Cartographie des endpoints (20 endpoints)

```mermaid
graph LR
    subgraph "🟢 NIVEAU 1 - CRUD (5 endpoints)"
        E1["POST /characters<br/>🔒 Protected"]
        E2["GET /characters<br/>✅ Public"]
        E3["GET /characters/ID<br/>✅ Public"]
        E4["PUT /characters/ID<br/>✅ Public"]
        E5["DELETE /characters/ID<br/>🔒 Protected"]
    end
    
    subgraph "🟡 NIVEAU 2 - Avancé (4 endpoints)"
        E6["GET /characters?class=...<br/>✅ Public"]
        E7["GET /characters/stats/global<br/>✅ Public"]
        E8["POST /characters/ID/level-up<br/>✅ Public"]
        E9["GET /characters/metadata/classes<br/>✅ Public"]
    end
    
    subgraph "🔴 NIVEAU 3 - Extensions (8 endpoints)"
        E10["POST /characters/battle<br/>✅ Public"]
        E11["GET /characters/web/home<br/>🌐 Web"]
        E12["GET /characters/ID/details<br/>🌐 Web"]
        E13["GET /characters/web/battle<br/>🌐 Web"]
        E14["POST /auth/register<br/>✅ Public"]
        E15["POST /auth/login<br/>✅ Public"]
        E16["GET /<br/>✅ Public"]
        E17["GET /health<br/>✅ Public"]
    end
    
    E1 -.upgrade.-> E5
    E2 -.add filters.-> E6
    E3 -.add stats.-> E7
    E4 -.add level-up.-> E8
    
    E8 -.add combat.-> E10
    E2 -.add web UI.-> E11
    E3 -.add web detail.-> E12
    E10 -.add web battle.-> E13
    
    style E1 fill:#c8e6c9
    style E2 fill:#c8e6c9
    style E3 fill:#c8e6c9
    style E4 fill:#c8e6c9
    style E5 fill:#c8e6c9
    
    style E6 fill:#fff59d
    style E7 fill:#fff59d
    style E8 fill:#fff59d
    style E9 fill:#fff59d
    
    style E10 fill:#ffccbc
    style E11 fill:#bbdefb
    style E12 fill:#bbdefb
    style E13 fill:#bbdefb
    style E14 fill:#ffccbc
    style E15 fill:#ffccbc
    style E16 fill:#e0e0e0
    style E17 fill:#e0e0e0
```

---

## 🔄 Gestion des exceptions (Niveau 2)

```mermaid
flowchart TD
    START([Requête entrante]) --> SERVICE[Exécution service]
    
    SERVICE --> CHECK{Exception<br/>levée ?}
    
    CHECK -->|Non| SUCCESS["✅ Réponse normale<br/>200/201/204"]
    
    CHECK -->|CharacterNotFoundError| EXC1[Exception Handler]
    EXC1 --> ERR1["❌ 404 Not Found<br/>error, message, character_id"]
    
    CHECK -->|InvalidClassError| EXC2[Exception Handler]
    EXC2 --> ERR2["❌ 400 Bad Request<br/>error, message, provided_class, valid_classes"]
    
    CHECK -->|InvalidLevelError| EXC3[Exception Handler]
    EXC3 --> ERR3["❌ 400 Bad Request<br/>error, message, provided_level, min, max"]
    
    CHECK -->|MaxLevelReachedError| EXC4[Exception Handler]
    EXC4 --> ERR4["❌ 400 Bad Request<br/>error, message, character_id, max_level"]
    
    SUCCESS --> END([Réponse client])
    ERR1 --> END
    ERR2 --> END
    ERR3 --> END
    ERR4 --> END
    
    style START fill:#c8e6c9
    style SUCCESS fill:#c8e6c9
    style SERVICE fill:#bbdefb
    style EXC1 fill:#fff9c4
    style EXC2 fill:#fff9c4
    style EXC3 fill:#fff9c4
    style EXC4 fill:#fff9c4
    style ERR1 fill:#ffcdd2
    style ERR2 fill:#ffcdd2
    style ERR3 fill:#ffcdd2
    style ERR4 fill:#ffcdd2
    style END fill:#e0e0e0
```

---

## 📋 Tableau récapitulatif complet

| Endpoint | Méthode | Auth | Niveau | Service | Repository | Description |
|----------|---------|------|--------|---------|------------|-------------|
| `/` | GET | ❌ | 1 | - | - | Documentation API |
| `/health` | GET | ❌ | 3 | - | - | Health check |
| `/characters` | POST | ✅ JWT | 1 | `CharacterService.create_character()` | `CharacterRepository.create()` | Créer personnage |
| `/characters` | GET | ❌ | 1 | `CharacterService.get_all_characters()` | `CharacterRepository.get_all()` | Lister tous |
| `/characters?filters` | GET | ❌ | 2 | `CharacterService.get_characters_filtered()` | `CharacterRepository.get_by_filters()` | Filtrer par classe/niveau |
| `/characters/{id}` | GET | ❌ | 1 | `CharacterService.get_character()` | `CharacterRepository.get_by_id()` | Obtenir un personnage |
| `/characters/{id}` | PUT | ❌ | 1 | `CharacterService.update_character()` | `CharacterRepository.update()` | Modifier personnage |
| `/characters/{id}` | DELETE | ✅ JWT | 1 | `CharacterService.delete_character()` | `CharacterRepository.delete()` | Supprimer personnage |
| `/characters/stats/global` | GET | ❌ | 2 | `CharacterService.get_statistics()` | `CharacterRepository.get_stats()` | Statistiques globales |
| `/characters/{id}/level-up` | POST | ❌ | 2 | `CharacterService.level_up()` | `CharacterRepository.update()` | Augmenter niveau |
| `/characters/metadata/classes` | GET | ❌ | 2 | - | - | Liste classes valides |
| `/characters/battle` | POST | ❌ | 3 | `BattleService.simulate_battle()` | `CharacterRepository.get_by_id()` | Combat entre 2 personnages |
| `/characters/web/home` | GET | ❌ | 3 | `CharacterService.*` | - | Page web liste |
| `/characters/{id}/details` | GET | ❌ | 3 | `CharacterService.get_character()` | - | Page web détail |
| `/characters/web/battle` | GET | ❌ | 3 | `CharacterService.get_all_characters()` | - | Page web combat |
| `/auth/register` | POST | ❌ | 3 | `AuthService.register()` | `UserRepository.create()` | Inscription |
| `/auth/login` | POST | ❌ | 3 | `AuthService.authenticate()` | `UserRepository.get_by_username()` | Connexion JWT |

---

## 🎨 Architecture web avec Jinja2 (Niveau 3)

```mermaid
graph TB
    subgraph "🌐 Client Browser"
        BR[Navigateur]
    end
    
    subgraph "📄 FastAPI Routes Web"
        R1["GET /characters/web/home"]
        R2["GET /characters/ID/details"]
        R3["GET /characters/web/battle"]
    end
    
    subgraph "🎭 Templates Jinja2"
        T1["base.html<br/>Layout commun"]
        T2["home.html<br/>Liste + Filtres"]
        T3["character_detail.html<br/>Fiche personnage"]
        T4["battle.html<br/>Arène combat"]
    end
    
    subgraph "🎨 Static Files"
        S1["style.css<br/>Design moderne"]
        S2["script.js<br/>Interactivité"]
    end
    
    subgraph "💼 Services"
        SV1[CharacterService]
        SV2[BattleService]
    end
    
    subgraph "🗄️ Repository"
        REP[CharacterRepository]
    end
    
    BR -->|HTTP GET| R1
    BR -->|HTTP GET| R2
    BR -->|HTTP GET| R3
    
    R1 --> SV1
    R2 --> SV1
    R3 --> SV1
    R3 --> SV2
    
    SV1 --> REP
    SV2 --> REP
    
    R1 --> T2
    R2 --> T3
    R3 --> T4
    
    T2 --> T1
    T3 --> T1
    T4 --> T1
    
    T1 --> S1
    T1 --> S2
    
    T2 -->|render HTML| BR
    T3 -->|render HTML| BR
    T4 -->|render HTML| BR
    
    style BR fill:#bbdefb
    style R1 fill:#e1f5ff
    style R2 fill:#e1f5ff
    style R3 fill:#e1f5ff
    style T1 fill:#e0f2f1
    style T2 fill:#e0f2f1
    style T3 fill:#e0f2f1
    style T4 fill:#e0f2f1
    style S1 fill:#f1f8e9
    style S2 fill:#f1f8e9
    style SV1 fill:#e8f5e9
    style SV2 fill:#e8f5e9
    style REP fill:#f3e5f5
```

---

## 🎓 Concepts clés appliqués

```mermaid
mindmap
  root((Mini-Projet<br/>API Characters))
    NIVEAU 1 - Fondations
      Architecture 3 couches
        Routes → Services → Repositories
      CRUD complet
        Create, Read, Update, Delete
      Validation Pydantic
        13 modèles avec contraintes
      SQLite + données initiales
        10 personnages JSON
      Configuration centralisée
        config.py
    
    NIVEAU 2 - Avancé
      Filtres query params
        class, min_level, max_level
      Statistiques SQL
        COUNT, AVG, GROUP BY
      Level-up avec règles
        +1 level, +10 HP, +2 ATK
      Exceptions personnalisées
        4 types + handlers
      Validation métier
        VALID_CLASSES, level 1-100
    
    NIVEAU 3 - Extensions
      JWT Authentication
        register, login, protect
      Système de combat
        Tour par tour, battle_log
      Interface web Jinja2
        3 pages HTML + CSS
      Protection endpoints
        Depends get_current_user
      Architecture modulaire
        auth.py, dependencies.py
```

---

## 📊 Modèle de données

```mermaid
erDiagram
    CHARACTERS ||--o{ BATTLES : "participent"
    USERS ||--o{ CHARACTERS : "créent"
    
    CHARACTERS {
        int id PK
        text name
        text class "warrior|mage|archer|tank|healer"
        int level "1-100"
        int health_points "50-500"
        int attack "10-100"
        int defense "5-50"
        int speed "10-100"
        text special_ability
        text image_url
        timestamp created_at
    }
    
    USERS {
        int id PK
        text username UK
        text hashed_password
    }
    
    BATTLES {
        int character1_id FK
        int character2_id FK
        int winner_id FK
        int turns
        int winner_remaining_hp
        json battle_log
    }
```

---

## 🔑 Points d'apprentissage progressifs

```mermaid
graph TD
    subgraph "🟢 Compétences Niveau 1"
        C1[Routes FastAPI]
        C2[Modèles Pydantic]
        C3[SQLite + cursor]
        C4[Architecture layered]
        C5[Status codes HTTP]
    end
    
    subgraph "🟡 Compétences Niveau 2"
        C6[Query parameters]
        C7[Exceptions custom]
        C8[Handlers d'exceptions]
        C9[Agrégations SQL]
        C10[Logique métier complexe]
    end
    
    subgraph "🔴 Compétences Niveau 3"
        C11[JWT + bcrypt]
        C12[Dependencies injection]
        C13[Jinja2 templates]
        C14[Static files]
        C15[Algorithmes de combat]
    end
    
    C1 --> C6
    C2 --> C7
    C3 --> C9
    C4 --> C10
    C5 --> C8
    
    C6 --> C11
    C7 --> C12
    C9 --> C13
    C10 --> C14
    C8 --> C15
    
    style C1 fill:#c8e6c9
    style C2 fill:#c8e6c9
    style C3 fill:#c8e6c9
    style C4 fill:#c8e6c9
    style C5 fill:#c8e6c9
    
    style C6 fill:#fff59d
    style C7 fill:#fff59d
    style C8 fill:#fff59d
    style C9 fill:#fff59d
    style C10 fill:#fff59d
    
    style C11 fill:#ffccbc
    style C12 fill:#ffccbc
    style C13 fill:#ffccbc
    style C14 fill:#ffccbc
    style C15 fill:#ffccbc
```

---

## 🚀 Workflow de développement recommandé

```mermaid
graph LR
    START([Démarrer projet]) --> N1[NIVEAU 1<br/>CRUD Basique]
    
    N1 --> T1{Tests<br/>passent ?}
    T1 -->|Non| DEBUG1[Debug]
    DEBUG1 --> N1
    T1 -->|Oui| N2[NIVEAU 2<br/>Fonctionnalités]
    
    N2 --> T2{Tests<br/>passent ?}
    T2 -->|Non| DEBUG2[Debug]
    DEBUG2 --> N2
    T2 -->|Oui| CHOICE{Quelle<br/>extension ?}
    
    CHOICE -->|Combat| N3A[NIVEAU 3A<br/>Battle System]
    CHOICE -->|Auth| N3B[NIVEAU 3B<br/>JWT Auth]
    CHOICE -->|Web| N3C[NIVEAU 3C<br/>Jinja2 UI]
    
    N3A --> FINAL[Projet complet]
    N3B --> FINAL
    N3C --> FINAL
    
    FINAL --> DEPLOY[Déploiement]
    
    style START fill:#c8e6c9
    style N1 fill:#c8e6c9
    style N2 fill:#fff59d
    style N3A fill:#ffccbc
    style N3B fill:#ffccbc
    style N3C fill:#bbdefb
    style FINAL fill:#81c784
    style DEPLOY fill:#4caf50
    style DEBUG1 fill:#ffcdd2
    style DEBUG2 fill:#ffcdd2
```

---

## 💡 Bonnes pratiques appliquées

```mermaid
graph TB
    subgraph "✅ Architecture"
        A1["Séparation claire des couches"]
        A2["Responsabilité unique par fichier"]
        A3["@staticmethod pour stateless"]
        A4["Configuration centralisée"]
    end
    
    subgraph "✅ Sécurité"
        S1["Hachage bcrypt pour passwords"]
        S2["JWT avec expiration"]
        S3["Protection endpoints sensibles"]
        S4["Validation Pydantic stricte"]
    end
    
    subgraph "✅ Code Quality"
        Q1["Type hints partout"]
        Q2["Docstrings sur fonctions"]
        Q3["Nommage explicite"]
        Q4["Gestion d'erreurs robuste"]
    end
    
    subgraph "✅ Performance"
        P1["Row factory pour dicts"]
        P2["Requêtes SQL optimisées"]
        P3["Validation exclude_unset"]
        P4["model_validate Pydantic v2"]
    end
    
    subgraph "✅ Maintenabilité"
        M1["Exceptions personnalisées"]
        M2["Handlers centralisés"]
        M3["Config par environnement"]
        M4["Structure modulaire"]
    end
    
    style A1 fill:#e8f5e9
    style A2 fill:#e8f5e9
    style A3 fill:#e8f5e9
    style A4 fill:#e8f5e9
    
    style S1 fill:#fff4e6
    style S2 fill:#fff4e6
    style S3 fill:#fff4e6
    style S4 fill:#fff4e6
    
    style Q1 fill:#e1f5ff
    style Q2 fill:#e1f5ff
    style Q3 fill:#e1f5ff
    style Q4 fill:#e1f5ff
    
    style P1 fill:#f3e5f5
    style P2 fill:#f3e5f5
    style P3 fill:#f3e5f5
    style P4 fill:#f3e5f5
    
    style M1 fill:#fff9c4
    style M2 fill:#fff9c4
    style M3 fill:#fff9c4
    style M4 fill:#fff9c4
```

---

## 🎯 Conclusion

Ce mini-projet synthétise **tous les concepts du workshop FastAPI** :

### 📚 Modules 01-09 appliqués

- **Module 01** : Python foundations (classes, fonctions, types)
- **Module 02** : First API (routes, documentation)
- **Module 03** : Path & Query params (filtres, pagination)
- **Module 04** : Pydantic validation (13 modèles avec validateurs)
- **Module 05** : SQLite database (connexions, requêtes, transactions)
- **Module 06** : Layered architecture (Routes → Services → Repositories)
- **Module 07** : Error handling (4 exceptions + handlers)
- **Module 08** : JWT authentication (register, login, protect)
- **Module 09** : Jinja2 templates (3 pages web + CSS)

### 🎓 Compétences acquises

- ✅ **Architecture professionnelle** en couches
- ✅ **CRUD complet** avec validation
- ✅ **Gestion d'erreurs** robuste
- ✅ **Authentification JWT** sécurisée
- ✅ **Interface web** moderne
- ✅ **Logique métier complexe** (combat, level-up)
- ✅ **Tests** et validation
- ✅ **Documentation** automatique

### 🚀 Prêt pour la production

Le projet intègre les bonnes pratiques pour un déploiement réel :
- Configuration par environnement
- Gestion d'erreurs complète
- Sécurité (JWT, bcrypt)
- Documentation Swagger
- Health check endpoint
- Structure modulaire évolutive

---

**Créé pour le Workshop FastAPI - Module 10 Applied Project**  
*Mini-projet complet synthétisant les modules 01-09* 🎓✨
