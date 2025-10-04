# WasteNot - System Architecture & User Flows

## High-Level System Architecture

```mermaid
graph LR
    subgraph "Client Side"
        Frontend[Web Frontend<br/>HTML5/CSS3/JavaScript<br/>Tailwind CSS<br/>GSAP Animations<br/>Swiper.js<br/>MapBox GL JS]
    end
    
    subgraph "Server Side"
        Backend[Django Application<br/>Views & URL Routing<br/>Models & Forms<br/>REST Framework<br/>Admin Interface]
        Auth[Authentication<br/>Django Auth System<br/>Session Management<br/>CSRF Protection]
    end
    
    subgraph "Data Layer"
        Database[(MySQL Database<br/>Users, Items<br/>Categories, Messages<br/>Exchange Schedules)]
        Storage[File Storage<br/>Item Images<br/>QR Code Images<br/>Message Attachments]
    end
    
    subgraph "External Services"
        APIs[Third-party APIs<br/>Google Cloud Vision<br/>MapBox Location<br/>Email Service<br/>QR Code Generator]
    end

    Frontend --> Backend
    Backend --> Auth
    Backend --> Database
    Backend --> Storage
    Backend --> APIs
    Frontend -.-> APIs

    %% Styling
    classDef client fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef server fill:#f1f8e9,stroke:#388e3c,stroke-width:2px
    classDef data fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef external fill:#fff3e0,stroke:#f57c00,stroke-width:2px

    class Frontend client
    class Backend,Auth server
    class Database,Storage data
    class APIs external
```

## Data Model Architecture

```mermaid
erDiagram
    User ||--o{ Item : "donates"
    User ||--o{ Item : "receives"
    User ||--o{ ExchangeSchedule : "donor"
    User ||--o{ ExchangeSchedule : "recipient"
    User ||--o{ Message : "sends"
    User ||--o{ Message : "receives"
    
    Category ||--o{ Item : "categorizes"
    
    Item ||--o{ ItemImage : "has"
    Item ||--o{ ExchangeSchedule : "scheduled_for"
    Item ||--o{ Message : "discussed_in"
    
    ExchangeSchedule ||--o{ Message : "related_to"

    User {
        int id PK
        string username
        string email
        string first_name
        string last_name
        datetime date_joined
        boolean is_active
    }

    Category {
        int id PK
        string name
        text description
    }

    Item {
        int id PK
        string title
        text description
        string condition
        string location
        float latitude
        float longitude
        image image
        int donor_id FK
        int recipient_id FK
        datetime created_at
        datetime received_at
        boolean is_available
        image qr_code
        string pickup_code
        int category_id FK
    }

    ItemImage {
        int id PK
        int item_id FK
        image image
        boolean is_primary
        datetime uploaded_at
    }

    ExchangeSchedule {
        int id PK
        int item_id FK
        int donor_id FK
        int recipient_id FK
        datetime scheduled_date
        string location
        string status
        text notes
        datetime created_at
        datetime updated_at
    }

    Message {
        int id PK
        int sender_id FK
        int recipient_id FK
        int item_id FK
        int exchange_schedule_id FK
        string subject
        text content
        boolean is_read
        datetime created_at
        file attachments
    }
```

## System Component Architecture

```mermaid
graph LR
    subgraph "Client Side"
        BROWSER[Web Browser]
        JS[JavaScript Engine]
        MAP[MapBox Integration]
    end

    subgraph "Server Side"
        subgraph "Web Server"
            DJANGO[Django Application]
            WSGI[WSGI Server]
        end
        
        subgraph "Application Logic"
            AUTH_SYS[Authentication System]
            ITEM_MGT[Item Management]
            EXCHANGE_MGT[Exchange Management]
            MSG_SYS[Messaging System]
            LOCATION_SVC[Location Services]
        end
        
        subgraph "Business Logic"
            QR_GEN[QR Code Generation]
            IMG_ANALYSIS[Image Analysis]
            NOTIFICATION[Email Notifications]
            SEARCH[Search & Filtering]
        end
    end

    subgraph "Data Layer"
        DATABASE[(MySQL)]
        FILE_STORAGE[File Storage]
    end

    subgraph "External APIs"
        VISION_API[Google Cloud Vision]
        MAPBOX_API[MapBox API]
        EMAIL_SVC[Email Service]
    end

    %% Client connections
    BROWSER --> DJANGO
    JS --> DJANGO
    MAP --> MAPBOX_API

    %% Server internal connections
    DJANGO --> AUTH_SYS
    DJANGO --> ITEM_MGT
    DJANGO --> EXCHANGE_MGT
    DJANGO --> MSG_SYS
    DJANGO --> LOCATION_SVC

    %% Business logic connections
    ITEM_MGT --> QR_GEN
    ITEM_MGT --> IMG_ANALYSIS
    EXCHANGE_MGT --> NOTIFICATION
    ITEM_MGT --> SEARCH

    %% Data connections
    AUTH_SYS --> DATABASE
    ITEM_MGT --> DATABASE
    EXCHANGE_MGT --> DATABASE
    MSG_SYS --> DATABASE
    ITEM_MGT --> FILE_STORAGE

    %% External API connections
    IMG_ANALYSIS --> VISION_API
    LOCATION_SVC --> MAPBOX_API
    NOTIFICATION --> EMAIL_SVC

    %% Styling
    classDef client fill:#e3f2fd
    classDef server fill:#f1f8e9
    classDef business fill:#fff8e1
    classDef data fill:#fce4ec
    classDef external fill:#f3e5f5

    class BROWSER,JS,MAP client
    class DJANGO,WSGI,AUTH_SYS,ITEM_MGT,EXCHANGE_MGT,MSG_SYS,LOCATION_SVC server
    class QR_GEN,IMG_ANALYSIS,NOTIFICATION,SEARCH business
    class DATABASE,FILE_STORAGE data
    class VISION_API,MAPBOX_API,EMAIL_SVC external
```

## User Flow Diagrams

### 1. User Registration & Authentication Flow

```mermaid
flowchart LR
    A[Visit Site] --> B{New/Existing User?}
    B -->|New| C[Register]
    B -->|Existing| D[Login]
    C --> E[Create Account]
    D --> F{Valid Credentials?}
    F -->|Yes| G[Dashboard]
    F -->|No| D
    E --> G
    G --> H[Access Features]

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px
    classDef decision fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef success fill:#e8f5e8,stroke:#4caf50,stroke-width:2px
    
    class B,F decision
    class G,H success
```

### 2. Item Posting Flow

```mermaid
flowchart LR
    A[Post Item] --> B[Fill Details & Upload Images]
    B --> C[Set Location & Category]
    C --> D{Form Valid?}
    D -->|No| B
    D -->|Yes| E[AI Analysis & QR Generation]
    E --> F[Item Posted]
    F --> G[Manage Item]

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px
    classDef decision fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef success fill:#e8f5e8,stroke:#4caf50,stroke-width:2px
    classDef process fill:#e3f2fd,stroke:#1976d2,stroke-width:1px
    
    class D decision
    class F,G success
    class E process
```

### 3. Item Discovery & Request Flow

```mermaid
flowchart LR
    A[Browse Items] --> B[Search & Filter]
    B --> C[View Item Details]
    C --> D{Interested?}
    D -->|No| A
    D -->|Yes| E[Contact Donor]
    E --> F[Exchange Request]
    F --> G[Schedule Pickup]

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px
    classDef decision fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef success fill:#e8f5e8,stroke:#4caf50,stroke-width:2px
    
    class D decision
    class G success
```

### 4. Exchange Scheduling & Completion Flow

```mermaid
flowchart LR
    A[Request Received] --> B{Donor Accept?}
    B -->|No| C[Decline]
    B -->|Yes| D[Schedule Meeting]
    D --> E{Recipient Agree?}
    E -->|No| D
    E -->|Yes| F[Confirmed Exchange]
    F --> G[Meet & Scan QR]
    G --> H[Complete Exchange]

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px
    classDef decision fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef success fill:#e8f5e8,stroke:#4caf50,stroke-width:2px
    classDef decline fill:#ffcdd2,stroke:#f44336,stroke-width:2px
    
    class B,E decision
    class F,H success
    class C decline
```

### 5. Messaging System Flow

```mermaid
flowchart LR
    A[Send Message] --> B[Compose Message]
    B --> C[Add Attachments?]
    C -->|Yes| D[Upload Files]
    C -->|No| E[Send]
    D --> E
    E --> F[Message Sent & Email Notification]
    F --> G[View Inbox]

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px
    classDef decision fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef success fill:#e8f5e8,stroke:#4caf50,stroke-width:2px
    
    class C decision
    class F,G success
```

### 6. QR Code Verification Flow

```mermaid
flowchart LR
    A[Scan QR Code] --> B{Valid Code?}
    B -->|No| C[Error Message]
    B -->|Yes| D{Item Available?}
    D -->|No| E[Already Claimed]
    D -->|Yes| F[Show Item Details]
    F --> G{Confirm Pickup?}
    G -->|No| H[Cancel]
    G -->|Yes| I[Verify & Complete]
    I --> J[Exchange Complete]

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px
    classDef decision fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef success fill:#e8f5e8,stroke:#4caf50,stroke-width:2px
    classDef error fill:#ffcdd2,stroke:#f44336,stroke-width:2px
    classDef info fill:#e1f5fe,stroke:#2196f3,stroke-width:2px
    
    class B,D,G decision
    class I,J success
    class C error
    class E,H info
```

## Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        subgraph "Frontend Security"
            CSRF_TOKEN[CSRF Token Protection]
            XSS_PROTECTION[XSS Protection]
            INPUT_VALIDATION[Client-side Validation]
        end
        
        subgraph "Authentication Layer"
            DJANGO_AUTH[Django Authentication]
            SESSION_MGT[Session Management]
            PASSWORD_HASH[Password Hashing]
            LOGIN_THROTTLE[Login Throttling]
        end
        
        subgraph "Authorization Layer"
            PERMISSION_CHECK[Permission Checks]
            USER_OWNERSHIP[User Ownership Validation]
            EXCHANGE_AUTH[Exchange Authorization]
        end
        
        subgraph "Data Security"
            SQL_INJECTION[SQL Injection Protection]
            FILE_VALIDATION[File Upload Validation]
            DATA_SANITIZATION[Data Sanitization]
        end
        
        subgraph "Communication Security"
            HTTPS[HTTPS Encryption]
            API_SECURITY[API Security]
            EMAIL_SECURITY[Secure Email Handling]
        end
    end

    subgraph "External Security"
        GCLOUD_AUTH[Google Cloud API Auth]
        MAPBOX_AUTH[MapBox API Auth]
        SECURE_KEYS[Secure Key Management]
    end

    %% Security flow connections
    INPUT_VALIDATION --> CSRF_TOKEN
    CSRF_TOKEN --> DJANGO_AUTH
    DJANGO_AUTH --> SESSION_MGT
    SESSION_MGT --> PERMISSION_CHECK
    PERMISSION_CHECK --> USER_OWNERSHIP
    USER_OWNERSHIP --> EXCHANGE_AUTH
    
    DATA_SANITIZATION --> SQL_INJECTION
    FILE_VALIDATION --> DATA_SANITIZATION
    
    API_SECURITY --> HTTPS
    EMAIL_SECURITY --> HTTPS
    
    SECURE_KEYS --> GCLOUD_AUTH
    SECURE_KEYS --> MAPBOX_AUTH

    %% Styling
    classDef frontend fill:#e3f2fd
    classDef auth fill:#f1f8e9
    classDef authz fill:#fff3e0
    classDef data fill:#fce4ec
    classDef comm fill:#f3e5f5
    classDef external fill:#ffebee

    class CSRF_TOKEN,XSS_PROTECTION,INPUT_VALIDATION frontend
    class DJANGO_AUTH,SESSION_MGT,PASSWORD_HASH,LOGIN_THROTTLE auth
    class PERMISSION_CHECK,USER_OWNERSHIP,EXCHANGE_AUTH authz
    class SQL_INJECTION,FILE_VALIDATION,DATA_SANITIZATION data
    class HTTPS,API_SECURITY,EMAIL_SECURITY comm
    class GCLOUD_AUTH,MAPBOX_AUTH,SECURE_KEYS external
```

## Technology Stack Overview

```mermaid
graph LR
    subgraph "Frontend Technologies"
        HTML[HTML5]
        CSS[CSS3 + Tailwind]
        JS[JavaScript ES6+]
        GSAP[GSAP Animations]
        SWIPER[Swiper.js]
        MAPBOX_JS[MapBox GL JS]
    end

    subgraph "Backend Technologies"
        PYTHON[Python 3.x]
        DJANGO[Django 4.2+]
        DRF[Django REST Framework]
        MYSQL[MySQL Database]
    end

    subgraph "External APIs"
        VISION[Google Cloud Vision]
        MAPBOX_API[MapBox API]
        EMAIL_API[Email Service]
    end

    subgraph "Libraries & Tools"
        QR_LIB[QRCode Library]
        PIL[Pillow (PIL)]
        CORS[Django CORS Headers]
        WIDGET[Widget Tweaks]
    end

    subgraph "Development Tools"
        GIT[Git Version Control]
        ENV[Environment Variables]
        VENV[Virtual Environment]
    end

    %% Technology connections
    HTML --> CSS
    CSS --> JS
    JS --> GSAP
    JS --> SWIPER
    JS --> MAPBOX_JS

    PYTHON --> DJANGO
    DJANGO --> DRF
    DJANGO --> MYSQL

    DJANGO --> VISION
    MAPBOX_JS --> MAPBOX_API
    DJANGO --> EMAIL_API

    DJANGO --> QR_LIB
    DJANGO --> PIL
    DJANGO --> CORS
    DJANGO --> WIDGET

    %% Styling
    classDef frontend fill:#e1f5fe
    classDef backend fill:#f3e5f5
    classDef external fill:#fff3e0
    classDef libraries fill:#e8f5e8
    classDef tools fill:#fce4ec

    class HTML,CSS,JS,GSAP,SWIPER,MAPBOX_JS frontend
    class PYTHON,DJANGO,DRF,MYSQL backend
    class VISION,MAPBOX_API,EMAIL_API external
    class QR_LIB,PIL,CORS,WIDGET libraries
    class GIT,ENV,VENV tools
```

## Summary

This comprehensive architecture documentation covers:

1. **High-Level System Architecture** - Shows the overall system structure with frontend, backend, database, and external services
2. **Data Model Architecture** - Entity-relationship diagram showing database structure
3. **System Component Architecture** - Detailed view of system components and their interactions
4. **User Flow Diagrams** - Six key user journeys covering the main application features
5. **Security Architecture** - Security layers and protection mechanisms
6. **Technology Stack Overview** - All technologies used in the project

The WasteNot application is a well-architected Django-based web application that facilitates community item sharing with robust features for user management, item posting, exchange scheduling, messaging, and secure pickup verification through QR codes.
