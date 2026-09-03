# Lenar — Performance & Reliability

> **Status:** Performance & Reliability Reference  
> **Document:** 11 — Performance & Reliability  
> **Purpose:** Define how well Lenar is expected to perform, how the system should behave under constrained conditions, what performance and reliability characteristics matter across platforms and services, how capacity should be approached, and how measurable evidence should guide optimization and scaling.

---

## At a Glance

Lenar should feel fast, responsive, dependable, efficient, and resilient even on imperfect networks and devices. 

Performance is not simply about making everything as fast as technically possible, and reliability is not simply about keeping servers online. For Lenar, the real objective is:
> **Deliver a responsive and dependable experience while preserving correctness under realistic university conditions.**

Those conditions routinely include low-end devices, weak or intermittent connectivity, temporary service failures, and large bursts of usage.

---

## 1. Critical Principles

All engineering work must observe these baseline performance and reliability rules:

1. **Measure before optimizing.**
2. **Optimize end-to-end,** not based on assumptions about where the bottleneck exists.
3. **Performance must not compromise correctness.**
4. **Performance must not compromise authorization.**
5. **Performance must not compromise data integrity.**
6. **Lenar must account for low-end devices and imperfect networks.**
7. **Reliability includes correctness, durability, recoverability, and observability**—not only uptime.
8. **Supporting-service failures should not automatically invalidate core authoritative operations.**
9. **Scaling should be incremental and evidence-driven.**
10. **More infrastructure does not automatically mean more reliability.**
11. **Tail latency matters;** averages alone are insufficient where appropriate.
12. **Exact numerical budgets should not be invented before they are validated.**

---

## 2. Performance Dimensions

Performance cannot be treated as a single metric. Lenar evaluates performance across these distinct dimensions:

- **Latency:** How long an operation takes.
- **Throughput:** How many operations complete in a period.
- **Responsiveness:** How quickly the UI acknowledges input.
- **Startup Time:** Time from launch to usable state.
- **Resource Usage:** CPU, RAM, battery, and storage consumption.
- **Stability:** Predictability of performance under load.
- **Scalability:** The ability to handle growing workloads gracefully.
- **Recovery Time:** How quickly the system returns to normal after constraint or failure.

### 2.1 End-to-End Performance Focus
Optimization must reflect the true user experience, evaluating the complete journey through the stack.

#### End-to-End Latency Path Across the Stack

```mermaid
flowchart TD
    classDef client fill:#eff6ff,stroke:#3b82f6,stroke-width:1px,color:#1e40af
    classDef network fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#334155,stroke-dasharray: 4 4
    classDef server fill:#f0fdf4,stroke:#16a34a,stroke-width:1px,color:#166534
    classDef terminal fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e,font-weight:bold

    subgraph ClientTier["Client Tier (Device)"]
        U(["User Action / Input"]):::terminal --> UI["UI Event Handling"]:::client
        UI --> CP["Client Processing & Local State"]:::client
    end

    subgraph NetworkTier["Network Layer"]
        CP --> NW["Network Request Transit<br/><i>(Latency, Flakiness, Bandwidth)</i>"]:::network
    end

    subgraph ServerTier["Backend Tier (Server)"]
        NW --> API["API Routing & Authorization"]:::server
        API --> APP["Application Domain Logic"]:::server
        APP --> DB[("Authoritative Database & Storage")]:::server
        APP -.->|Secondary| EXT["External Providers"]:::server
    end

    subgraph ReturnTier["Response & Perception"]
        DB --> RES["Response Serialization & Downlink"]:::network
        EXT -.-> RES
        RES --> RENDER["Client Render & Visual Feedback"]:::terminal
    end
```

---

## 3. Reliability Dimensions

Reliability is significantly broader than uptime. A system can be reachable but incorrect, or it can temporarily lose availability while preserving user intent securely. 

- **Availability:** The system is reachable and responding.
- **Correctness:** The system behaves according to its domain rules.
- **Durability:** Committed data is safely preserved against loss.
- **Recoverability:** The system can restore itself from a failure state.
- **Consistency:** Operations observe the correct logical sequence of data.
- **Failure Handling:** The system degrades gracefully when components break.
- **Observability:** Operators can accurately determine system health.

#### Core Dimensions of System Reliability

```mermaid
flowchart TD
    classDef root fill:#1e293b,color:#fff,stroke:#0f172a,stroke-width:2px,font-weight:bold
    classDef pillar fill:#f1f5f9,stroke:#475569,stroke-width:2px,color:#0f172a,font-weight:bold
    classDef integrity fill:#eff6ff,stroke:#3b82f6,stroke-width:1px,color:#1e40af
    classDef resilience fill:#f0fdf4,stroke:#16a34a,stroke-width:1px,color:#166534
    classDef visibility fill:#fef3c7,stroke:#d97706,stroke-width:1px,color:#92400e

    RS["<b>Reliable System</b><br/><i>Performance & Trust Beyond Simple Uptime</i>"]:::root

    RS --> P1["<b>Data & Domain Integrity</b>"]:::pillar
    RS --> P2["<b>Operational Resilience</b>"]:::pillar
    RS --> P3["<b>Operational Visibility</b>"]:::pillar

    P1 --> C["<b>Correctness</b><br/>Domain & authorization rules enforced"]:::integrity
    P1 --> CS["<b>Consistency</b><br/>Logical sequence of state maintained"]:::integrity
    P1 --> D["<b>Durability</b><br/>Committed data safely preserved"]:::integrity

    P2 --> A["<b>Availability</b><br/>Reachable & responsive to requests"]:::resilience
    P2 --> FH["<b>Failure Handling</b><br/>Graceful degradation on dependency failure"]:::resilience
    P2 --> REC["<b>Recoverability</b><br/>Rapid restoration after outage"]:::resilience

    P3 --> O["<b>Observability</b><br/>Actionable telemetry to assess system health"]:::visibility
```

> [!WARNING]
> AVAILABLE ≠ CORRECT ≠ RESILIENT

---

## 4. Real-World Constraints

### 4.1 Mobile / Low-End Devices
Performance must be evaluated on representative real-world devices, not solely developer hardware. Key factors include RAM, CPU, storage, GPU limitations, thermal throttling, battery life, and background execution limits.

### 4.2 Network
The system must gracefully handle fast, slow, high-latency, intermittent, and completely offline network conditions. See [08-Offline-Sync-Resilience.md](08-Offline-Sync-Resilience.md) for detailed resilience behavior.

---

## 5. Component-Specific Constraints

- **Database (PostgreSQL):** Approached through query latency, proper indexing, bounded transaction duration, pagination, and predictable connection utilization.
- **Search:** Search performance must remain strictly subject to authorization. We never bypass security rules to make a search faster.
- **Files / Object Storage:** Evaluated by payload size, streaming viability, and bandwidth optimization.
- **Synchronization:** Evaluated by sync latency, queue age, queue throughput, and payload efficiency.

---

## 6. Dependency Failure

The reliability model dictates that failures in secondary systems must be isolated from the core authoritative transaction:
- **Analytics failure** → Analytics unavailable → *Core operation remains valid.*
- **Notification failure** → Delivery affected → *Authoritative state remains valid.*
- **Search delay** → Search representation delayed → *Source of truth remains authoritative.*

---

## 7. Optimization & Scaling Models

### 7.1 Optimization
Optimization must follow a strictly evidence-driven loop.

#### Evidence-Driven Optimization Workflow

```mermaid
flowchart TD
    classDef step fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a
    classDef action fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e40af,font-weight:bold
    classDef decision fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e,font-weight:bold
    classDef terminal fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#166534,font-weight:bold

    Start(["Performance Goal / Degradation Detected"]):::terminal --> Obs["<b>1. Observe</b><br/>Monitor real-world symptoms & telemetry"]:::step
    Obs --> Measure["<b>2. Measure Baseline</b><br/>Profile latency, CPU, queries & network"]:::action
    Measure --> Bottleneck["<b>3. Identify Bottleneck</b><br/>Pinpoint the true constraint"]:::step
    Bottleneck --> Impact["<b>4. Estimate Impact</b><br/>Weigh projected gain against complexity"]:::step
    Impact --> Optimize["<b>5. Apply Simplest Fix</b><br/>Minimal effective change <i>(e.g., index, cache, pagination)</i>"]:::action
    Optimize --> Remeasure["<b>6. Measure Again</b><br/>Collect post-change metrics under load"]:::action

    Remeasure --> Eval{"Target Met &<br/>Correctness Preserved?"}:::decision

    Eval -->|No: Insufficient gain| Measure
    Eval -->|Yes: Evidence verified| Complete(["Deploy & Document Baseline"]):::terminal
```

### 7.2 Scaling
Do not introduce microservices, Kubernetes, message brokers, or specialized search engines merely because they could theoretically improve scale.

#### Evidence-Based Scaling Decision Process

```mermaid
flowchart TD
    classDef input fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a
    classDef decision fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e,font-weight:bold
    classDef action fill:#eff6ff,stroke:#3b82f6,stroke-width:1px,color:#1e40af
    classDef outcome fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#166534,font-weight:bold
    classDef reject fill:#fef2f2,stroke:#dc2626,stroke-width:2px,color:#991b1b,font-weight:bold

    Demand["<b>1. Increased Demand</b><br/>Workload, throughput, or user growth"]:::input --> Measure["<b>2. Measure Bottleneck</b><br/>Telemetry confirms physical limit"]:::input
    
    Measure --> LimitCheck{"Can Current Stack<br/>Handle with Tuning?"}:::decision
    
    LimitCheck -->|Yes: Tuning viable| Tune["<b>Optimize In-Place</b><br/>Tune queries, add indexes, or configure pooling"]:::action
    
    LimitCheck -->|No: Physical ceiling reached| Candidate["<b>3. Formulate Candidate Solution</b><br/>Identify simplest architectural step"]:::action
    
    Candidate --> Tradeoff{"Does Benefit Outweigh<br/>Added Complexity & Cost?"}:::decision
    
    Tradeoff -->|No: Premature complexity| Reject["<b>Reject / Defer Expansion</b><br/>Avoid microservices, brokers, or K8s without evidence"]:::reject
    
    Tradeoff -->|Yes: Justified by evidence| Adopt["<b>Adopt Simplest Scale Step</b><br/>Implement minimal viable scaling tier"]:::outcome
```

---

## 8. Service Level Objectives (SLOs) & Budgets

*(Note: Final numerical targets for latency, availability, battery utilization, RTO, and RPO will be established after representative measurement on production-grade infrastructure).*

---

## Related Documentation

- [../product/03-Product-Requirements.md](../product/03-Product-Requirements.md)
- [../product/04-UX-UI.md](../product/04-UX-UI.md)
- [05-Platform.md](05-Platform.md)
- [../product/06-Data-Content.md](../product/06-Data-Content.md)
- [../product/07-Security-Privacy-Governance.md](../product/07-Security-Privacy-Governance.md)
- [08-Offline-Sync-Resilience.md](08-Offline-Sync-Resilience.md)
- [09-System-Architecture.md](09-System-Architecture.md)
- [10-Technology-Stack.md](10-Technology-Stack.md)
- [12-Testing-Quality.md](12-Testing-Quality.md)
- [13-Analytics-Observability.md](13-Analytics-Observability.md)
- [14-Infrastructure-Operations.md](14-Infrastructure-Operations.md)
- [16-Development-Release.md](16-Development-Release.md)
- [../decisions/17-Decisions-Risks-Evolution.md](../decisions/17-Decisions-Risks-Evolution.md)
