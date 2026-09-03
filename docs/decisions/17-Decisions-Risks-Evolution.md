# Lenar — Decisions, Risks & Evolution

> **Status:** Decision & Evolution Reference  
> **Document:** 17 — Decisions, Risks & Evolution  
> **Purpose:** Record why important Lenar decisions were made, what assumptions and risks surround them, how technical debt and future change are managed, when existing decisions should be reconsidered, and how the system evolves without losing architectural coherence.

---

## At a Glance

Lenar will change. Requirements, technology, and environments evolve. This document ensures that change remains deliberate, explainable, traceable, evidence-driven, and reversible where practical. 

> **A decision should be understandable not only when it is made, but also months or years later when someone needs to question, change, or replace it.**

---

## 1. Core Principle

We do not pretend that architecture or technology is permanent. The engineering approach is:
```text
Choose deliberately.
Document honestly.
Measure continuously.
Reconsider when evidence changes.
```

## 2. Vocabulary & Distinctions

To evaluate a system accurately, the language must be precise. Do not merge these concepts:
- **FACT:** Observed and established.
- **DECISION:** A deliberate choice between alternatives.
- **ASSUMPTION:** A belief not yet fully validated by evidence.
- **REQUIREMENT:** A condition that must be satisfied.
- **CONSTRAINT:** A limitation on available choices.

---

## 3. Architecture Decision Records (ADRs)

For decisions that are difficult to reverse, we use Architecture Decision Records (ADRs). 

ADRs should be created for choices that materially affect:
- Core architecture and security
- Data authority and synchronization protocols
- Major technology frameworks or provider dependencies

**Do NOT create ADRs for every tiny coding decision.** ADRs are conceptually stored under `docs/adr/`. 

```mermaid
flowchart TD
    classDef step fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a,font-weight:bold
    classDef decision fill:#dcfce3,stroke:#22c55e,stroke-width:2px,color:#166534,font-weight:bold
    classDef review fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e,font-weight:bold

    Q[Question]
    O[Options]
    E[Evidence]
    T[Trade-offs]
    D[Decision]
    C[Consequences]
    RC[Review Condition]
    REC[Reconsideration when evidence changes]

    Q --> O
    O --> E
    E --> T
    T --> D
    D --> C
    C --> RC
    RC --> REC
    REC -.-> Q

    class Q,O,E,T,C,RC step;
    class D decision;
    class REC review;
```

---

## 4. Current Major Decisions

The following are the established, current technological decisions for Lenar. *Do not introduce new core technologies without a formal architectural decision.*

| Domain | Technology / Strategy |
|---|---|
| **Architecture** | Modular monolith |
| **Web** | React + TypeScript + Vite |
| **Mobile** | Flutter + Dart |
| **Backend** | FastAPI + Python |
| **Validation** | Pydantic |
| **Data Access & Migrations** | SQLAlchemy 2.x & Alembic |
| **Database** | PostgreSQL |
| **Mobile Local Persistence** | SQLite-based |
| **Authentication** | Lenar-controlled JWT / Credentials / Sessions |
| **Authorization** | Lenar server-side authorization |
| **Object Storage** | Cloudflare R2 |
| **Push Notifications** | Firebase Cloud Messaging |
| **Analytics & Observability** | PostHog, Sentry, OpenTelemetry |
| **CI/CD & Packaging** | GitHub Actions, Docker |

> [!NOTE]
> **Mobile Framework Note:** Flutter is the selected mobile framework. We do not continuously reopen the debate against alternatives (e.g., KMP, React Native) unless explicit, severe, evidence-driven reconsideration triggers are hit.

---

## 5. Evidence & Evolution

### 5.1 Evidence Hierarchy
We weigh evidence according to the following preference hierarchy:
```text
Production evidence
↓
Controlled benchmark / testing
↓
Representative user evidence
↓
Development experience
↓
Technical reasoning
↓
Preference
```

### 5.2 Evolutionary Change
We do not encourage constant architectural churn. Evolution follows a disciplined path:
```text
Current State → Observed Problem → Evidence → Smallest Effective Change → Measure → Adopt or Reconsider
```

---

## 6. Risk Management & Technical Debt

### 6.1 Risk
**Risk ≠ Issue.** An issue is a problem occurring now; a risk is a future possibility.
`Risk = Probability × Impact`

```mermaid
flowchart TD
    classDef risk fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#991b1b,font-weight:bold
    classDef step fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a,font-weight:bold
    classDef monitor fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e40af,font-weight:bold

    R[Risk]
    U[Understand]
    A[Assess]
    Mit[Mitigate]
    Mon[Monitor]
    Re[Reassess]

    R --> U
    U --> A
    A --> Mit
    Mit --> Mon
    Mon --> Re
    Re -.-> R

    class R risk;
    class U,A,Mit step;
    class Mon,Re monitor;
```

### 6.2 Technical Debt
We explicitly distinguish between **intentional debt** (taken deliberately to meet a deadline with a known cost) and **unintentional debt** (accrued through poor quality or misunderstanding).

All recorded technical debt should have a reason, documented impact, risk, assigned owner, and a clear repayment trigger. We do not maintain giant debt registers full of invented or trivial items.

---

## 7. Decision Dependencies & Change Impact

Major decisions rarely exist in isolation; they influence the entire system topology.

```mermaid
flowchart TD
    classDef main flow fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e40af,font-weight:bold
    classDef cross fill:#f1f5f9,stroke:#64748b,stroke-width:1px,color:#334155,font-weight:bold

    PR[Product Requirements]
    Arch[Architecture]
    Tech[Technology]
    Imp[Implementation]
    Test[Testing]
    Ops[Operations]

    PR --> Arch
    Arch --> Tech
    Tech --> Imp
    Imp --> Test
    Test --> Ops

    Sec[Security]
    Sec <--> Arch
    Arch <--> Tech

    OS[Offline/Sync]
    Data[Data]
    Mob[Mobile]
    OS <--> Data
    Data <--> Arch
    Arch <--> Mob

    LP[Legal/Privacy]
    An[Analytics]
    Infra[Infrastructure]
    LP <--> Data
    Data <--> An
    An <--> Infra

    class PR,Arch,Tech,Imp,Test,Ops main;
    class Sec,OS,Data,Mob,LP,An,Infra cross;
```

Consequently, a significant architectural or technological change has a massive impact surface that must be explicitly reviewed across disciplines.

```mermaid
flowchart LR
    classDef center fill:#fee2e2,stroke:#ef4444,stroke-width:3px,color:#991b1b,font-weight:bold
    classDef node fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a,font-weight:bold

    SC((SIGNIFICANT<br/>CHANGE))

    subgraph Impacts
        direction TB
        P[Product]
        U[UX]
        Pl[Platform]
        D[Data]
        S[Security]
        OS[Offline / Sync]
        A[Architecture]
        T[Technology]
        Te[Testing]
        An[Analytics]
        O[Operations]
        LB[Legal / Business]
    end

    SC --- P
    SC --- U
    SC --- Pl
    SC --- D
    SC --- S
    SC --- OS
    SC --- A
    SC --- T
    SC --- Te
    SC --- An
    SC --- O
    SC --- LB

    class SC center;
    class P,U,Pl,D,S,OS,A,T,Te,An,O,LB node;
```

---

## 8. AI Governance

AI agents and tools may actively assist in implementation and decision exploration. However, **AI must not silently:**
- Invent architecture
- Reverse approved decisions
- Invent business rules
- Introduce unsupported technologies
- Resolve unresolved requirements without explicit human authorization

The correct flow when utilizing AI is:
```text
Canonical Documentation → Approved Decision → Implementation → Verification
```

If an AI identifies a gap in the architecture or requirements, it must:
```text
Identify Gap → Do Not Invent → Request Decision Resolution → Update Source of Truth → Implement
```

---

## 9. Documentation Drift

When the documented architecture and the codebase diverge:
**Documented Architecture ≠ Actual Implementation**

This divergence is treated as a defect requiring attention, not as acceptable collateral damage. The codebase implements the architecture; it does not silently redefine it.

---

## Related Documentation

- [../product/01-Lenar-Foundation.md](../product/01-Lenar-Foundation.md)
- [../product/03-Product-Requirements.md](../product/03-Product-Requirements.md)
- [../architecture/05-Platform.md](../architecture/05-Platform.md)
- [../product/06-Data-Content.md](../product/06-Data-Content.md)
- [../product/07-Security-Privacy-Governance.md](../product/07-Security-Privacy-Governance.md)
- [../architecture/08-Offline-Sync-Resilience.md](../architecture/08-Offline-Sync-Resilience.md)
- [../architecture/09-System-Architecture.md](../architecture/09-System-Architecture.md)
- [../architecture/10-Technology-Stack.md](../architecture/10-Technology-Stack.md)
- [../architecture/11-Performance-Reliability.md](../architecture/11-Performance-Reliability.md)
- [../architecture/12-Testing-Quality.md](../architecture/12-Testing-Quality.md)
- [../architecture/13-Analytics-Observability.md](../architecture/13-Analytics-Observability.md)
- [../architecture/14-Infrastructure-Operations.md](../architecture/14-Infrastructure-Operations.md)
- [../product/15-Legal-Business.md](../product/15-Legal-Business.md)
- [../architecture/16-Development-Release.md](../architecture/16-Development-Release.md)
