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

### Architecture Decision Record (ADR) Lifecycle

```mermaid
flowchart TD
    classDef phase fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a
    classDef core fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e40af,font-weight:bold
    classDef decision fill:#dcfce3,stroke:#16a34a,stroke-width:2px,color:#166534,font-weight:bold
    classDef review fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e,font-weight:bold

    subgraph Phase1 ["1. Problem Evaluation & Evidence"]
        direction TB
        Q["Architectural Question<br/>Core Problem Framing"]:::core
        O["Viable Options<br/>Alternatives Considered"]:::phase
        E["Empirical Evidence<br/>Production Data & Benchmarks"]:::phase
        T["Trade-off Analysis<br/>Costs, Limits & Reversibility"]:::phase

        Q -->|"Explore"| O
        O -->|"Evaluate"| E
        E -->|"Weigh"| T
    end

    subgraph Phase2 ["2. ADR Commitment & Impact"]
        direction TB
        D["Formal Decision<br/>Documented in ADR"]:::decision
        C["Consequences<br/>Architectural Debt & Constraints"]:::phase

        D -->|"Documents"| C
    end

    subgraph Phase3 ["3. Review Triggers & Evolution"]
        direction TB
        RC["Review Conditions<br/>Explicit Invalidation Triggers"]:::phase
        REC["Reconsideration Trigger<br/>New Production Evidence"]:::review

        RC -->|"Monitors for"| REC
    end

    T -->|"Selects path"| D
    C -->|"Defines guardrails"| RC
    REC -.->|"Invalidates assumptions"| Q
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

#### Risk Management Lifecycle

```mermaid
flowchart TD
    classDef risk fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#991b1b,font-weight:bold
    classDef step fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a
    classDef monitor fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e40af,font-weight:bold

    subgraph Assessment ["1. Identification & Assessment"]
        direction TB
        R["Risk Identification<br/>Potential Future Failure Mode"]:::risk
        U["Understand Context<br/>Root Causes & Exposure Triggers"]:::step
        A["Assess Severity<br/>Calculate: Probability × Impact"]:::step

        R -->|"Analyze root cause"| U
        U -->|"Score exposure"| A
    end

    subgraph Treatment ["2. Treatment & Governance"]
        direction TB
        Mit["Mitigate & Control<br/>Preventive Architectural Countermeasures"]:::step
        Mon["Continuous Monitoring<br/>Track Leading Indicators & Telemetry"]:::monitor
        Re["Periodic Reassessment<br/>Evaluate Residual Risk & Effectiveness"]:::monitor

        Mit -->|"Observe in production"| Mon
        Mon -->|"Review telemetry"| Re
    end

    A -->|"Define controls"| Mit
    Re -.->|"Residual or new risk detected"| R
```

### 6.2 Technical Debt
We explicitly distinguish between **intentional debt** (taken deliberately to meet a deadline with a known cost) and **unintentional debt** (accrued through poor quality or misunderstanding).

All recorded technical debt should have a reason, documented impact, risk, assigned owner, and a clear repayment trigger. We do not maintain giant debt registers full of invented or trivial items.

---

## 7. Decision Dependencies & Change Impact

Major decisions rarely exist in isolation; they influence the entire system topology.

### Architectural Decision Dependency Flow

```mermaid
flowchart TD
    classDef core fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e40af,font-weight:bold
    classDef cross fill:#f8fafc,stroke:#64748b,stroke-width:1.5px,color:#334155
    classDef delivery fill:#f0fdf4,stroke:#22c55e,stroke-width:1.5px,color:#166534

    subgraph CrossCutting ["Cross-Cutting Architectural Guardrails"]
        direction TB
        Sec["Security & Governance<br/>Server-Side Authz, Legal & Privacy"]:::cross
        Data["Data & Resilience<br/>Authority, Local SQLite & Offline Sync"]:::cross
        Obs["Platform & Observability<br/>Cloudflare R2, OpenTelemetry & Infra"]:::cross
    end

    subgraph Cascade ["Primary Decision Cascade"]
        direction TB
        PR["Product Requirements<br/>Canonical Scope & User Needs"]:::core
        Arch["System Architecture<br/>Modular Monolith & Explicit Boundaries"]:::core
        Tech["Technology Choices<br/>FastAPI, Flutter, React, PostgreSQL"]:::core

        PR -->|"Shapes"| Arch
        Arch -->|"Selects"| Tech
    end

    subgraph Delivery ["Delivery & Verification"]
        direction TB
        Imp["Implementation<br/>Modular Monolith Codebase"]:::delivery
        Test["Testing & Quality<br/>Contract, Sync & Regression Tests"]:::delivery
        Ops["Operations & Runtime<br/>Production Deployment & Health"]:::delivery

        Imp -->|"Validated by"| Test
        Test -->|"Released to"| Ops
    end

    Sec <-->|"Constrains"| Arch
    Data <-->|"Contracts with"| Arch
    Obs <-->|"Instruments"| Tech
    Tech -->|"Executes via"| Imp
```

Consequently, a significant architectural or technological change has a massive impact surface that must be explicitly reviewed across disciplines.

### Cross-Disciplinary Review Surface for Significant Changes

```mermaid
flowchart TD
    classDef change fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#991b1b,font-weight:bold
    classDef product fill:#eff6ff,stroke:#3b82f6,stroke-width:1px,color:#1e40af
    classDef tech fill:#f8fafc,stroke:#475569,stroke-width:1px,color:#0f172a
    classDef ops fill:#fef3c7,stroke:#d97706,stroke-width:1px,color:#92400e

    SC["Proposed Significant Change<br/><b>Core Architecture or Technology Modification</b>"]:::change

    subgraph ProductReview ["1. Product & Business Review"]
        direction TB
        P["Product Requirements & Scope"]:::product
        UX["User Experience & Flows"]:::product
        LB["Legal, Privacy & Business Constraints"]:::product
        P --- UX --- LB
    end

    subgraph TechReview ["2. Architecture & Data Review"]
        direction TB
        Arch["System Architecture & Boundaries"]:::tech
        Tech["Technology Stack & Dependencies"]:::tech
        Sync["Data Authority & Offline / Sync Protocol"]:::tech
        Arch --- Tech --- Sync
    end

    subgraph OpsReview ["3. Assurance & Operations Review"]
        direction TB
        Sec["Security & Server-Side Authorization"]:::ops
        Test["Testing & Quality Verification"]:::ops
        Ops["Infrastructure, Telemetry & SRE"]:::ops
        Sec --- Test --- Ops
    end

    SC -->|"Evaluates product scope"| P
    SC -->|"Evaluates boundaries & sync"| Arch
    SC -->|"Evaluates security & runtime"| Sec
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
