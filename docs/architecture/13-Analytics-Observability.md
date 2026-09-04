# Lenar — Analytics & Observability

> **Status:** Analytics & Observability Reference  
> **Document:** 13 — Analytics & Observability  
> **Purpose:** Define how Lenar measures product usage, system behavior, performance, errors, reliability, and operational health while maintaining appropriate privacy boundaries and keeping measurement systems separate from authoritative product state.

---

## At a Glance

Lenar needs to know two different things:
> **Are people getting value from the product?**
> **Is the system itself working correctly and reliably?**

These are related, but they are not the same question.

### Product Analytics
Helps us understand what users do, which features are useful, where workflows are abandoned, and whether important product outcomes are occurring over time.

### Observability
Helps us understand whether services are healthy, where requests fail, how long operations take, whether infrastructure is overloaded, and what happened during an incident.

The central principle is:
> **Measure enough to make good decisions, but never collect information merely because it can be collected.**

Analytics and observability are supporting systems. They must never become the authoritative source of product truth, authorization, user identity, security decisions, or transactional correctness.

---

## 1. Measurement Philosophy

Measurement exists to reduce uncertainty. A useful measurement should help answer:
```text
What happened?
Why does it matter?
What decision could this information improve?
```

---

## 2. The Measurement Model

Lenar cleanly separates the measurement of product behavior from the measurement of application and infrastructure health.

### [Measurement Domain Separation]

```mermaid
flowchart LR
    classDef source fill:#f8fafc,stroke:#64748b,stroke-width:1px,color:#0f172a,font-weight:bold
    classDef signal fill:#eff6ff,stroke:#3b82f6,stroke-width:1px,color:#1e40af
    classDef system fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#14532d,font-weight:bold

    subgraph ProductDomain ["1. Product Domain"]
        direction LR
        P["User & Feature Activity"]:::source --> PE["Product Events<br/>(Outcomes & Funnels)"]:::signal --> PA["Product Analytics<br/>(PostHog)"]:::system
    end

    subgraph AppDomain ["2. Application Domain"]
        direction LR
        APP["FastAPI Monolith & Services"]:::source --> LMTE["Logs, Metrics, Traces & Errors"]:::signal --> OB["Observability<br/>(OpenTelemetry & Sentry)"]:::system
    end

    subgraph InfraDomain ["3. Infrastructure Domain"]
        direction LR
        INFRA["Hosting & Database Systems"]:::source --> HRS["Health & Resource Signals<br/>(CPU, Memory, Connections)"]:::signal --> OM["Operational Monitoring"]:::system
    end
```

---

## 3. Product Analytics

Lenar uses **PostHog** for product analytics. 

### 3.1 Event Semantics & Outcomes
Events should represent meaningful product behavior tied to outcomes, not transient UI states. We prefer outcome-oriented measurement over vanity metrics.

| Good Analytics Event | Bad Analytics Event |
|---|---|
| `issue_created` | `button_4_clicked` |
| `announcement_viewed` | `screen_2_opened` |
| `search_performed` | `text_field_focused` |

### 3.2 Onboarding Measurement
Analytics may later measure meaningful onboarding outcomes such as: registration started, verification completed, profile submitted, review completed, approved, rejected, resubmitted, and active. However, analytics do NOT become authoritative for Enrollment, Authorization, Account state, or Community membership.

### 3.3 Analytics Flow and Failure
Analytics explicitly do not modify the authoritative state of the product. 

### [Analytics Flow and Failure Isolation]

```mermaid
flowchart TD
    classDef user fill:#fef3c7,stroke:#d97706,stroke-width:1px,color:#92400e,font-weight:bold
    classDef auth fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#14532d,font-weight:bold
    classDef analytics fill:#eff6ff,stroke:#3b82f6,stroke-width:1px,color:#1e40af
    classDef boundary fill:#f8fafc,stroke:#cbd5e1,stroke-width:1px,color:#475569

    UA["User Action<br/>(e.g., Submit Issue)"]:::user

    subgraph AuthoritativePath ["Authoritative Execution (Guaranteed Core Flow)"]
        direction TB
        APP["FastAPI Application Logic"]:::auth --> DB[("Authoritative Database State")]:::auth
    end

    subgraph AnalyticsPath ["Telemetry Pipeline (Non-Blocking & Asynchronous)"]
        direction TB
        PE["Product Event<br/>(Fire-and-Forget Emission)"]:::analytics --> PH["PostHog Analytics"]:::analytics
        PH --> INS["Insights & Product Decisions"]:::analytics
    end

    UA ==>|Synchronous Mutation| APP
    UA -.->|Asynchronous Event| PE

    subgraph IsolationPrinciple ["Decoupled Failure Boundary"]
        direction TB
        ISO["Analytics failure never blocks or corrupts authoritative state.<br/>If PostHog is unavailable, the user action still succeeds."]:::boundary
    end

    AnalyticsPath ~~~ IsolationPrinciple
```

**Analytics failure must never be a dependency for core product correctness.** 
If PostHog is unavailable, the analytics signal is degraded, but the authoritative user action (e.g., submitting an issue) must still succeed.

---

## 4. Observability

Lenar uses **Sentry** for error monitoring and **OpenTelemetry** for application telemetry (metrics, traces, and logs).

Observability focuses on system behavior and diagnostic detection. Similar to analytics, observability failure reduces visibility but must not corrupt or block the authoritative product state.

### [Observability Lifecycle and Diagnostic Flow]

```mermaid
flowchart TD
    classDef runtime fill:#f8fafc,stroke:#64748b,stroke-width:1px,color:#0f172a,font-weight:bold
    classDef telemetry fill:#eff6ff,stroke:#3b82f6,stroke-width:1px,color:#1e40af
    classDef platform fill:#fef3c7,stroke:#d97706,stroke-width:1px,color:#92400e,font-weight:bold
    classDef action fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#14532d,font-weight:bold

    subgraph RuntimeExecution ["1. Runtime Execution"]
        APP["Application & Infrastructure Runtime<br/>(FastAPI Monolith, Database, Background Workers)"]:::runtime
    end

    subgraph TelemetryCapture ["2. Telemetry Capture"]
        direction LR
        OTEL["OpenTelemetry<br/>(Metrics, Distributed Traces, Logs)"]:::telemetry
        SENTRY["Sentry<br/>(Exceptions & Error Context)"]:::telemetry
    end

    subgraph Analysis ["3. Detection & Diagnosis"]
        direction TB
        AGG["Signal Aggregation & Threshold Alerting"]:::platform
        DD["Root Cause Analysis & Bottleneck Identification"]:::platform
        AGG --> DD
    end

    subgraph Outcome ["4. Operational Resolution"]
        OA["Operational Action<br/>(Mitigation, Code Fix, Scaling)"]:::action
    end

    APP -->|Emits Telemetry| OTEL
    APP -->|Captures Exceptions| SENTRY
    OTEL --> AGG
    SENTRY --> AGG
    DD --> OA
```

---

## 5. Critical Distinctions

A correct mental model of Lenar telemetry preserves these conceptual boundaries:

- **PRODUCT ANALYTICS ≠ OBSERVABILITY**
- **ANALYTICS ≠ AUTHORITATIVE PRODUCT STATE**
- **OBSERVABILITY ≠ AUTHORITATIVE PRODUCT STATE**
- **ANALYTICS ≠ AUTHORIZATION**
- **OBSERVABILITY ≠ AUTHORIZATION**
- **LOGS ≠ AUDIT RECORDS**
- **METRICS ≠ RAW EVENTS**
- **TRACES ≠ PRODUCT ANALYTICS**
- **ERROR MONITORING ≠ PRODUCT ANALYTICS**
- **NOTIFICATION DELIVERY ≠ AUTHORITATIVE STATE**

---

## 6. Privacy & Data Collection

We collect the minimum useful information needed to answer important questions. We do not "track everything."

**We do NOT automatically send:**
- Complete user profiles with every event
- Passwords, credentials, or tokens
- Raw search queries
- Unredacted issue descriptions
- Uploaded file content
- Highly sensitive device/personal information

### 6.1 Retention & Access
Data retention is determined according to usefulness, cost, privacy, security, and legal/operational requirements rather than an infinite default. Production analytics and observability data are protected by least-privilege access, as they can reveal user behavior and security signals.

---

## 7. Metrics & Incident Correlation

Operational metrics capture system dimensions such as request rate, latency, error rate, resource use, queue depth, queue age, database performance, sync health, and overall availability.

During an incident, traces and correlation identifiers connect these technical signals back to actual user impact.

### [Incident Signal Correlation and Recovery Flow]

```mermaid
flowchart TD
    classDef signal fill:#eff6ff,stroke:#3b82f6,stroke-width:1px,color:#1e40af
    classDef change fill:#fef3c7,stroke:#d97706,stroke-width:1px,color:#92400e
    classDef correlation fill:#ede9fe,stroke:#8b5cf6,stroke-width:1px,color:#5b21b6,font-weight:bold
    classDef assess fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#0369a1,font-weight:bold
    classDef recovery fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#14532d,font-weight:bold

    subgraph DiscoveredSignals ["1. Observed Signals"]
        direction LR
        SYS["System Telemetry<br/>(Logs, Metrics, Traces, Sentry Errors)"]:::signal
        CHG["Change Events<br/>(Deployments, Migrations & Config Releases)"]:::change
    end

    subgraph ContextEngine ["2. Correlation Context"]
        CORR["Trace IDs & Request Correlation<br/>(Links technical anomalies directly to affected user workflows)"]:::correlation
    end

    subgraph IncidentAssessment ["3. Incident Understanding"]
        IU["Incident Understanding<br/>(Technical Root Cause & True Product Impact)"]:::assess
    end

    subgraph Recovery ["4. Operational Recovery"]
        AR["Targeted Recovery Action<br/>(Rollback, Hotfix, Failover, or Rate-Limit)"]:::recovery
    end

    SYS --> CORR
    CHG --> CORR
    CORR --> IU
    IU --> AR
```

---

## 8. Alerts & Dashboards

### 8.1 Alerts
Alerts must be actionable. We avoid alerting on every minor warning, noisy thresholds, or conditions that no human needs to respond to. Alert fatigue is an operational failure.

### 8.2 Dashboards
Dashboards are conceptually separated by their audience and purpose. An infrastructure dashboard monitoring PostgreSQL connections should remain distinct from a product dashboard measuring daily active students.

---

## 9. The Combined Model

Product use and system health provide parallel paths toward the same goal: **Lenar Improvement.**

### [Dual-Track Improvement Model: Product Experience and System Reliability]

```mermaid
flowchart TD
    classDef product fill:#eff6ff,stroke:#3b82f6,stroke-width:1px,color:#1e40af,font-weight:bold
    classDef system fill:#fef3c7,stroke:#d97706,stroke-width:1px,color:#92400e,font-weight:bold
    classDef goal fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#14532d,font-weight:bold

    subgraph ProductTrack ["Product Experience Track"]
        direction TB
        PU["Product Usage<br/>(Student Workflows & Features)"]:::product
        PA["Product Analytics<br/>(PostHog Outcomes & Funnels)"]:::product
        PI["Product Insights<br/>(Feature Utility & Abandonment)"]:::product
        P_ACT["Product Action<br/>(UX Improvements & Hypothesis Iteration)"]:::product

        PU --> PA --> PI --> P_ACT
    end

    subgraph SystemTrack ["System Reliability Track"]
        direction TB
        SH["System Health<br/>(Services, DB & Background Queues)"]:::system
        OB["Observability<br/>(OpenTelemetry & Sentry Signals)"]:::system
        DD["Detection & Diagnosis<br/>(Latency, Errors & Bottlenecks)"]:::system
        S_ACT["Operational Action<br/>(Optimization, Bugfixes & Scaling)"]:::system

        SH --> OB --> DD --> S_ACT
    end

    GOAL(["Continuous Lenar Improvement<br/>(Higher Student Value + Dependable System Operation)"]):::goal

    P_ACT ==> GOAL
    S_ACT ==> GOAL
```

### 9.1 Experiments & Feature Flags
When evaluating improvements via experimentation, the process requires a formal hypothesis, defined audience, success metric, explicit duration, safety boundary, and clear rollback conditions. Feature flags must have an owner and a review/expiry discipline to prevent permanent technical debt.

### 9.2 Analytics Testing
Analytics instrumentation is code and must be tested. Tests should verify that the correct event fires, incorrect events do not fire, required properties exist, and sensitive properties are explicitly absent.

---

## Related Documentation

- [../product/03-Product-Requirements.md](../01-user-requirements/03-Product-Requirements.md)
- [../product/04-UX-UI.md](../01-user-requirements/04-UX-UI.md)
- [../product/06-Data-Content.md](../01-user-requirements/06-Data-Content.md)
- [../product/07-Security-Privacy-Governance.md](../01-user-requirements/07-Security-Privacy-Governance.md)
- [08-Offline-Sync-Resilience.md](08-Offline-Sync-Resilience.md)
- [09-System-Architecture.md](09-System-Architecture.md)
- [10-Technology-Stack.md](10-Technology-Stack.md)
- [11-Performance-Reliability.md](11-Performance-Reliability.md)
- [12-Testing-Quality.md](12-Testing-Quality.md)
- [14-Infrastructure-Operations.md](14-Infrastructure-Operations.md)
- [../product/15-Legal-Business.md](../01-user-requirements/15-Legal-Business.md)
- [16-Development-Release.md](16-Development-Release.md)
- [../decisions/17-Decisions-Risks-Evolution.md](../decisions/17-Decisions-Risks-Evolution.md)
