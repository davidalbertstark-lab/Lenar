# Lenar — Offline, Sync & Resilience

> **Status:** Core Architecture Reference  
> **Document:** 08 — Offline, Sync & Resilience  
> **Purpose:** Define how Lenar behaves when connectivity is weak, unavailable, interrupted, or restored; how local state and server state relate; how supported offline actions are preserved and synchronized; how conflicts and failures are handled; and how the system recovers without unnecessarily losing user work or data integrity.

---

## At a Glance

Lenar is designed for a world where connectivity cannot always be assumed. An offline-first product must answer more than *"Can the app work without internet?"* It must answer:
- What can the user do?
- What is saved locally?
- What has reached the server?
- What happens when local state and server state differ?

The central principle is:
> **Preserve supported user intent locally, synchronize it safely when connectivity returns, and keep the server authoritative for shared state.**

Offline support is therefore a **feature-by-feature product capability**, not a blanket promise that every part of Lenar works without connectivity.

---

## 1. The Offline-First Principle

Offline-first means that the application is designed with disconnected operation as a normal condition for supported experiences rather than as an exceptional error.

It does **not** mean:
- every feature works offline;
- approval works offline;
- enrollment is established offline;
- authorization can be decided offline permanently;
- every piece of server data is stored locally;
- the device becomes the source of truth;
- local data automatically becomes authoritative;
- every action can be completed without server interaction.

Instead:
```text
Connectivity
    ↓
may improve or degrade
    ↓
supported features adapt
```

---

## 2. Synchronization Architecture

The mobile client maintains a clear separation between its internal local database, its queue of outbound operations, and the synchronization engine responsible for talking to the network.

```mermaid
flowchart TD
    classDef boundary fill:#f1f5f9,stroke:#94a3b8,stroke-width:2px,color:#0f172a,font-weight:bold
    classDef component fill:#fff,stroke:#cbd5e1,stroke-width:1px,color:#334155
    classDef flow fill:#eff6ff,stroke:#3b82f6,stroke-width:1px,color:#1e40af,font-style:italic

    subgraph Mobile[Mobile App]
        LD[Local Data]
        PO[Pending Operations / Outbox]
        SE[Sync Engine]
        LD --- SE
        PO --- SE
    end

    NW((Network))

    subgraph Server[Lenar API]
        VA[Validation / Authorization]
        DL[Domain Logic]
        AD[Authoritative Data]
        VA --- DL
        DL --- AD
    end

    SE <--> NW
    NW <--> VA

    SC[Server Changes]
    SyncFlow[synchronization]
    LR[local representation]

    SC --> SyncFlow
    SyncFlow --> LR

    class Mobile,Server boundary;
    class LD,PO,SE,VA,DL,AD component;
    class SC,SyncFlow,LR flow;
```

---

## 3. Offline Write & Synchronization

When a user performs an action offline, it must be safely durably preserved, then correctly synchronized.

```mermaid
sequenceDiagram
    participant U as User
    participant MC as Mobile Client
    participant LD as Local Database
    participant OB as Outbox
    participant NW as Network
    participant S as FastAPI / Server
    participant AD as Authoritative Data

    U->>MC: User Action
    MC->>LD: Local Durable Save (Locally Saved)
    MC->>OB: Mark as Pending
    Note over LD, OB: Operation is Pending,<br/>NOT Server Confirmed

    opt Connectivity Returns
        OB->>NW: Sync Attempt
        NW->>S: Transmit Operation
        S->>S: Server Validation / Authorization
        S->>AD: Authoritative Change
        AD-->>S: Success
        S-->>NW: Confirmation
        NW-->>OB: Server Confirmed
        OB->>LD: Local Reconciliation
        LD-->>MC: State Updated
        MC-->>U: Confirmed UI State
    end
```

### 3.1 Critical Conceptual Distinctions

These states must never be collapsed or confused in either the architecture or the user interface:

- **OFFLINE:** The device has no usable network connection.
- **LOCAL SAVE:** User intent/state is durably preserved on the device.
- **PENDING:** The operation exists locally but has not been server-confirmed.
- **SYNCING:** The operation is actively being processed against the server.
- **SERVER CONFIRMED:** The authoritative server state confirms the operation.
- **CONFLICT:** Local intent cannot be applied automatically under current rules.
- **REJECTED:** The authoritative server refuses or invalidates the operation.
- **STALE DATA:** The locally available representation may no longer be current.

---

## 4. Operation Lifecycle & Idempotency

Operations progress through a predictable lifecycle as they transition from local intent to authoritative server state.

```mermaid
flowchart TD
    classDef main fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a,font-weight:bold
    classDef endstate fill:#dcfce3,stroke:#22c55e,stroke-width:2px,color:#166534,font-weight:bold
    classDef failstate fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#991b1b,font-weight:bold
    classDef title fill:none,stroke:none,font-weight:bold,font-size:16px

    Title[Generalized Operation Lifecycle]
    style Title fill:none,stroke:none,color:#0f172a,font-weight:bold

    C[Created]
    P[Pending]
    S[Syncing]
    Conf[Confirmed]
    
    TF[Temporary Failure]
    CR[Conflict / Rejection]
    NR[Needs Resolution / Terminal Failure]

    C --> P
    P --> S
    S --> Conf
    
    S --> TF
    TF -->|Retry| P
    
    S --> CR
    CR --> NR

    class C,P,S main;
    class Conf endstate;
    class TF,CR,NR failstate;
```

### 4.1 Idempotency
A single logical user operation must not accidentally become multiple authoritative effects because of:
- retries
- timeouts
- duplicated delivery
- app restarts
- repeated synchronization

The exact key generation strategy will be defined in implementation, but the architectural requirement is absolute: **retry must be safe.**

---

## 5. Authorization and Conflicts

### 5.1 Authorization Re-Evaluation
The server re-evaluates authorization when the operation reaches the authoritative boundary. Do not assume that an authorization result observed before going offline remains permanently valid when connectivity returns.

### 5.2 Conflict Handling
Lenar does not rely on one universal conflict algorithm. Conflict strategy depends strictly on domain semantics. Potential strategies (e.g., server wins, merge, reject, user resolution) are applied only where justified by the specific domain rule.

```mermaid
flowchart TD
    classDef state fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a,font-weight:bold
    classDef decision fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e,font-weight:bold
    classDef action fill:#eff6ff,stroke:#3b82f6,stroke-width:1px,color:#1e40af
    classDef recovery fill:#f0fdf4,stroke:#16a34a,stroke-width:1px,color:#14532d,stroke-dasharray: 4 4

    LO[Local Operation]
    CSS[Current Server State]
    
    CM{Can Merge?}
    
    LO --> CM
    CSS --> CM
    
    AR[Apply / Reconcile]
    CM -->|Yes| AR
    
    C[Conflict]
    CM -->|No| C
    
    DR[Domain Rule / User Resolution]
    C --> DR
    
    FS[Final State]
    DR --> FS
    AR --> FS

    %% Recovery Path
    DI[Detect inconsistency]
    RBLR[rebuild/recover local representation]
    OAS[obtain authoritative state]
    RVPI[reconcile valid pending intent]
    RS[resume synchronization]

    DI -.-> RBLR
    RBLR -.-> OAS
    OAS -.-> RVPI
    RVPI -.-> RS

    class LO,CSS,FS state;
    class CM decision;
    class AR,C,DR action;
    class DI,RBLR,OAS,RVPI,RS recovery;
```

---

## 6. Local Storage, Performance, and UX

### 6.1 Local Storage
Do not mirror the entire server by default. Local persistence is selected according to:
- User value
- Offline usefulness
- Data sensitivity
- Freshness requirements
- Storage cost
- Sync complexity

It is vital to distinguish an **optional cache** from **important pending user intent**.

### 6.2 Performance and Network
- Avoid unnecessary full refreshes.
- Prefer incremental synchronization where appropriate.
- Avoid unnecessary duplicate payloads.
- Control retry behavior to prevent server flooding.
- Minimize unnecessary battery and network usage.

### 6.3 UX Connection
The user interface should clearly distinguish: Offline, Saved locally, Pending, Syncing, Synced, Needs attention, and Failed. **Never allow the UI to claim server confirmation before authoritative confirmation exists.**

---

## 7. Resilience, Recovery, and Testing

The architecture must have a clear path from failure back toward a trusted state.

```mermaid
flowchart TD
    classDef state fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a,font-weight:bold
    classDef action fill:#2563eb,color:#fff,stroke:#1e40af,stroke-width:2px,font-weight:bold

    SN[Strong Network]
    WN[Weak Network]
    IN[Intermittent]
    OFF[Offline]
    RF[Request Failure]
    AT[App Termination]
    DR[Device Restart]
    BF[Backend Failure]
    REC[Recovery]

    FS[Fail Safely]
    PI[Preserve Intent]
    RC[Recover]
    CV[Converge]

    SN --> WN
    WN --> IN
    IN --> OFF
    OFF --> RF
    RF --> AT
    AT --> DR
    DR --> BF
    BF --> REC

    REC -.-> FS
    FS -.-> PI
    PI -.-> RC
    RC -.-> CV

    class SN,WN,IN,OFF,RF,AT,DR,BF,REC state;
    class FS,PI,RC,CV action;
```

### 7.1 Testing the Model
The resilience model demands robust testing across critical scenarios, including:
- Offline submission
- App termination after local persistence
- Device restart
- Network loss during a request
- Timeout and duplicate retry
- Authorization change while offline
- Server-side resource change while offline (Deleted resource / Conflict)
- Expired authentication
- Full resynchronization
- Local storage pressure
- Backend outage

### 7.2 Observability
Synchronization health should be measurable. Key metrics include:
- Queue size and queue age
- Sync success rate vs failure rate
- Retry count and conflict rate
- Full-resync frequency
- Synchronization latency

*(Note: Analytics are secondary. An analytics failure must not break core authoritative operations).*

---

## Related Documentation

For how offline behavior connects to the broader system, refer to:

- [../product/03-Product-Requirements.md](../product/03-Product-Requirements.md)
- [../product/04-UX-UI.md](../product/04-UX-UI.md)
- [../product/06-Data-Content.md](../product/06-Data-Content.md)
- [../product/07-Security-Privacy-Governance.md](../product/07-Security-Privacy-Governance.md)
- [09-System-Architecture.md](09-System-Architecture.md)
- [10-Technology-Stack.md](10-Technology-Stack.md)
- [11-Performance-Reliability.md](11-Performance-Reliability.md)
- [12-Testing-Quality.md](12-Testing-Quality.md)
- [13-Analytics-Observability.md](13-Analytics-Observability.md)
- [16-Development-Release.md](16-Development-Release.md)
- [../decisions/17-Decisions-Risks-Evolution.md](../decisions/17-Decisions-Risks-Evolution.md)
