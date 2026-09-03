# Lenar — Product & Requirements

> **Status:** Product Reference
> **Document:** 03 — Product & Requirements
> **Purpose:** Define what Lenar is intended to provide, what belongs in the current product scope, how features are prioritized, what the system must do, how quality is measured, and what remains outside the current scope.

---

## At a Glance

Lenar is being built to reduce the fragmentation between students and the information, services, opportunities, and institutional interactions they need throughout university life.

This document translates that purpose into a product definition.

It establishes:
- the major product areas;
- the current V1 boundary;
- feature priorities;
- functional requirements;
- non-functional requirements;
- important user journeys and use cases;
- edge and failure conditions;
- acceptance criteria;
- dependencies between capabilities;
- explicit exclusions.

The objective is not to maximize the number of features. The objective is to define the **smallest complete product that meaningfully solves the most important problems Lenar is intended to solve**.

> [!IMPORTANT]
> **Product rule:** A feature belongs in Lenar because it creates meaningful value within the product's purpose and scope—not simply because it is technically possible to build.

---

## 1. Product Definition

### 1.1 What Lenar Provides

At a high level, Lenar provides a unified student-facing experience around:

1. **University information and announcements**
2. **Campus services and issue reporting**
3. **Student opportunities**
4. **Relevant student-facing experiences and services**
5. **Personalized access to information based on institutional context**
6. **Reliable operation across imperfect network conditions**

The exact implementation of each area is defined throughout the remainder of this document and its supporting specifications.

### 1.2 Product Outcome

The intended outcome is not merely:
> *"Students use another university application."*

The intended outcome is:
> **Students can more easily discover what matters, access what they need, act when necessary, and understand what happens next.**

That means product success depends on:

```text
Discoverability
+
Relevance
+
Trust
+
Actionability
+
Resilience
+
Ease of use
```

---

## 2. Major Product Areas

Lenar groups its functionality into distinct, focused product areas. Each area serves a clear segment of the student experience while connecting to the same unified platform identity.

```mermaid
flowchart TD
    classDef center fill:#2563eb,color:#fff,stroke:#1e40af,stroke-width:2px,font-weight:bold,font-size:16px
    classDef area fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#334155,font-weight:bold

    L((LENAR))
    
    A[Information & Announcements]
    B[Campus Services & Issues]
    C[Opportunities]
    D[Notifications]
    E[Search & Discovery]
    F[Student Context]
    G[Admin Control Plane]
    
    L --- A
    L --- B
    L --- C
    L --- D
    L --- E
    L --- F
    L --- G
    
    class L center;
    class A,B,C,D,E,F,G area;
```

---

## 3. The V1 Scope Boundary

The current V1 scope restricts feature expansion to ensure a stable, dependable initial release.

### In Scope for V1:
- **Authentication & Onboarding:** The complete lifecycle recognizing that account creation is not equivalent to active platform participation. Includes: Registration, Email Verification, Academic Profile Completion, Profile Submission, Pending Review, Approval (or Rejection & correction), Enrollment, Academic Context, Base Community, and Active Access.
- **Information & Announcements:** Surfacing official university, faculty, and departmental notices.
- **Campus Services & Issues:** Standardized reporting mechanisms for campus problems (e.g., maintenance).
- **Opportunities:** Aggregation of relevant events, programs, and opportunities.
- **Offline Reliability:** Core read operations and pending action queues must survive connectivity drops.

### Explicitly Excluded from V1:
- Advanced social networking or chat capabilities.
- Integrated financial or tuition payment processing.
- Unrestricted peer-to-peer file sharing.
- Complex administrative workflows unrelated to content publishing or basic issue triage.

> [!WARNING]
> Future features must remain clearly separated from the current V1 scope. Do not add speculative capabilities simply because they might be useful later.

---

## 4. Feature Dependencies

Capabilities in Lenar do not exist in isolation. Many user-facing features rely on shared foundational models.

```mermaid
flowchart TD
    classDef default fill:#f8fafc,stroke:#cbd5e1,stroke-width:1px,color:#334155
    classDef foundation fill:#e2e8f0,stroke:#64748b,stroke-width:2px,font-weight:bold,color:#0f172a
    classDef feature fill:#bfdbfe,stroke:#2563eb,stroke-width:1px,font-weight:bold,color:#1e40af

    Auth[Authentication]
    Prof[Academic Profile]
    Rev[Review / Approval]
    Enr[Enrollment]
    Context[Student Context]
    Comm[Base Community / Membership]
    
    Content[Content]
    Search[Search]
    Issue[Issue Reporting]
    Opp[Opportunities]
    Notif[Notifications]
    Local[Local Persistence]
    Offline[Offline Operations]
    Sync[Synchronization]
    Admin[Admin Control Plane]
    
    Auth --> Prof
    Prof --> Rev
    Rev --> Enr
    Enr --> Context
    Context --> Comm
    
    Auth --> Admin
    
    Comm --> Content
    Comm --> Issue
    Comm --> Opp
    
    Content --> Search
    Issue --> Search
    Opp --> Search
    
    Content --> Notif
    Issue --> Notif
    Opp --> Notif
    
    Local --> Offline
    Offline --> Sync
    
    Sync -.-> Content
    Sync -.-> Issue
    Sync -.-> Opp
    
    class Auth,Prof,Rev,Enr,Context,Comm,Local,Offline,Sync,Admin foundation;
    class Content,Search,Issue,Opp,Notif feature;
```

---

## 5. Traceability and Product State

### 5.1 Requirement Traceability

Lenar ensures every line of code traces back to a genuine user need. We do not invent features in isolation.

```mermaid
flowchart TD
    classDef step fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a,font-weight:bold

    P[Problem]
    UN[User Need]
    PR[Product Requirement]
    F[Feature]
    UC[Use Case]
    UX[UX Flow]
    S[Screen]
    API[API / Domain]
    D[Data]
    Sec[Security]
    OB[Offline Behavior]
    T[Test]
    A[Analytics]
    
    P --> UN
    UN --> PR
    PR --> F
    F --> UC
    UC --> UX
    UX --> S
    S --> API
    API --> D
    D --> Sec
    Sec --> OB
    OB --> T
    T --> A
    
    class P,UN,PR,F,UC,UX,S,API,D,Sec,OB,T,A step;
```

*(Note: Not every feature requires a heavy artifact at every layer, but the logical traceability must remain intact).*

### 5.2 Generalized Product State Model

Every feature in Lenar must account for the reality of mobile usage, unpredictable networks, and missing data. Features should progressively adapt their state.

```mermaid
flowchart TD
    classDef default fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a
    classDef state fill:#e2e8f0,stroke:#64748b,stroke-width:1px,font-weight:bold

    title[Generalized Product State Model<br/>Not a literal state machine for every feature]
    style title fill:none,stroke:none,font-weight:bold,font-size:14px

    E[Entry] --> L[Loading]
    
    L --> S[Success] --> C[Content / Action]
    L --> Em[Empty] --> ES[Empty State]
    L --> Er[Error] --> RE[Recoverable Error]
    L --> O[Offline] --> OS[Offline / Pending State]
    
    class E,L,S,C,Em,ES,Er,RE,O,OS state;
```

---

## 6. Functional Requirements and Acceptance Criteria

Acceptance criteria in Lenar describe **verifiable behavior**, not technical implementation instructions.

### 6.1 Discoverability & Relevance
- **Requirement:** A student should only see announcements relevant to their organizational context (e.g., Faculty, Department, Level) unless an announcement is university-wide.
- **Acceptance:** If a student switches their departmental context, the feed correctly filters out the previous department's exclusive content.

### 6.2 Offline Behavior & Resilience
- **Requirement:** User intent must not be silently lost during network failures.
- **Acceptance:** If a user submits an issue report while offline, the system queues the action. Closing and reopening the application must preserve the pending operation until connectivity is restored.

### 6.3 Trust & Authority
- **Requirement:** The source of any content must be visually distinct and verifiable.
- **Acceptance:** Official departmental announcements clearly display the authorized publisher and the timestamp of creation.

---

## 7. Non-Functional Requirements

- **Performance:** Information feeds should load gracefully. Search results should return without disruptive latency.
- **Reliability:** Data displayed to the user must accurately reflect the server's authoritative state when connected.
- **Accessibility:** Text must remain legible at OS-level scaled font sizes. Touch targets must accommodate standard accessibility guidelines.

---

## Related Documentation

For how these product requirements translate into specific domain models, designs, and architectures, refer to the following canonical documents:

- [02-Problem-Users-Domain.md](02-Problem-Users-Domain.md)
- [04-UX-UI.md](04-UX-UI.md)
- [../architecture/05-Platform.md](../architecture/05-Platform.md)
- [06-Data-Content.md](06-Data-Content.md)
- [07-Security-Privacy-Governance.md](07-Security-Privacy-Governance.md)
- [../architecture/08-Offline-Sync-Resilience.md](../architecture/08-Offline-Sync-Resilience.md)
- [../architecture/09-System-Architecture.md](../architecture/09-System-Architecture.md)
- [../architecture/10-Technology-Stack.md](../architecture/10-Technology-Stack.md)
- [../architecture/11-Performance-Reliability.md](../architecture/11-Performance-Reliability.md)
- [../architecture/12-Testing-Quality.md](../architecture/12-Testing-Quality.md)
- [../architecture/13-Analytics-Observability.md](../architecture/13-Analytics-Observability.md)
- [../architecture/16-Development-Release.md](../architecture/16-Development-Release.md)
- [../decisions/17-Decisions-Risks-Evolution.md](../decisions/17-Decisions-Risks-Evolution.md)
