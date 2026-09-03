# Domain Relationships

This document details how the nine foundational domains interact. 

To maintain clear system boundaries without creating monolithic interdependencies, domain interactions are divided into two complementary perspectives:
1. **Context and Dependency Flow**: How upstream events trigger state changes and supply runtime context to downstream domains.
2. **Non-Cascading Boundary Invariants**: Explicit architectural guarantees that prevent lifecycle and session disruptions from propagating across boundaries.

### Diagram A: Authoritative Domain Context and Dependency Flow

# [Authoritative Domain Context and Dependency Flow]
This diagram illustrates how identity approval propagates into academic context, community placement, and runtime authorization enforcement across the foundational domains.

*(Reference Diagram:)*

```mermaid
flowchart TD
    classDef domain fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#1e40af,font-weight:bold
    classDef engine fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#166534,font-weight:bold
    classDef boundary fill:#f8fafc,stroke:#94a3b8,stroke-width:1.5px,color:#334155,font-weight:bold

    subgraph Identity ["1. Identity & Account"]
        direction TB
        Onb["Onboarding<br/>(Review & Approval)"]:::domain
        Acc["Account Lifecycle<br/>(Account State)"]:::domain
        Auth["Authentication / Session<br/>(Session Management)"]:::domain

        Onb -->|"1. Approval triggers Active"| Acc
        Acc -.->|"11. Suspension terminates session"| Auth
    end

    subgraph Academic ["2. Academic Foundation"]
        direction TB
        Org["Organization<br/>(Institutional Units)"]:::domain
        Time["Academic Time<br/>(Effective Period)"]:::domain
        Enr["Enrollment<br/>(Academic Context)"]:::domain

        Org -->|"3. Institutional structure"| Enr
        Time -->|"4. Effective calendar period"| Enr
    end

    subgraph Participation ["3. Participation & Governance"]
        direction TB
        Comm["Community<br/>(Base Community)"]:::domain
        Mem["Membership<br/>(Base Membership)"]:::domain
        Gov["Governance<br/>(Authority Assignments)"]:::domain

        Comm -->|"6. Automatically grants"| Mem
        Comm -->|"7. Scopes authority target"| Gov
    end

    subgraph Enforcement ["4. Runtime Enforcement"]
        direction TB
        Authz["Authorization Engine<br/>(Real-Time Policy Evaluation)"]:::engine
    end

    %% Inter-domain flows
    Onb -->|"2. Approval establishes record"| Enr
    Enr -->|"5. Context determines community"| Comm

    %% Authorization context inputs
    Acc -.->|"12. Universal DENY if Suspended"| Authz
    Enr -->|"9. Enrollment status"| Authz
    Mem -->|"10. Verified membership"| Authz
    Gov -->|"8. Role & scope context"| Authz

    class Identity,Academic,Participation,Enforcement boundary
```

### Diagram B: Non-Cascading Boundary Invariants

# [Non-Cascading Boundary Invariants]
This diagram illustrates the explicit isolation boundaries that prevent lifecycle and session events in one domain from automatically cascading into destructive updates in others.

*(Reference Diagram:)*

```mermaid
flowchart TD
    classDef trigger fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#991b1b,font-weight:bold
    classDef protected fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#065f46,font-weight:bold
    classDef boundary fill:#f8fafc,stroke:#94a3b8,stroke-width:1.5px,color:#334155,font-weight:bold

    subgraph Rule1 ["1. Session Expiration Isolation"]
        direction TB
        T1["Authentication:<br/>Session Expires or Terminates"]:::trigger
        P1["Onboarding & Enrollment:<br/>Progress and Records Retained"]:::protected
        T1 -.->|"Does NOT reset"| P1
    end

    subgraph Rule2 ["2. Account Suspension Isolation"]
        direction TB
        T2["Account Lifecycle:<br/>Account Suspended / Closed"]:::trigger
        P2["Enrollment & Governance:<br/>Historical Audit Records Preserved"]:::protected
        T2 -.->|"Does NOT delete"| P2
    end

    subgraph Rule3 ["3. Academic Progression Isolation"]
        direction TB
        T3["Academic Time:<br/>Term or Calendar Advances"]:::trigger
        P3["Governance:<br/>Existing Roles Remain Active"]:::protected
        T3 -.->|"Does NOT revoke"| P3
    end

    subgraph Rule4 ["4. Governance Revocation Isolation"]
        direction TB
        T4["Governance:<br/>Leader / Superior Role Revoked"]:::trigger
        P4["Governance Subordinates:<br/>Assignments Require Explicit Action"]:::protected
        T4 -.->|"Does NOT cascade to"| P4
    end

    class Rule1,Rule2,Rule3,Rule4 boundary
```

### Onboarding → Account Lifecycle
- **Relationship:** Influences / Triggers.
- **Why:** Onboarding manages the review process; Account Lifecycle manages the state.
- **Flow:** When Onboarding reaches an `Approval` decision, it signals Account Lifecycle to transition the account from `Created` to `Active`.
- **What does NOT cross:** Onboarding does not manage the Account Lifecycle state machine directly.

### Onboarding → Enrollment
- **Relationship:** Establishes.
- **Why:** Enrollment cannot exist for unapproved users.
- **Flow:** The `Approval` decision in Onboarding triggers the initial establishment of the user's Enrollment record.
- **What does NOT cross:** Once established, Enrollment handles progression. Onboarding does not manage ongoing academic changes.

### Organization → Enrollment
- **Relationship:** Provides context.
- **Why:** Enrollment must attach a user to valid institutional units.
- **Flow:** Organization provides the valid University, Faculty, and Department structures. Enrollment consumes this to ensure the academic attachment is valid.
- **What does NOT cross:** Enrollment does not create or mutate organizational units.

### Academic Time → Enrollment
- **Relationship:** Provides temporal framework.
- **Why:** Academic context must be anchored in time.
- **Flow:** Academic Time provides the Current Effective Period. Enrollment consumes this to formulate the user's Current Academic Context.
- **What does NOT cross:** Enrollment does not alter the academic calendar.

### Enrollment → Community
- **Relationship:** Determines / Influences.
- **Why:** A user's Base Community is dictated by their academic position.
- **Flow:** Enrollment formulates the Current Academic Context. That context determines which Base Community the user belongs to.
- **What does NOT cross:** Enrollment does not directly create Community records.

### Community ↔ Membership
- **Relationship:** Owns / Contains.
- **Why:** Users need a representation of their participation within a Community.
- **Flow:** The Community domain automatically establishes Base Membership when a user matches a Base Community.
- **What does NOT cross:** Membership does not redefine the Community structure.

### Community ↔ Governance
- **Relationship:** Provides target context.
- **Why:** Governance Assignments (like Leader) need a scope.
- **Flow:** Community provides the target boundary (the specific Base Community). Governance uses this to scope the Assignment.
- **What does NOT cross:** Community does not assign roles. Membership does not automatically grant Governance authority.

### Governance → Authorization
- **Relationship:** Provides authority context.
- **Why:** The policy engine needs to know who holds what role.
- **Flow:** Governance establishes the Governance Assignment (User + Role + Target). Authorization evaluates this assignment at runtime.
- **What does NOT cross:** Governance does not execute the ALLOW/DENY decision. 

### Enrollment → Authorization
- **Relationship:** Contributes context.
- **Why:** Some policies may require a user to have an active Enrollment.
- **Flow:** Enrollment status is evaluated as part of the Authorization Context.

### Membership → Authorization
- **Relationship:** Contributes context.
- **Why:** Access to specific community features requires verified membership.
- **Flow:** Membership status is evaluated as part of the Authorization Context.

### Account Lifecycle → Authentication
- **Relationship:** Constrains.
- **Why:** Suspended/Closed accounts must not be able to log in.
- **Flow:** If Account Lifecycle changes to `Suspended`, it forces Authentication to invalidate existing sessions and deny future attempts.

### Account Lifecycle → Authorization
- **Relationship:** Overrides / Constrains.
- **Why:** A suspended user might still hold a Governance Assignment historically, but must not be allowed to act.
- **Flow:** Account status is consumed by Authorization. A `Suspended` state results in a universal DENY for protected operations.
