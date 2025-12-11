# Architecture API avec Authentification JWT
## Module 08 - Exercise 02

---

## 🏗️ Vue d'ensemble de l'architecture en couches

```mermaid
graph TB
    subgraph "🌐 COUCHE PRÉSENTATION - Routes"
        R1[auth_router<br/>/auth]
        R2[tasks_router<br/>/tasks]
    end
    
    subgraph "🔐 COUCHE SÉCURITÉ - Dependencies"
        D1[get_current_user<br/>Vérifie JWT]
        D2[require_admin<br/>Vérifie rôle admin]
    end
    
    subgraph "💼 COUCHE MÉTIER - Services"
        S1[AuthService<br/>register, login]
        S2[TaskService<br/>CRUD tâches]
    end
    
    subgraph "🗄️ COUCHE DONNÉES - Repositories"
        REP1[UserRepository<br/>create, get_by_username]
        REP2[TaskRepository<br/>create, get_all, get_by_owner, delete]
    end
    
    subgraph "🔧 COUCHE UTILITAIRES"
        U1[auth.py<br/>hash_password, verify_password<br/>create_access_token]
        U2[database.py<br/>get_db_connection<br/>init_database]
    end
    
    subgraph "📦 COUCHE MODÈLES"
        M1[models.py<br/>UserRole, UserRegister<br/>UserLogin, Token<br/>TaskCreate, TaskResponse]
    end
    
    subgraph "💾 BASE DE DONNÉES"
        DB[(SQLite<br/>users table<br/>tasks table)]
    end
    
    R1 --> D1
    R1 --> D2
    R2 --> D1
    R2 --> D2
    
    D1 --> U1
    D2 --> D1
    D2 --> REP1
    
    R1 --> S1
    R2 --> S2
    
    S1 --> REP1
    S1 --> U1
    S2 --> REP2
    
    REP1 --> U2
    REP2 --> U2
    
    U2 --> DB
    
    R1 -.utilise.-> M1
    R2 -.utilise.-> M1
    S1 -.utilise.-> M1
    S2 -.utilise.-> M1
    
    style R1 fill:#e1f5ff
    style R2 fill:#e1f5ff
    style D1 fill:#fff4e6
    style D2 fill:#fff4e6
    style S1 fill:#e8f5e9
    style S2 fill:#e8f5e9
    style REP1 fill:#f3e5f5
    style REP2 fill:#f3e5f5
    style U1 fill:#fce4ec
    style U2 fill:#fce4ec
    style M1 fill:#fff9c4
    style DB fill:#ffebee
```

---

## 🔄 Flux d'authentification détaillé

```mermaid
sequenceDiagram
    participant Client
    participant Routes as routes.py<br/>(auth_router)
    participant Service as services.py<br/>(AuthService)
    participant Repo as repositories.py<br/>(UserRepository)
    participant Auth as auth.py<br/>(Utilitaires)
    participant DB as SQLite DB

    rect rgb(230, 240, 255)
        Note over Client,DB: 📝 INSCRIPTION (POST /auth/register)
        Client->>Routes: POST /auth/register<br/>{username, password, role}
        Routes->>Service: register(UserRegister)
        Service->>Repo: get_by_username(username)
        Repo->>DB: SELECT * FROM users WHERE username = ?
        DB-->>Repo: None (utilisateur inexistant)
        Repo-->>Service: None
        Service->>Auth: hash_password(password)
        Auth-->>Service: hashed_password
        Service->>Repo: create(username, hashed_password, role)
        Repo->>DB: INSERT INTO users (...)
        DB-->>Repo: user_id
        Repo-->>Service: user_id
        Service-->>Routes: {"message": "Utilisateur créé"}
        Routes-->>Client: 200 OK
    end

    rect rgb(240, 255, 240)
        Note over Client,DB: 🔐 CONNEXION (POST /auth/login)
        Client->>Routes: POST /auth/login<br/>{username, password}
        Routes->>Service: login(UserLogin)
        Service->>Repo: get_by_username(username)
        Repo->>DB: SELECT * FROM users WHERE username = ?
        DB-->>Repo: user_data
        Repo-->>Service: {id, username, hashed_password, role}
        Service->>Auth: verify_password(password, hashed_password)
        Auth-->>Service: True
        Service->>Auth: create_access_token({"sub": username})
        Auth-->>Service: JWT token
        Service-->>Routes: Token(access_token, token_type)
        Routes-->>Client: {"access_token": "...", "token_type": "bearer"}
    end
```

---

## 🛡️ Flux d'autorisation avec JWT

```mermaid
sequenceDiagram
    participant Client
    participant Routes as routes.py<br/>(tasks_router)
    participant Deps as dependencies.py
    participant Auth as auth.py
    participant Service as services.py<br/>(TaskService)
    participant Repo as repositories.py<br/>(TaskRepository)
    participant DB as SQLite DB

    rect rgb(255, 245, 230)
        Note over Client,DB: ✅ REQUÊTE UTILISATEUR (GET /tasks/my-tasks)
        Client->>Routes: GET /tasks/my-tasks<br/>Header: Authorization: Bearer xxx
        Routes->>Deps: get_current_user(authorization)
        Deps->>Deps: Extraire token du header
        Deps->>Auth: jwt.decode(token, SECRET_KEY)
        Auth-->>Deps: payload {"sub": "alice"}
        Deps-->>Routes: username = "alice"
        Routes->>Service: get_my_tasks("alice")
        Service->>Repo: get_by_owner("alice")
        Repo->>DB: SELECT * FROM tasks WHERE owner = ?
        DB-->>Repo: [task1, task2]
        Repo-->>Service: [task1, task2]
        Service-->>Routes: [TaskResponse, TaskResponse]
        Routes-->>Client: 200 OK + tasks
    end

    rect rgb(255, 230, 230)
        Note over Client,DB: 🚫 REQUÊTE ADMIN (GET /tasks/all)
        Client->>Routes: GET /tasks/all<br/>Header: Authorization: Bearer xxx
        Routes->>Deps: require_admin(authorization)
        Deps->>Deps: get_current_user() ✅
        Deps-->>Deps: username = "alice"
        Deps->>Repo: get_by_username("alice")
        Repo->>DB: SELECT * FROM users WHERE username = ?
        DB-->>Repo: {role: "user"}
        Repo-->>Deps: {role: "user"}
        Deps->>Deps: Vérifier role == "admin" ❌
        Deps-->>Routes: HTTPException(403, "Accès réservé aux administrateurs")
        Routes-->>Client: 403 FORBIDDEN
    end
```

---

## 📊 Relations entre classes et méthodes

```mermaid
classDiagram
    class main {
        +FastAPI app
        +init_database()
        +include_router(auth_router)
        +include_router(tasks_router)
        +root() dict
    }
    
    class routes {
        <<APIRouter>>
        +auth_router /auth
        +tasks_router /tasks
        --AUTH--
        +register(UserRegister) dict
        +login(UserLogin) Token
        --TASKS USER--
        +create_task(TaskCreate, user) TaskResponse
        +get_my_tasks(user) list~TaskResponse~
        --TASKS ADMIN--
        +get_all_tasks(admin) list~TaskResponse~
        +delete_task(task_id, admin) dict
    }
    
    class dependencies {
        <<Security>>
        +get_current_user(authorization) str
        +require_admin(current_user) str
    }
    
    class AuthService {
        <<Service>>
        +register(UserRegister) dict
        +login(UserLogin) Token
    }
    
    class TaskService {
        <<Service>>
        +create_task(TaskCreate, owner) TaskResponse
        +get_my_tasks(username) list~TaskResponse~
        +get_all_tasks() list~TaskResponse~
        +delete_task(task_id) dict
    }
    
    class UserRepository {
        <<Repository>>
        +create(username, hashed_pwd, role) int
        +get_by_username(username) dict
    }
    
    class TaskRepository {
        <<Repository>>
        +create(title, desc, owner) int
        +get_all() list~dict~
        +get_by_owner(owner) list~dict~
        +delete(task_id) bool
    }
    
    class auth {
        <<Utilities>>
        +SECRET_KEY str
        +ALGORITHM str
        +pwd_context CryptContext
        +hash_password(password) str
        +verify_password(plain, hashed) bool
        +create_access_token(data) str
    }
    
    class database {
        <<Utilities>>
        +DATABASE_PATH str
        +get_db_connection() Connection
        +init_database() None
    }
    
    class models {
        <<Pydantic Models>>
        +UserRole Enum
        +UserRegister BaseModel
        +UserLogin BaseModel
        +Token BaseModel
        +TaskCreate BaseModel
        +TaskResponse BaseModel
    }
    
    main --> routes
    routes --> dependencies : Depends()
    routes --> AuthService
    routes --> TaskService
    routes ..> models : uses
    
    dependencies --> auth : jwt.decode()
    dependencies --> UserRepository
    
    AuthService --> UserRepository
    AuthService --> auth
    AuthService ..> models : uses
    
    TaskService --> TaskRepository
    TaskService ..> models : uses
    
    UserRepository --> database
    TaskRepository --> database
    
    database --> SQLite : conn.execute()
```

---

## 🎯 Matrice des responsabilités

```mermaid
graph LR
    subgraph "📄 Fichier: main.py"
        M1[Initialisation app]
        M2[Configuration routers]
        M3[Route racine /]
    end
    
    subgraph "📄 Fichier: routes.py"
        RT1[Définir endpoints HTTP]
        RT2[Appliquer dépendances]
        RT3[Appeler services]
        RT4[Retourner réponses]
    end
    
    subgraph "📄 Fichier: dependencies.py"
        DP1[Vérifier JWT token]
        DP2[Extraire username]
        DP3[Vérifier rôle admin]
        DP4[Lever exceptions 401/403]
    end
    
    subgraph "📄 Fichier: services.py"
        SV1[Logique métier]
        SV2[Validation données]
        SV3[Orchestration repos]
        SV4[Transformation modèles]
    end
    
    subgraph "📄 Fichier: repositories.py"
        RP1[Requêtes SQL]
        RP2[CRUD base de données]
        RP3[Conversion Row → dict]
    end
    
    subgraph "📄 Fichier: auth.py"
        AU1[Hachage mots de passe]
        AU2[Vérification mots de passe]
        AU3[Génération JWT]
        AU4[Gestion expiration]
    end
    
    subgraph "📄 Fichier: database.py"
        DB1[Connexion SQLite]
        DB2[Initialisation tables]
        DB3[Row factory]
    end
    
    subgraph "📄 Fichier: models.py"
        MD1[Validation Pydantic]
        MD2[Schémas requête/réponse]
        MD3[Énumérations]
        MD4[Documentation API]
    end
    
    style M1 fill:#e3f2fd
    style M2 fill:#e3f2fd
    style M3 fill:#e3f2fd
    style RT1 fill:#e1f5ff
    style RT2 fill:#e1f5ff
    style RT3 fill:#e1f5ff
    style RT4 fill:#e1f5ff
    style DP1 fill:#fff4e6
    style DP2 fill:#fff4e6
    style DP3 fill:#fff4e6
    style DP4 fill:#fff4e6
    style SV1 fill:#e8f5e9
    style SV2 fill:#e8f5e9
    style SV3 fill:#e8f5e9
    style SV4 fill:#e8f5e9
    style RP1 fill:#f3e5f5
    style RP2 fill:#f3e5f5
    style RP3 fill:#f3e5f5
    style AU1 fill:#fce4ec
    style AU2 fill:#fce4ec
    style AU3 fill:#fce4ec
    style AU4 fill:#fce4ec
    style DB1 fill:#fff3e0
    style DB2 fill:#fff3e0
    style DB3 fill:#fff3e0
    style MD1 fill:#fff9c4
    style MD2 fill:#fff9c4
    style MD3 fill:#fff9c4
    style MD4 fill:#fff9c4
```

---

## 🔐 Architecture de sécurité - Flux complet

```mermaid
flowchart TD
    START([Client envoie requête]) --> HAS_AUTH{Endpoint<br/>protégé ?}
    
    HAS_AUTH -->|Non| ROUTE[Exécuter route]
    HAS_AUTH -->|Oui| CHECK_HEADER{Header<br/>Authorization<br/>présent ?}
    
    CHECK_HEADER -->|Non| ERR_401_1[❌ 401 Token manquant]
    CHECK_HEADER -->|Oui| PARSE_HEADER[Extraire Bearer token]
    
    PARSE_HEADER --> VALID_FORMAT{Format<br/>Bearer xxx<br/>valide ?}
    VALID_FORMAT -->|Non| ERR_401_2[❌ 401 Format invalide]
    VALID_FORMAT -->|Oui| DECODE_JWT[Décoder JWT]
    
    DECODE_JWT --> JWT_VALID{JWT<br/>valide ?}
    JWT_VALID -->|Non| ERR_401_3[❌ 401 Token invalide/expiré]
    JWT_VALID -->|Oui| EXTRACT_USER[Extraire username du payload]
    
    EXTRACT_USER --> HAS_USERNAME{Username<br/>présent ?}
    HAS_USERNAME -->|Non| ERR_401_4[❌ 401 Token invalide]
    HAS_USERNAME -->|Oui| CHECK_ADMIN{Endpoint<br/>admin only ?}
    
    CHECK_ADMIN -->|Non| ROUTE
    CHECK_ADMIN -->|Oui| GET_USER[Récupérer user de la DB]
    
    GET_USER --> USER_EXISTS{User<br/>existe ?}
    USER_EXISTS -->|Non| ERR_401_5[❌ 401 Utilisateur non trouvé]
    USER_EXISTS -->|Oui| CHECK_ROLE{role ==<br/>'admin' ?}
    
    CHECK_ROLE -->|Non| ERR_403[❌ 403 Accès réservé aux admins]
    CHECK_ROLE -->|Oui| ROUTE
    
    ROUTE --> SUCCESS([✅ Réponse 200/201])
    
    ERR_401_1 --> END([Erreur retournée])
    ERR_401_2 --> END
    ERR_401_3 --> END
    ERR_401_4 --> END
    ERR_401_5 --> END
    ERR_403 --> END
    SUCCESS --> END
    
    style START fill:#c8e6c9
    style SUCCESS fill:#c8e6c9
    style ERR_401_1 fill:#ffcdd2
    style ERR_401_2 fill:#ffcdd2
    style ERR_401_3 fill:#ffcdd2
    style ERR_401_4 fill:#ffcdd2
    style ERR_401_5 fill:#ffcdd2
    style ERR_403 fill:#ff8a80
    style ROUTE fill:#bbdefb
```

---

## 📋 Tableau récapitulatif des endpoints

| Endpoint | Méthode | Authentification | Autorisation | Service | Repository |
|----------|---------|------------------|--------------|---------|------------|
| `/` | GET | ❌ Non | - | - | - |
| `/auth/register` | POST | ❌ Non | - | `AuthService.register()` | `UserRepository.create()` |
| `/auth/login` | POST | ❌ Non | - | `AuthService.login()` | `UserRepository.get_by_username()` |
| `/tasks` | POST | ✅ JWT | User/Admin | `TaskService.create_task()` | `TaskRepository.create()` |
| `/tasks/my-tasks` | GET | ✅ JWT | User/Admin | `TaskService.get_my_tasks()` | `TaskRepository.get_by_owner()` |
| `/tasks/all` | GET | ✅ JWT | **Admin only** | `TaskService.get_all_tasks()` | `TaskRepository.get_all()` |
| `/tasks/{id}` | DELETE | ✅ JWT | **Admin only** | `TaskService.delete_task()` | `TaskRepository.delete()` |

---

## 🎓 Principes architecturaux appliqués

```mermaid
mindmap
  root((Architecture<br/>Layered))
    Séparation des responsabilités
      Routes → HTTP
      Services → Logique métier
      Repositories → Données
      Dependencies → Sécurité
    Réutilisabilité
      @staticmethod partout
      Pas d'état
      Fonctions pures
    Sécurité
      JWT pour auth
      Hachage bcrypt
      Vérification rôles
      Middleware d'auth
    Maintenabilité
      Couches indépendantes
      Tests unitaires faciles
      Documentation claire
    Scalabilité
      Ajout endpoints simple
      Nouveaux rôles facile
      Migration DB simple
```

---

## 🔑 Légende des symboles

| Symbole | Signification |
|---------|---------------|
| 🌐 | Couche Présentation (Routes) |
| 🔐 | Couche Sécurité (Dependencies) |
| 💼 | Couche Métier (Services) |
| 🗄️ | Couche Données (Repositories) |
| 🔧 | Utilitaires (Auth, Database) |
| 📦 | Modèles Pydantic |
| 💾 | Base de données SQLite |
| ✅ | Succès / Autorisé |
| ❌ | Erreur / Refusé |
| 🔒 | Endpoint protégé |
| 👤 | Utilisateur normal |
| 👑 | Administrateur |

---

## 📝 Notes importantes

1. **Dépendances FastAPI** : `Depends(get_current_user)` injecte automatiquement le username
2. **Chaînage de dépendances** : `require_admin` appelle `get_current_user` en interne
3. **Stateless** : Aucun état stocké entre les requêtes, JWT contient toutes les infos
4. **Modularité** : Chaque couche peut être testée indépendamment
5. **Extensibilité** : Ajouter un nouveau rôle = modifier `UserRole` enum + ajouter une dependency

---

**Créé pour le Workshop FastAPI - Module 08 Authentication**  
*Architecture professionnelle avec JWT, rôles et permissions* 🚀
