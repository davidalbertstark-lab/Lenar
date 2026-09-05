# Lenar — Data & Content

> [!NOTE]  
> **Purpose:** Defines the conceptual information model, defining how content and data are scoped, published, and retired.  
> **Prerequisites:** `03-Product-Requirements.md`  
> **Primary Audience:** Backend Engineers, Database Architects.



---

## At a Glance

Lenar is fundamentally an information system. 

Its usefulness depends not only on features and interfaces, but on whether the information inside it is:
- meaningful;
- accurate;
- appropriately scoped;
- discoverable;
- current;
- trustworthy;
- protected;
- recoverable;
- and represented consistently across the platforms that use it.

This document establishes the conceptual data and content model. The physical PostgreSQL schema and implementation-level data specifications belong in the appropriate supporting specifications and later implementation work.

---

## 1. Data Philosophy

Lenar should treat data as a product asset rather than merely database records. The system should preserve the meaning and relationships of information across its entire flow:

```text
Collection
   ↓
Validation
   ↓
Storage
   ↓
Use
   ↓
Update
   ↓
Archive / Retention
   ↓
Deletion where appropriate
```

---

## 2. The Lenar Information Model

The Lenar domain requires modeling several conceptual families of data that interact closely to create the student experience.

*(Reference Diagram: Conceptual Information Model — Domain Families & Structural Boundaries)*

```mermaid
flowchart TD
    classDef domain fill:#eff6ff,stroke:#2563eb,stroke-width:1.5px,color:#1e40af,font-weight:bold
    classDef entity fill:#ffffff,stroke:#64748b,stroke-width:1px,color:#0f172a
    classDef ops fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#334155

    subgraph AcademicStructure ["1. Academic Foundation"]
        direction TB
        Org["Institutional Hierarchy<br/>(University / Faculty / Department / Level)"]:::entity
        Time["Academic Time<br/>(Session / Semester)"]:::entity
    end

    subgraph IdentityDomain ["2. Identity & Academic Context"]
        direction TB
        User["User Identity & Verification"]:::entity
        Profile["Academic Profile Claims"]:::entity
        Enroll["Authoritative Enrollment"]:::domain
        User --> Profile --> Enroll
    end

    subgraph CommunityDomain ["3. Community & Governance"]
        direction TB
        Comm["Community & Membership<br/>(Base Community auto-assigned)"]:::domain
        Gov["Governance & Creator Roles<br/>(Publishing Authority)"]:::entity
    end

    subgraph ContentServices ["4. Content & Campus Services"]
        direction TB
        Content["Approved Content<br/>(Announcements, Opps, Events)"]:::entity
        Services["Campus Services & Issues"]:::entity
        Media["Attached Files & Media"]:::entity
        Content --- Media
        Services --- Media
    end

    subgraph PlatformOperations ["5. Cross-Cutting Platform Operations"]
        direction LR
        Search["Search Index"]:::ops
        Sync["Offline Sync State"]:::ops
        Audit["Audit & History"]:::ops
    end

    Org & Time -->|Establishes academic scope| Enroll
    Enroll -->|Derives Base Membership| Comm
    Gov -->|Grants publishing authority in| Comm
    Comm -->|Scopes & hosts| Content
    Comm -->|Scopes & hosts| Services
    Content & Services -.->|Synchronized & Indexed| Search & Sync & Audit
```

### 2.1 Core Conceptual Entities

Lenar relies on the following core conceptual entities. *(Note: This is a domain model, not a physical database schema).*

- **User Identity:** The base authentication persona established via Registration.
- **Academic Profile:** The set of academic claims submitted by the user prior to approval.
- **University / Faculty / Department / Level:** The institutional structural academic organization.
- **Academic Time:** Authoritative tracking of time (Academic Session, Semester).
- **Enrollment:** Establishes the specific academic context of a student (Level, Academic Session, Semester).
- **Community:** Represents participation and belonging. Every active user has a Base Community.
- **Membership:** The relationship denoting participation in a Community. Base Community membership is automatically established from an approved Academic Context.
- **Governance:** Manages Creator Roles, Assignments, Revocation, and Transfer.
- **Announcement / Opportunity / Event / Resource:** Approved informational content distributed to users.
- **Issue / Issue Update:** Structured campus reporting and its resolution history.
- **Notification:** Timely alerts and delivery tracking.
- **File / Media:** Assets attached to primary entities.
- **Audit Event / Revision / Change Metadata:** Tracking who changed what and when.
- **Sync Operation:** Managing offline interactions and state reconciliation.

---

## 3. Data Authority & Representations

A critical boundary in Lenar is the distinction between authoritative state and secondary representations. 

*(Reference Diagram: Data Authority vs. Secondary Representations)*

```mermaid
flowchart TD
    classDef auth fill:#1e3a8a,stroke:#1e40af,stroke-width:2px,color:#ffffff,font-weight:bold
    classDef secondary fill:#f8fafc,stroke:#94a3b8,stroke-width:1.5px,color:#0f172a,font-weight:bold
    classDef client fill:#f0fdf4,stroke:#16a34a,stroke-width:1.5px,color:#14532d,font-weight:bold

    subgraph ServerDomain ["Authoritative Boundary (Backend)"]
        Auth["Authoritative Server State<br/>(PostgreSQL Canonical Truth)"]:::auth
    end

    subgraph Projections ["Secondary Derived Systems"]
        direction TB
        SI["Search Index<br/>(Accelerated Discovery Projection)"]:::secondary
        AT["Analytics & Telemetry<br/>(System Usage Observability)"]:::secondary
        Notif["Push Notifications<br/>(Transient Event Alerts)"]:::secondary
    end

    subgraph MobileClient ["Mobile Client Boundary"]
        direction TB
        Cache["Local Read Cache<br/>(Replicated Authoritative Data)"]:::secondary
        Intent["Local Intent & Drafts<br/>(Pending Sync Mutations)"]:::client
    end

    Auth -->|Filtered Indexing| SI
    Auth -->|Emits Events| AT
    Auth -->|Dispatches Alerts| Notif

    Auth -->|Replicates Down| Cache
    Intent -->|Syncs Up When Online| Auth
```

### 3.1 Essential Distinctions

- **Authoritative Data vs Cache:** The server-side system is authoritative for shared product state unless a specific domain rule establishes another authority.
- **Authoritative Data vs Search Index:** A search index accelerates discovery but is not the authoritative source of truth.
- **Authoritative Data vs Analytics/Telemetry:** Analytics measure system usage; they do not dictate core data state.
- **Authoritative Data vs Notification:** A push notification is a transient alert about data, not the data itself.

### 3.2 The Mobile Local State

Do not treat the local mobile database as "just a cache." While the server remains authoritative for shared state, the mobile client maintains rich local states containing:
- Cached information
- Drafts
- Durable local user intent
- Pending operations
- Synchronization metadata

### 3.3 Ownership vs Authority
Ownership defines who is responsible for the data (e.g., a Department owns its announcements). Authority dictates which system layer possesses the undeniable current state of that data.

### 3.4 Search Behavior
Search must not become an authorization bypass. The conceptual flow remains strict:
```text
Source Data → Indexable Representation → Search → Visibility / Authorization Filtering → Result
```

---

## 4. Content & Data Lifecycle

Information in Lenar is not static. Content transitions through states of visibility, while underlying data follows a broader technical lifecycle.

### 4.1 Content Lifecycle

Content (such as Announcements or Opportunities) experiences a visibility and validation lifecycle.

*(Reference Diagram: Content Visibility & Publishing Lifecycle)*

```mermaid
stateDiagram-v2
    [*] --> Draft: Author creates content

    Draft --> InReview: Submit for approval
    Draft --> Published: Direct publish (authorized role)

    InReview --> Published: Moderator approves
    InReview --> Draft: Changes requested / Rejected

    Published --> Updated: Content edited / revised
    Updated --> Updated: Subsequent revisions

    Published --> Archived: Validity expired / Deprecated
    Updated --> Archived: Validity expired / Deprecated

    Archived --> [*]

    note right of Published
        Active and discoverable in
        targeted community feeds
    end note

    note right of Archived
        Preserved in historical record;
        hidden from active feeds
    end note
```

- **Publication State vs Content Validity:** A draft (publication state) is distinct from an expired notice (content validity).
- **Current State vs Historical State:** The system must distinguish between what is actively applicable today versus what was applicable previously.

### 4.2 Data Lifecycle

At a systemic level, all records proceed through a generalized operational lifecycle.

*(Reference Diagram: Generalized Data Record Lifecycle)*

```mermaid
stateDiagram-v2
    [*] --> Ingestion: Data submitted / collected

    Ingestion --> AuthoritativeStore: Validation passed
    Ingestion --> [*]: Validation failed (rejected)

    AuthoritativeStore --> ActiveUse: Committed to database of record

    ActiveUse --> AuthoritativeStore: Record updated / revision tracked
    ActiveUse --> Archived: Retention policy triggered / Deactivated

    Archived --> Anonymized: PII stripped for analytical retention
    Archived --> Purged: Physical eradication (compliance expiry)

    Anonymized --> [*]
    Purged --> [*]

    note right of ActiveUse
        Available for queries, search
        indexing, and client sync
    end note

    note right of Archived
        Hidden from regular access;
        retained for legal/audit compliance
    end note
```

---

## 5. Files and Attachments

Files are conceptually associated with domain resources rather than existing in a vacuum. 
- **Announcement** → Attachment
- **Issue** → Evidence
- **Opportunity** → Supporting document

The file URL itself is not the authorization boundary. Access to a file is governed by the user's access to the parent resource.

---

## 6. Local Data Persistence Strategy

Not every server resource needs to be mirrored locally. Local persistence decisions are evaluated against:
- User value
- Offline usefulness
- Data sensitivity
- Storage cost on the device
- Required freshness
- Synchronization complexity

---

## 7. Retention and Deletion

Data does not live forever. Lenar preserves the conceptual distinction between:
- **Removal from normal access:** The data is hidden from users but exists operationally.
- **Physical deletion:** The data is securely eradicated.
- **Anonymization:** Identifying traits are stripped for analytical retention.
- **Retention:** Data kept strictly for legitimate audit, legal, or operational reasons.

*(Exact retention periods and legal classifications will be specified in detailed compliance policies).*

---

## Related Documentation

For how this data model connects to the rest of the Lenar system, refer to:

- [02-Problem-Users-Domain.md](02-Problem-Users-Domain.md)
- [03-Product-Requirements.md](03-Product-Requirements.md)
- [07-Security-Privacy-Governance.md](07-Security-Privacy-Governance.md)
- [../architecture/08-Offline-Sync-Resilience.md](../architecture/08-Offline-Sync-Resilience.md)
- [../architecture/09-System-Architecture.md](../architecture/09-System-Architecture.md)
- [../architecture/10-Technology-Stack.md](../architecture/10-Technology-Stack.md)
- [../architecture/11-Performance-Reliability.md](../architecture/11-Performance-Reliability.md)
- [../architecture/13-Analytics-Observability.md](../architecture/13-Analytics-Observability.md)
- [../architecture/14-Infrastructure-Operations.md](../architecture/14-Infrastructure-Operations.md)
- [15-Legal-Business.md](15-Legal-Business.md)
