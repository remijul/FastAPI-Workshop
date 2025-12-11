# Architecture API Blog avec Authentification JWT
## Module 08 - Exercise 01 Solution

---

## 🏗️ Vue d'ensemble de l'architecture en couches

```mermaid
graph TB
    subgraph "🌐 COUCHE PRÉSENTATION - Routes"
        R1[auth_router<br/>/auth]
        R2[articles_router<br/>/articles]
    end
    
    subgraph "🔐 COUCHE SÉCURITÉ - Dependencies"
        D1[get_current_user<br/>Vérifie JWT]
    end
    
    subgraph "💼 COUCHE MÉTIER - Services"
        S1[AuthService<br/>register, login]
        S2[ArticleService<br/>CRUD articles]
    end
    
    subgraph "🗄️ COUCHE DONNÉES - Repositories"
        REP1[UserRepository<br/>create, get_by_username]
        REP2[ArticleRepository<br/>create, get_all, get_by_author]
    end
    
    subgraph "🔧 COUCHE UTILITAIRES"
        U1[auth.py<br/>hash_password, verify_password<br/>create_access_token]
        U2[database.py<br/>get_db_connection<br/>init_database]
    end
    
    subgraph "📦 COUCHE MODÈLES"
        M1[models.py<br/>UserRegister, UserLogin<br/>Token, ArticleCreate<br/>ArticleResponse]
    end
    
    subgraph "💾 BASE DE DONNÉES"
        DB[(SQLite<br/>users table<br/>articles table)]
    end
    
    R1 --> D1
    R2 --> D1
    
    D1 --> U1
    
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
        Client->>Routes: POST /auth/register<br/>{username, password}
        Routes->>Service: register(UserRegister)
        Service->>Repo: get_by_username(username)
        Repo->>DB: SELECT * FROM users WHERE username = ?
        DB-->>Repo: None (utilisateur inexistant)
        Repo-->>Service: None
        Service->>Auth: hash_password(password)
        Auth-->>Service: hashed_password
        Service->>Repo: create(username, hashed_password)
        Repo->>DB: INSERT INTO users (username, hashed_password)
        DB-->>Repo: user_id
        Repo-->>Service: user_id
        Service-->>Routes: {"message": "Utilisateur créé avec succès"}
        Routes-->>Client: 200 OK
    end

    rect rgb(240, 255, 240)
        Note over Client,DB: 🔐 CONNEXION (POST /auth/login)
        Client->>Routes: POST /auth/login<br/>{username, password}
        Routes->>Service: login(UserLogin)
        Service->>Repo: get_by_username(username)
        Repo->>DB: SELECT * FROM users WHERE username = ?
        DB-->>Repo: user_data
        Repo-->>Service: {id, username, hashed_password}
        Service->>Auth: verify_password(password, hashed_password)
        Auth-->>Service: True
        Service->>Auth: create_access_token({"sub": username})
        Auth-->>Service: JWT token
        Service-->>Routes: Token(access_token, token_type)
        Routes-->>Client: {"access_token": "eyJ...", "token_type": "bearer"}
    end
```

---

## 📝 Flux de gestion des articles

```mermaid
sequenceDiagram
    participant Client
    participant Routes as routes.py<br/>(articles_router)
    participant Deps as dependencies.py<br/>(get_current_user)
    participant Auth as auth.py
    participant Service as services.py<br/>(ArticleService)
    participant Repo as repositories.py<br/>(ArticleRepository)
    participant DB as SQLite DB

    rect rgb(255, 250, 240)
        Note over Client,DB: 📖 LISTER ARTICLES - Public (GET /articles)
        Client->>Routes: GET /articles
        Routes->>Service: get_all_articles()
        Service->>Repo: get_all()
        Repo->>DB: SELECT * FROM articles
        DB-->>Repo: [article1, article2, article3]
        Repo-->>Service: [dict1, dict2, dict3]
        Service-->>Routes: [ArticleResponse, ArticleResponse, ArticleResponse]
        Routes-->>Client: 200 OK + articles
    end

    rect rgb(240, 255, 240)
        Note over Client,DB: ✍️ CRÉER ARTICLE - Protégé (POST /articles)
        Client->>Routes: POST /articles<br/>Header: Authorization: Bearer xxx<br/>{title, content}
        Routes->>Deps: get_current_user(authorization)
        Deps->>Deps: Extraire token du header
        Deps->>Auth: jwt.decode(token, SECRET_KEY)
        Auth-->>Deps: payload {"sub": "alice"}
        Deps-->>Routes: username = "alice"
        Routes->>Service: create_article(ArticleCreate, "alice")
        Service->>Repo: create(title, content, "alice")
        Repo->>DB: INSERT INTO articles (title, content, author)
        DB-->>Repo: article_id = 1
        Repo-->>Service: 1
        Service-->>Routes: ArticleResponse(id=1, title, content, author="alice")
        Routes-->>Client: 201 Created + article
    end

    rect rgb(255, 240, 245)
        Note over Client,DB: 📚 MES ARTICLES - Protégé (GET /articles/my-articles)
        Client->>Routes: GET /articles/my-articles<br/>Header: Authorization: Bearer xxx
        Routes->>Deps: get_current_user(authorization)
        Deps->>Auth: jwt.decode(token, SECRET_KEY)
        Auth-->>Deps: payload {"sub": "bob"}
        Deps-->>Routes: username = "bob"
        Routes->>Service: get_my_articles("bob")
        Service->>Repo: get_by_author("bob")
        Repo->>DB: SELECT * FROM articles WHERE author = ?
        DB-->>Repo: [article1, article2]
        Repo-->>Service: [dict1, dict2]
        Service-->>Routes: [ArticleResponse, ArticleResponse]
        Routes-->>Client: 200 OK + articles de Bob
    end
```

---

## 🛡️ Architecture de sécurité - Vérification JWT

```mermaid
flowchart TD
    START([Client envoie requête]) --> IS_PUBLIC{Endpoint<br/>public ?}
    
    IS_PUBLIC -->|GET /articles| PUBLIC[✅ Exécuter sans auth]
    IS_PUBLIC -->|POST /articles<br/>GET /my-articles| CHECK_HEADER{Header<br/>Authorization<br/>présent ?}
    
    CHECK_HEADER -->|Non| ERR_401_1[❌ 401 Token manquant]
    CHECK_HEADER -->|Oui| PARSE[Extraire token<br/>du header]
    
    PARSE --> VALID_FORMAT{Format<br/>'Bearer xxx'<br/>valide ?}
    
    VALID_FORMAT -->|Non| ERR_401_2[❌ 401 Format invalide]
    VALID_FORMAT -->|Oui| SPLIT[Séparer scheme et token]
    
    SPLIT --> CHECK_SCHEME{scheme ==<br/>'bearer' ?}
    CHECK_SCHEME -->|Non| ERR_401_3[❌ 401 Type d'auth invalide]
    CHECK_SCHEME -->|Oui| DECODE[Décoder JWT]
    
    DECODE --> JWT_VALID{JWT<br/>valide ?}
    JWT_VALID -->|Non| ERR_401_4[❌ 401 Token invalide/expiré]
    JWT_VALID -->|Oui| EXTRACT[Extraire username<br/>du payload sub]
    
    EXTRACT --> HAS_SUB{Username<br/>présent ?}
    HAS_SUB -->|Non| ERR_401_5[❌ 401 Token invalide]
    HAS_SUB -->|Oui| ROUTE[✅ Exécuter route<br/>avec username]
    
    PUBLIC --> SUCCESS([✅ Réponse 200/201])
    ROUTE --> SUCCESS
    
    ERR_401_1 --> END([Erreur retournée])
    ERR_401_2 --> END
    ERR_401_3 --> END
    ERR_401_4 --> END
    ERR_401_5 --> END
    SUCCESS --> END
    
    style START fill:#c8e6c9
    style SUCCESS fill:#c8e6c9
    style PUBLIC fill:#bbdefb
    style ROUTE fill:#bbdefb
    style ERR_401_1 fill:#ffcdd2
    style ERR_401_2 fill:#ffcdd2
    style ERR_401_3 fill:#ffcdd2
    style ERR_401_4 fill:#ffcdd2
    style ERR_401_5 fill:#ffcdd2
```

---

## 📊 Relations entre classes et méthodes

```mermaid
classDiagram
    class main {
        +FastAPI app
        +init_database()
        +include_router(auth_router)
        +include_router(articles_router)
        +root() dict
    }
    
    class routes {
        <<APIRouter>>
        +auth_router /auth
        +articles_router /articles
        --AUTH--
        +register(UserRegister) dict
        +login(UserLogin) Token
        --ARTICLES--
        +get_all_articles() list~ArticleResponse~
        +create_article(ArticleCreate, user) ArticleResponse
        +get_my_articles(user) list~ArticleResponse~
    }
    
    class dependencies {
        <<Security>>
        +get_current_user(authorization) str
    }
    
    class AuthService {
        <<Service>>
        +register(UserRegister) dict
        +login(UserLogin) Token
    }
    
    class ArticleService {
        <<Service>>
        +create_article(ArticleCreate, author) ArticleResponse
        +get_all_articles() list~ArticleResponse~
        +get_my_articles(username) list~ArticleResponse~
    }
    
    class UserRepository {
        <<Repository>>
        +create(username, hashed_password) int
        +get_by_username(username) dict | None
    }
    
    class ArticleRepository {
        <<Repository>>
        +create(title, content, author) int
        +get_all() list~dict~
        +get_by_author(author) list~dict~
    }
    
    class auth {
        <<Utilities>>
        +SECRET_KEY str
        +ALGORITHM str
        +ACCESS_TOKEN_EXPIRE_MINUTES int
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
        +UserRegister BaseModel
        +UserLogin BaseModel
        +Token BaseModel
        +ArticleCreate BaseModel
        +ArticleResponse BaseModel
    }
    
    main --> routes
    routes --> dependencies : Depends()
    routes --> AuthService
    routes --> ArticleService
    routes ..> models : uses
    
    dependencies --> auth : jwt.decode()
    
    AuthService --> UserRepository
    AuthService --> auth
    AuthService ..> models : uses
    
    ArticleService --> ArticleRepository
    ArticleService ..> models : uses
    
    UserRepository --> database
    ArticleRepository --> database
    
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
        M4[init_database]
    end
    
    subgraph "📄 Fichier: routes.py"
        RT1[Définir endpoints HTTP]
        RT2[Appliquer dépendance JWT]
        RT3[Appeler services]
        RT4[Retourner réponses]
    end
    
    subgraph "📄 Fichier: dependencies.py"
        DP1[Vérifier header Authorization]
        DP2[Extraire Bearer token]
        DP3[Décoder JWT]
        DP4[Extraire username payload]
        DP5[Lever exceptions 401]
    end
    
    subgraph "📄 Fichier: services.py"
        SV1[Validation métier]
        SV2[Orchestration repos]
        SV3[Transformation modèles]
        SV4[Gestion erreurs HTTP]
    end
    
    subgraph "📄 Fichier: repositories.py"
        RP1[Requêtes SQL INSERT]
        RP2[Requêtes SQL SELECT]
        RP3[Conversion Row → dict]
        RP4[Gestion connexions DB]
    end
    
    subgraph "📄 Fichier: auth.py"
        AU1[Hachage bcrypt]
        AU2[Vérification bcrypt]
        AU3[Génération JWT]
        AU4[Expiration tokens]
    end
    
    subgraph "📄 Fichier: database.py"
        DB1[Connexion SQLite]
        DB2[Row factory]
        DB3[Création tables users]
        DB4[Création tables articles]
    end
    
    subgraph "📄 Fichier: models.py"
        MD1[Validation Pydantic]
        MD2[Schémas requête]
        MD3[Schémas réponse]
        MD4[Contraintes données]
    end
    
    style M1 fill:#e3f2fd
    style M2 fill:#e3f2fd
    style M3 fill:#e3f2fd
    style M4 fill:#e3f2fd
    style RT1 fill:#e1f5ff
    style RT2 fill:#e1f5ff
    style RT3 fill:#e1f5ff
    style RT4 fill:#e1f5ff
    style DP1 fill:#fff4e6
    style DP2 fill:#fff4e6
    style DP3 fill:#fff4e6
    style DP4 fill:#fff4e6
    style DP5 fill:#fff4e6
    style SV1 fill:#e8f5e9
    style SV2 fill:#e8f5e9
    style SV3 fill:#e8f5e9
    style SV4 fill:#e8f5e9
    style RP1 fill:#f3e5f5
    style RP2 fill:#f3e5f5
    style RP3 fill:#f3e5f5
    style RP4 fill:#f3e5f5
    style AU1 fill:#fce4ec
    style AU2 fill:#fce4ec
    style AU3 fill:#fce4ec
    style AU4 fill:#fce4ec
    style DB1 fill:#fff3e0
    style DB2 fill:#fff3e0
    style DB3 fill:#fff3e0
    style DB4 fill:#fff3e0
    style MD1 fill:#fff9c4
    style MD2 fill:#fff9c4
    style MD3 fill:#fff9c4
    style MD4 fill:#fff9c4
```

---

## 🔐 Flux complet : Créer un article (authentifié)

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant FastAPI
    participant get_current_user as dependencies.py<br/>get_current_user()
    participant jwt as auth.py<br/>jwt.decode()
    participant ArticleService as services.py<br/>ArticleService
    participant ArticleRepo as repositories.py<br/>ArticleRepository
    participant DB as SQLite

    Client->>FastAPI: POST /articles<br/>Authorization: Bearer eyJ...<br/>{title, content}
    
    Note over FastAPI: Endpoint protégé<br/>Depends(get_current_user)
    
    FastAPI->>get_current_user: Appel automatique
    
    alt Header manquant
        get_current_user-->>FastAPI: HTTPException(401, "Token manquant")
        FastAPI-->>Client: 401 Unauthorized
    else Header présent
        get_current_user->>get_current_user: authorization.split()
        
        alt Format invalide
            get_current_user-->>FastAPI: HTTPException(401, "Format invalide")
            FastAPI-->>Client: 401 Unauthorized
        else Format valide
            get_current_user->>jwt: decode(token, SECRET_KEY)
            
            alt Token invalide/expiré
                jwt-->>get_current_user: JWTError
                get_current_user-->>FastAPI: HTTPException(401, "Token invalide")
                FastAPI-->>Client: 401 Unauthorized
            else Token valide
                jwt-->>get_current_user: payload {"sub": "alice"}
                get_current_user->>get_current_user: username = payload.get("sub")
                get_current_user-->>FastAPI: "alice"
                
                FastAPI->>ArticleService: create_article(ArticleCreate, "alice")
                ArticleService->>ArticleRepo: create(title, content, "alice")
                ArticleRepo->>DB: INSERT INTO articles (...)
                DB-->>ArticleRepo: article_id = 5
                ArticleRepo-->>ArticleService: 5
                ArticleService->>ArticleService: Créer ArticleResponse
                ArticleService-->>FastAPI: ArticleResponse(id=5, ...)
                FastAPI-->>Client: 201 Created + article
            end
        end
    end
```

---

## 📋 Tableau récapitulatif des endpoints

| Endpoint | Méthode | Authentification | Service | Repository | Description |
|----------|---------|------------------|---------|------------|-------------|
| `/` | GET | ❌ Non | - | - | Documentation API |
| `/auth/register` | POST | ❌ Non | `AuthService.register()` | `UserRepository.create()` | Créer un compte |
| `/auth/login` | POST | ❌ Non | `AuthService.login()` | `UserRepository.get_by_username()` | Obtenir un token JWT |
| `/articles` | GET | ❌ Non | `ArticleService.get_all_articles()` | `ArticleRepository.get_all()` | Lister tous les articles |
| `/articles` | POST | ✅ JWT | `ArticleService.create_article()` | `ArticleRepository.create()` | Créer un article |
| `/articles/my-articles` | GET | ✅ JWT | `ArticleService.get_my_articles()` | `ArticleRepository.get_by_author()` | Mes articles |

---

## 📝 Structure de la base de données

```mermaid
erDiagram
    USERS ||--o{ ARTICLES : "écrit"
    
    USERS {
        int id PK
        text username UK
        text hashed_password
    }
    
    ARTICLES {
        int id PK
        text title
        text content
        text author FK
    }
```

---

## 🛠️ Flux de hachage et vérification des mots de passe

```mermaid
flowchart LR
    subgraph "INSCRIPTION"
        PWD1[Password:<br/>'monmotdepasse']
        HASH[hash_password]
        BCRYPT1[bcrypt.hash]
        HASHED1[Hashed:<br/>'$2b$12$abc...']
        DB1[(Database<br/>users)]
        
        PWD1 --> HASH
        HASH --> BCRYPT1
        BCRYPT1 --> HASHED1
        HASHED1 --> DB1
    end
    
    subgraph "CONNEXION"
        PWD2[Password:<br/>'monmotdepasse']
        DB2[(Database<br/>users)]
        STORED[Hashed:<br/>'$2b$12$abc...']
        VERIFY[verify_password]
        BCRYPT2[bcrypt.verify]
        RESULT{Match ?}
        
        PWD2 --> VERIFY
        DB2 --> STORED
        STORED --> VERIFY
        VERIFY --> BCRYPT2
        BCRYPT2 --> RESULT
        RESULT -->|True| SUCCESS[✅ Créer JWT]
        RESULT -->|False| ERROR[❌ 401 Identifiants<br/>incorrects]
    end
    
    style PWD1 fill:#fff9c4
    style HASHED1 fill:#f3e5f5
    style DB1 fill:#ffebee
    style PWD2 fill:#fff9c4
    style STORED fill:#f3e5f5
    style DB2 fill:#ffebee
    style SUCCESS fill:#c8e6c9
    style ERROR fill:#ffcdd2
```

---

## 🎯 Points d'apprentissage clés

```mermaid
graph TD
    A[Exercise 01:<br/>API Blog avec JWT] --> B[Concepts de base]
    
    B --> C[1. Authentification JWT]
    C --> C1[Hachage bcrypt]
    C --> C2[Génération token]
    C --> C3[Vérification token]
    
    B --> D[2. Architecture en couches]
    D --> D1[Routes HTTP]
    D --> D2[Services métier]
    D --> D3[Repositories données]
    
    B --> E[3. Dépendances FastAPI]
    E --> E1[Depends]
    E --> E2[Header injection]
    E --> E3[Automatic auth]
    
    B --> F[4. Protection endpoints]
    F --> F1[Public routes]
    F --> F2[Protected routes]
    F --> F3[User context]
    
    style A fill:#4fc3f7
    style B fill:#81c784
    style C fill:#ffb74d
    style D fill:#ba68c8
    style E fill:#4db6ac
    style F fill:#ff8a65
```

---

## 🔐 Anatomie d'un JWT Token

```mermaid
graph LR
    subgraph "JWT Structure"
        HEADER[HEADER<br/>eyJhbGc...]
        DOT1[.]
        PAYLOAD[PAYLOAD<br/>eyJzdWI...]
        DOT2[.]
        SIGNATURE[SIGNATURE<br/>SflKxw...]
    end
    
    subgraph "Header Décodé"
        H1["{ 'alg': 'HS256',<br/>'typ': 'JWT' }"]
    end
    
    subgraph "Payload Décodé"
        P1["{ 'sub': 'alice',<br/>'exp': 1735742400 }"]
    end
    
    subgraph "Signature Process"
        S1[HMAC-SHA256]
        S2[SECRET_KEY]
    end
    
    HEADER --- DOT1
    DOT1 --- PAYLOAD
    PAYLOAD --- DOT2
    DOT2 --- SIGNATURE
    
    HEADER -.decode.-> H1
    PAYLOAD -.decode.-> P1
    SIGNATURE -.verify.-> S1
    S2 -.used by.-> S1
    
    style HEADER fill:#e1f5ff
    style PAYLOAD fill:#fff9c4
    style SIGNATURE fill:#f3e5f5
    style H1 fill:#bbdefb
    style P1 fill:#fff59d
    style S1 fill:#ce93d8
    style S2 fill:#ffcdd2
```

---

## 📚 Ressources et bonnes pratiques

### ✅ Bonnes pratiques implémentées

1. **Sécurité**
   - Hachage bcrypt pour les mots de passe
   - JWT avec expiration (30 minutes)
   - SECRET_KEY à changer en production
   - Validation des headers Authorization

2. **Architecture**
   - Séparation claire des couches
   - @staticmethod pour services/repos stateless
   - Modèles Pydantic pour validation
   - Gestion d'erreurs centralisée

3. **Code propre**
   - Type hints partout
   - Docstrings sur fonctions importantes
   - Nommage explicite
   - Pas de code dupliqué

### ⚠️ Améliorations possibles (Exercise 02)

1. Ajouter des rôles utilisateur (admin, user)
2. Implémenter une dépendance require_admin
3. Ajouter refresh tokens
4. Logger les tentatives de connexion
5. Rate limiting sur les endpoints sensibles

---

## 🎯 Conclusion

**Exercise 01** est une introduction complète à :
- L'authentification JWT avec FastAPI
- L'architecture en couches professionnelle
- La protection d'endpoints via dépendances
- La gestion sécurisée des mots de passe

**Prérequis pour Exercise 02** : Maîtriser ces concepts avant d'ajouter les rôles et permissions ! 🚀

---

**Créé pour le Workshop FastAPI - Module 08 Authentication**  
*Exercice 01 : Fondations de l'authentification JWT* 🔐
