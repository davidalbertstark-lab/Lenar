# Lenar — Technology Stack

> **Status:** Technology Reference  
> **Document:** 10 — Technology Stack  
> **Purpose:** Define the technologies currently selected for Lenar, the responsibility of each technology, the boundaries between technologies, the reasons for the major choices, and the rules for introducing, replacing, or evolving dependencies.

---

## At a Glance

Lenar uses a deliberately practical technology stack. The goal is not to assemble the newest or most sophisticated technologies. The goal is to provide a stack that can support:
- a coherent multi-platform product;
- strong backend architecture;
- reliable offline behavior;
- secure data handling;
- maintainable development;
- good performance;
- scalable growth;
- effective testing;
- operational simplicity.

These choices are organized around the system architecture defined in [09-System-Architecture.md](09-System-Architecture.md) and the product requirements defined in [../product/03-Product-Requirements.md](../product/03-Product-Requirements.md).

---

## 1. Technology Philosophy

Technology exists to serve product requirements. The preferred stack is therefore the one that provides an appropriate combination of:
```text
Capability
+
Correctness
+
Security
+
Performance
+
Maintainability
+
Developer productivity
+
Operational simplicity
+
Cost
```

---

## 2. Technology Stack Overview

The stack is composed of grouped responsibility layers to ensure cohesive development across environments.

```mermaid
flowchart TD
    classDef group fill:#f8fafc,stroke:#94a3b8,stroke-width:2px,color:#0f172a,font-weight:bold
    classDef item fill:#eff6ff,stroke:#3b82f6,stroke-width:1px,color:#1e40af

    subgraph Web[Web]
        direction LR
        W1[React + TypeScript + Vite]
    end

    subgraph Mobile[Mobile]
        direction LR
        M1[Flutter + Dart]
    end

    subgraph Backend[Backend]
        direction LR
        B1[FastAPI + Python]
        B2[Pydantic]
        B3[SQLAlchemy]
        B4[Alembic]
    end

    subgraph Data[Data]
        direction LR
        D1[PostgreSQL]
        D2[SQLite local persistence]
    end

    subgraph Supporting[Supporting]
        direction LR
        S1[Lenar JWT Auth]
        S2[Cloudflare R2]
        S3[FCM]
        S4[PostHog]
        S5[Sentry]
        S6[OpenTelemetry]
    end

    subgraph Delivery[Delivery]
        direction LR
        Del1[GitHub Actions]
        Del2[Docker]
        Del3[Managed Infrastructure]
    end

    Web ~~~ Mobile
    Mobile ~~~ Backend
    Backend ~~~ Data
    Data ~~~ Supporting
    Supporting ~~~ Delivery

    class Web,Mobile,Backend,Data,Supporting,Delivery group;
    class W1,M1,B1,B2,B3,B4,D1,D2,S1,S2,S3,S4,S5,S6,Del1,Del2,Del3 item;
```

---

## 3. Technology Responsibility Map

Technologies in Lenar have strict responsibility boundaries. A single tool must not silently become responsible for unrelated concerns. 

```mermaid
flowchart LR
    classDef cap fill:#fef3c7,stroke:#d97706,stroke-width:1px,color:#92400e
    classDef bound fill:#f1f5f9,stroke:#64748b,stroke-width:1px,color:#334155,stroke-dasharray: 4 4
    classDef tech fill:#dcfce3,stroke:#22c55e,stroke-width:1px,color:#166534,font-weight:bold

    subgraph Capability [Product Capability]
        C1[Web UI]
        C2[Mobile UI]
        C3[API]
        C4[Schema validation]
        C5[Database access]
        C6[Migrations]
        C7[Authoritative data]
        C8[Authentication]
        C9[Storage]
        C10[Push]
        C11[Analytics]
        C12[Errors]
        C13[Telemetry]
    end

    subgraph Boundary [Implementation Boundary]
        B1(( ))
        B2(( ))
        B3(( ))
        B4(( ))
        B5(( ))
        B6(( ))
        B7(( ))
        B8(( ))
        B9(( ))
        B10(( ))
        B11(( ))
        B12(( ))
        B13(( ))
    end

    subgraph Technology [Technology]
        T1[React]
        T2[Flutter]
        T3[FastAPI]
        T4[Pydantic]
        T5[SQLAlchemy]
        T6[Alembic]
        T7[PostgreSQL]
        T8[Lenar JWT Auth]
        T9[R2]
        T10[FCM]
        T11[PostHog]
        T12[Sentry]
        T13[OpenTelemetry]
    end

    C1 --- B1 --- T1
    C2 --- B2 --- T2
    C3 --- B3 --- T3
    C4 --- B4 --- T4
    C5 --- B5 --- T5
    C6 --- B6 --- T6
    C7 --- B7 --- T7
    C8 --- B8 --- T8
    C9 --- B9 --- T9
    C10 --- B10 --- T10
    C11 --- B11 --- T11
    C12 --- B12 --- T12
    C13 --- B13 --- T13

    class C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13 cap;
    class B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,B11,B12,B13 bound;
    class T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13 tech;
```

### Current Core Boundaries
- **React** → Web UI
- **Flutter** → Mobile application / UI
- **FastAPI** → HTTP/API boundary
- **Pydantic** → API schemas and validation
- **SQLAlchemy 2.x** → Server-side data access
- **Alembic** → Database migrations
- **PostgreSQL** → Authoritative relational state
- **SQLite-based architecture** → Selected mobile local state / offline support
- **Lenar-controlled authentication** → JWT / Credentials / Sessions
- **Lenar authorization** → Server-side authority (Permissions)
- **Cloudflare R2** → Object storage
- **Firebase Cloud Messaging (FCM)** → Push delivery
- **PostHog** → Product analytics
- **Sentry** → Error monitoring
- **OpenTelemetry** → Telemetry / instrumentation
- **GitHub Actions** → Automation / CI/CD
- **Docker** → Packaging / reproducible environments

---

## 4. Critical Boundaries & Distinctions

A technology implements product responsibilities; it does not redefine product or domain authority. 

```mermaid
flowchart TD
    classDef step fill:#f8fafc,stroke:#94a3b8,stroke-width:2px,color:#0f172a,font-weight:bold
    classDef note fill:none,stroke:none,font-style:italic,color:#334155

    PD[Product / Domain]
    AB[Application Boundary]
    T[Technology]
    IP[Infrastructure / Provider]
    
    PD --> AB
    AB --> T
    T --> IP
    
    N["Technology implements product responsibilities.<br/>Technology does not redefine product/domain authority."]
    
    IP ~~~ N
    
    class PD,AB,T,IP step;
    class N note;
```

We explicitly separate related but distinct responsibilities:
- **AUTHENTICATION ≠ AUTHORIZATION**
- **DATABASE ≠ CACHE**
- **DATABASE ≠ SEARCH INDEX**
- **DATABASE ≠ ANALYTICS**
- **NOTIFICATION ≠ AUTHORITATIVE STATE**
- **ANALYTICS ≠ APPLICATION DATABASE**
- **TECHNOLOGY ≠ PRODUCT CAPABILITY**
- **PROVIDER ≠ DOMAIN AUTHORITY**
- **FRAMEWORK ≠ DOMAIN MODEL**

---

## 5. Specific Technology Constraints

### 5.1 Mobile Framework
**Flutter** is the current selected mobile framework. While Kotlin Multiplatform + Native UI was heavily evaluated, Flutter currently provides the strongest overall trade-off for Lenar's present mobile requirements. This choice does not claim Flutter is universally superior to all alternatives.

### 5.2 PostgreSQL
**PostgreSQL** is the authoritative relational database direction. However, this does not mean every possible future dataset or cache must live in PostgreSQL. 

### 5.3 Mobile Local Persistence
The mobile local persistence direction relies on **SQLite**. Local storage may contain a cache, drafts, durable user intent, pending operations, and sync metadata. It must *not* be treated as a full mirror of the entire server database.

### 5.4 Authentication vs Authorization
**Lenar-controlled JWT authentication** handles authentication (proving user identity). It does *not* define Lenar's complete authorization model. Server-side authorization remains authoritative.

### 5.5 Object Storage
**Cloudflare R2** is the direction for object storage. Protected file access must remain aligned with the permissions of the associated domain resource. The raw file URL is not an authorization boundary.

### 5.6 Analytics & Observability
These must remain conceptually separated:
- **PostHog** handles product analytics.
- **Sentry** tracks application error monitoring.
- **OpenTelemetry** handles systemic instrumentation.
None of these tools are permitted to become a structural dependency for core, authoritative product correctness.

---

## 6. Dependency Policy & Technology Lifecycle

Technology choices are lifecycle-managed rather than permanent by default.

```mermaid
flowchart LR
    classDef state fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a,font-weight:bold
    classDef reeval fill:#fef08a,stroke:#ca8a04,stroke-width:1px,color:#854d0e,font-style:italic

    P[Proposed]
    E[Evaluated]
    S[Selected]
    I[Implemented]
    M[Maintained]
    D[Deprecated]
    R[Replaced]
    
    P --> E
    E --> S
    S --> I
    I --> M
    M --> D
    D --> R
    
    ERC[Evidence / Requirement Change]
    
    M -.-> ERC
    ERC -.-> E
    
    class P,E,S,I,M,D,R state;
    class ERC reeval;
```

**The core rule:** If the existing stack can safely and adequately satisfy a requirement, prefer using it over introducing another dependency.

Any new technology addition or replacement must be formally justified by:
`problem + benefit + cost + risk + maintenance + replaceability`

---

## Related Documentation

For context on how these technologies fulfill product and architectural needs, refer to:

- [../product/03-Product-Requirements.md](../product/03-Product-Requirements.md)
- [05-Platform.md](05-Platform.md)
- [../product/06-Data-Content.md](../product/06-Data-Content.md)
- [../product/07-Security-Privacy-Governance.md](../product/07-Security-Privacy-Governance.md)
- [08-Offline-Sync-Resilience.md](08-Offline-Sync-Resilience.md)
- [09-System-Architecture.md](09-System-Architecture.md)
- [11-Performance-Reliability.md](11-Performance-Reliability.md)
- [12-Testing-Quality.md](12-Testing-Quality.md)
- [13-Analytics-Observability.md](13-Analytics-Observability.md)
- [14-Infrastructure-Operations.md](14-Infrastructure-Operations.md)
- [16-Development-Release.md](16-Development-Release.md)
- [../decisions/17-Decisions-Risks-Evolution.md](../decisions/17-Decisions-Risks-Evolution.md)
