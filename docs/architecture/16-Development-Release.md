# Lenar — Development & Release

> **Status:** Development & Delivery Reference  
> **Document:** 16 — Development & Release  
> **Purpose:** Define how Lenar is developed, reviewed, integrated, tested, versioned, released, and maintained so that changes can move from implementation to production in a controlled, repeatable, and understandable way.

---

## At a Glance

Lenar needs a development process that makes it possible to move quickly without making the system chaotic. The development strategy aims to balance:

```text
Speed + Quality + Security + Consistency + Traceability + Recoverability
```

---

## 1. Development Philosophy & Source of Truth

The development lifecycle connects requirements to observed production behavior, creating a continuous feedback loop.

```mermaid
flowchart TD
    classDef step fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a,font-weight:bold
    classDef action fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e40af,font-weight:bold
    classDef output fill:#dcfce3,stroke:#22c55e,stroke-width:2px,color:#166534,font-weight:bold

    R[Requirement]
    D[Design]
    I[Implement]
    T[Test]
    Rev[Review]
    Int[Integrate]
    Rel[Release]
    O[Observe]
    Imp[Improve]

    R --> D
    D --> I
    I --> T
    T --> Rev
    Rev --> Int
    Int --> Rel
    Rel --> O
    O --> Imp

    Imp -.-> R
    Imp -.-> D

    class R,D,I,T,Rev,Int step;
    class Rel,O,Imp action;
```

### 1.1 The Source of Truth
- **Canonical documentation** defines product and architecture intent.
- **Code** implements it.

If implementation reveals a contradiction or flaw in the architecture, you must **identify the discrepancy → resolve the decision → update the source of truth.** Do not allow implementation to silently redefine architecture without documentation.

---

## 2. Change Risk Model

Not every change requires identical process depth. A minor typo fix does not require the same scrutiny as a core database migration.

```mermaid
flowchart TD
    classDef step fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a,font-weight:bold
    classDef factor fill:#eff6ff,stroke:#3b82f6,stroke-width:1px,color:#1e40af
    classDef risk fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#991b1b,font-weight:bold
    classDef outcome fill:#dcfce3,stroke:#22c55e,stroke-width:2px,color:#166534,font-weight:bold

    C[Change]
    
    subgraph Vectors [Risk Vectors]
        direction LR
        S[Scope]
        SI[Security Impact]
        DI[Data Impact]
        Comp[Compatibility]
        MC[Migration Complexity]
        Rev[Reversibility]
    end

    R[Risk]
    RVR[Required Validation / Review]

    C --> Vectors
    Vectors --> R
    R --> RVR

    class C step;
    class S,SI,DI,Comp,MC,Rev factor;
    class R risk;
    class RVR outcome;
```

- **Small Changes:** Typo, small UI fix, isolated bug fix, minor refactor.
- **Significant Changes:** New capability, domain rule, security change, architecture change, database migration, sync protocol change, or new provider. 

Larger-risk changes require stronger review, explicit validation, and more rigorous evidence.

---

## 3. Code Review

Code review is not merely about formatting and syntax. A high-quality review must evaluate:
- **Correctness** and **Tests**
- **Architecture** and **Maintainability**
- **Security** and **Data Integrity**
- **Failure Handling** (how does it break?)
- **Documentation** (is it updated?)
- **Performance** (where relevant)

---

## 4. CI/CD Flow

Lenar utilizes a structured Continuous Integration and Continuous Deployment pipeline to validate code before it reaches users.

```mermaid
flowchart TD
    classDef trigger fill:#f1f5f9,stroke:#64748b,stroke-width:1px,color:#334155,font-weight:bold
    classDef check fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e40af,font-weight:bold
    classDef env fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e,font-weight:bold
    classDef prod fill:#dcfce3,stroke:#22c55e,stroke-width:3px,color:#166534,font-weight:bold

    PR[Pull Request]
    B[Build]
    LF[Lint / Format]
    TC[Type Checks]
    T[Tests]
    SC[Security Checks]
    A[Artifact]
    S[Staging]
    V[Validation]
    P[Production]

    PR --> B
    B --> LF
    LF --> TC
    TC --> T
    T --> SC
    SC --> A
    A --> S
    S --> V
    V --> P

    class PR trigger;
    class B,LF,TC,T,SC,A check;
    class S,V env;
    class P prod;
```

*(Note: The exact CI providers and deployment platforms are implemented in code, but they strictly follow this conceptual validation funnel).*

---

## 5. Compatibility & Versioning

Because Lenar is a multi-platform product, deployment is not atomic. A **new backend** will inevitably coexist with **older mobile clients**. 

Therefore, developers must explicitly consider compatibility for:
- API requests and responses
- Database schemas
- The synchronization protocol
- Authentication tokens and sessions

The project enforces a consistent versioning approach to reflect meaningful compatibility changes and coordinate these lifecycles.

---

## 6. Database Migrations

Database migrations are the highest-risk changes. The lifecycle is:
```text
Create → Test → Review → Stage → Validate → Apply
```
Because of client compatibility, migrations should conceptually follow an **expand-and-contract** pattern where safe to do so, ensuring that the database supports both the old state and the new state simultaneously during the transition window.

---

## 7. Release & Recovery

```mermaid
flowchart TD
    classDef step fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a,font-weight:bold
    classDef issue fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#991b1b,font-weight:bold
    classDef recovery fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e,font-weight:bold

    C[Change]
    V[Validate]
    B[Build]
    S[Stage]
    R[Release]
    ST[Smoke Test]
    M[Monitor]

    P[Problem]
    RM[Rollback / Mitigate]
    V2[Validate Recovery]

    C --> V
    V --> B
    B --> S
    S --> R
    R --> ST
    ST --> M

    M -.->|If detected| P
    ST -.->|If detected| P
    
    P --> RM
    RM --> V2
    V2 --> M

    class C,V,B,S,R,ST,M step;
    class P issue;
    class RM,V2 recovery;
```

### 7.1 Rollback vs. Recovery
**Rollback ≠ Recovery.**
- **Database changes** may not be safely or easily reversible.
- **Mobile rollback** is severely constrained because older app binaries remain installed on student devices long after a new version is released.

Do not claim every release can be "automatically rolled back." Many failures require a "roll-forward" mitigation (a hotfix).

### 7.2 Emergency Releases (Hotfixes)
An emergency does not mean undocumented. Even critical hotfixes must preserve traceability, appropriate automated testing, monitoring, and post-release documentation.

---

## 8. Lifecycles: Feature Flags & Deprecation

### 8.1 Feature Flags
Feature flags allow safe, decoupled releases. However, temporary flags must not remain indefinitely. Their lifecycle is:
```text
Created → Active → Fully Released → Cleanup / Removal
```

### 8.2 Deprecation
When a feature or API is sunset, the process is:
```text
State Reason → Provide Replacement → Identify Affected Consumers → Define Migration Path → Remove
```

---

## 9. Build Security

Development pipelines are privileged environments. We explicitly protect:
- Repository integrity (branch protections)
- CI and deployment credentials
- Mobile signing certificates
- Environment secrets
- Build artifacts

---

## Related Documentation

- [../product/01-Lenar-Foundation.md](../product/01-Lenar-Foundation.md)
- [../product/03-Product-Requirements.md](../product/03-Product-Requirements.md)
- [09-System-Architecture.md](09-System-Architecture.md)
- [10-Technology-Stack.md](10-Technology-Stack.md)
- [11-Performance-Reliability.md](11-Performance-Reliability.md)
- [12-Testing-Quality.md](12-Testing-Quality.md)
- [13-Analytics-Observability.md](13-Analytics-Observability.md)
- [14-Infrastructure-Operations.md](14-Infrastructure-Operations.md)
- [../product/15-Legal-Business.md](../product/15-Legal-Business.md)
- [../decisions/17-Decisions-Risks-Evolution.md](../decisions/17-Decisions-Risks-Evolution.md)
