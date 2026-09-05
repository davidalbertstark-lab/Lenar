# Lenar — Platform & Experience Strategy

> [!NOTE]  
> **Purpose:** Defines the physical boundaries, application layers, and separation of concerns across the Lenar platform.  
> **Prerequisites:** `../03-specifications/README.md`  
> **Primary Audience:** Backend Engineers, Mobile Engineers, Architects.



---

## At a Glance

Lenar is a multi-platform product. It is not one interface copied onto several devices.

The product should preserve the same underlying meaning, rules, and user outcomes while allowing each platform to use interaction patterns appropriate to its environment.

The current platform strategy is:

| Platform | Primary Role | Current Direction |
|---|---|---|
| **Web** | Broad access, productivity, management | React + TypeScript + Vite |
| **PWA** | Installable/lightweight web access | Web application with appropriate PWA capabilities |
| **Android** | Primary mobile student experience | Flutter |
| **iOS** | Mobile student experience | Flutter |

The key platform principle is:
> **Shared product semantics, platform-appropriate experience.**

This means Lenar should not become four different products. At the same time, Android, iOS, Web, and PWA should not be forced into identical layouts or interaction patterns merely for the sake of consistency.

---

## 1. Why a Multi-Platform Strategy?

Students and other Lenar users will access the system through different devices and contexts. Some may use:
- Android phones
- iPhones
- Laptops
- Desktop computers
- Browser-based access
- Installed PWAs

The product therefore needs more than a single access surface. The platform strategy exists to answer:
> **What should Lenar provide on each platform, and what should remain common across all of them?**

---

## 2. Platform Philosophy

Lenar follows core platform principles designed to unify the experience while respecting the medium.

### 2.1 One Product

Users should experience:
> **one Lenar**

rather than unrelated applications that happen to use the same brand. The underlying concepts, terminology, account model, permissions, and product semantics should remain strictly aligned.

### 2.2 Platform-Appropriate Experience

Shared meaning does not require identical interaction.

```text
Web
→ keyboard/mouse-oriented interaction

Mobile
→ touch-first interaction

PWA
→ browser-first experience with installable capabilities
```

### [Shared Product Semantics vs. Platform-Appropriate Experience]

```mermaid
flowchart TD
    classDef shared fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#14532d
    classDef platform fill:#fffbeb,stroke:#d97706,stroke-width:2px,color:#78350f
    classDef item fill:#ffffff,stroke:#94a3b8,stroke-width:1px,color:#0f172a

    subgraph SharedLayer ["Shared Product Layer (Consistent Across All Platforms)"]
        direction TB
        S1["Domain Semantics & Consistent Terminology"]:::item
        S2["Identity, Account Model & Permissions"]:::item
        S3["Authoritative Data Meaning & Workflows"]:::item
    end

    subgraph PlatformLayer ["Platform-Specific Layer (Adapted to Device Context)"]
        direction TB
        P1["Interaction Mode (Mouse/Keyboard vs. Touch)"]:::item
        P2["Navigation & UI Layout (Responsive vs. Native Shell)"]:::item
        P3["Device APIs, Lifecycle & Distribution Channels"]:::item
    end

    SharedLayer -->|"Informs and governs"| PlatformLayer
```

---

## 3. Platform Map & Roles

Lenar branches into dedicated platforms to best serve the user's immediate context. 

### [Platform Map and Experience Roles]

```mermaid
flowchart TD
    classDef core fill:#2563eb,stroke:#1e40af,stroke-width:2px,color:#ffffff,font-weight:bold
    classDef client fill:#eff6ff,stroke:#3b82f6,stroke-width:1px,color:#1e40af

    Core["Lenar Unified Core<br/>(Shared Domain Semantics & APIs)"]:::core

    subgraph WebSurface ["Web Platform (React + TypeScript + Vite)"]
        direction TB
        Web["Web Portal<br/>(Broad Access, Management & Productivity)"]:::client
        PWA["PWA<br/>(Lightweight Installable Experience)"]:::client
    end

    subgraph MobileSurface ["Mobile Platform (Flutter + Dart)"]
        direction TB
        Android["Android Client<br/>(Primary Student Experience)"]:::client
        IOS["iOS Client<br/>(Mobile Student Experience)"]:::client
    end

    Core -->|"Web Client Shell"| WebSurface
    Core -->|"Native Mobile App"| MobileSurface
```

---

## 4. Current Mobile Strategy

The current mobile strategy relies on **Flutter + Dart** to build the Android and iOS experiences. 

While Kotlin Multiplatform + Native UI was a serious alternative during the evaluation process, Flutter currently provides the strongest overall trade-off for Lenar's present mobile requirements. 

It is important to emphasize that framework choices are driven by product requirements, maintenance cost, and capability needs—not technology preference. 

---

## 5. Platform Lifecycle

The lifecycle of the application varies significantly by platform. For example, mobile app lifecycles (App Store distribution, strict updates) differ mechanically from Browser/PWA lifecycles (continuous deployment, immediate updates).

### [Platform Application Lifecycle States]

```mermaid
stateDiagram-v2
    [*] --> Installed : App Store download or Web visit
    Installed --> Initializing : First launch & bootstrapping
    Initializing --> ActiveSession : Setup & authentication complete

    state ActiveSession {
        [*] --> Running
        Running --> Updating : Store release or Web deploy
        Updating --> Migrating : Local schema / cache migration
        Migrating --> Running : Migration complete
    }

    ActiveSession --> Initializing : Session reset / Re-authentication
    ActiveSession --> Terminated : App uninstall or storage clear
    Terminated --> [*]
```

---

## 6. Platform Decision Flow

When introducing new features or capabilities, the decision of how to implement them on a platform is guided by a structured evaluation of product needs against platform reality.

### [Platform Capability Decision Pipeline]

```mermaid
flowchart TD
    classDef step fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a
    classDef decision fill:#2563eb,stroke:#1e40af,stroke-width:2px,color:#ffffff,font-weight:bold
    classDef outcome fill:#f0fdf4,stroke:#16a34a,stroke-width:1px,color:#14532d

    UN["1. User Need & Desired Outcome"]:::step
    R["2. Product Requirement & Semantics"]:::step
    PC["3. Platform Capability & Constraints"]:::step
    SP["4. Security, Privacy & Server Authority"]:::step
    P["5. Performance & Device Budget"]:::step
    MC["6. Maintenance Cost & Code Boundaries"]:::step
    
    PD{"Platform Decision"}:::decision
    
    O1["Shared Implementation<br/>(Unified Web & Mobile)"]:::outcome
    O2["Platform-Specific Adaptation<br/>(Form-factor specialized UX/API)"]:::outcome
    O3["Graceful Fallback<br/>(Degraded mode if unsupported)"]:::outcome

    UN --> R
    R --> PC
    PC --> SP
    SP --> P
    P --> MC
    MC --> PD
    
    PD -->|"Standard capability"| O1
    PD -->|"Divergent form-factor"| O2
    PD -->|"Unsupported on surface"| O3
```

---

## 7. Platform Content Rules

The following rules govern how features should be approached across platforms:

1. **One Product:** Lenar is one product across multiple platforms.
2. **Semantics:** Shared semantics do not require identical interfaces.
3. **Mobile Framework:** Flutter is the current mobile framework decision.
4. **Adaptation:** Platform-specific behavior is appropriate where platform differences materially affect usability or capability.
5. **Permissions:** Permissions should be contextual and minimal.
6. **Graceful Degradation:** Unsupported capabilities need defined fallback/limitation behavior.
7. **Authority:** Server-side authorization remains authoritative on every client.
8. **Boundaries:** Platform differences should be concentrated in appropriate boundaries rather than scattered throughout the application logic.
9. **Validation:** Platform support must be tested on actual representative environments.
10. **Constraints:** Low-end device constraints are highly relevant to the platform strategy.

---

## Related Documentation

For detailed specifications connected to this platform strategy, refer to the following canonical documents:

- [../product/03-Product-Requirements.md](../01-user-requirements/03-Product-Requirements.md)
- [../product/04-UX-UI.md](../01-user-requirements/04-UX-UI.md)
- [../product/06-Data-Content.md](../01-user-requirements/06-Data-Content.md)
- [../product/07-Security-Privacy-Governance.md](../01-user-requirements/07-Security-Privacy-Governance.md)
- [08-Offline-Sync-Resilience.md](08-Offline-Sync-Resilience.md)
- [09-System-Architecture.md](09-System-Architecture.md)
- [10-Technology-Stack.md](10-Technology-Stack.md)
- [11-Performance-Reliability.md](11-Performance-Reliability.md)
- [12-Testing-Quality.md](12-Testing-Quality.md)
- [../product/15-Legal-Business.md](../01-user-requirements/15-Legal-Business.md)
- [16-Development-Release.md](16-Development-Release.md)
- [../decisions/17-Decisions-Risks-Evolution.md](../decisions/17-Decisions-Risks-Evolution.md)
