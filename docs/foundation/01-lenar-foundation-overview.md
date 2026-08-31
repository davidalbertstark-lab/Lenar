# Lenar Foundation Overview

## What is Lenar Trying to Build?
Lenar is a comprehensive platform designed to model, manage, and facilitate the complex realities of academic institutional life. It provides a structured environment where users are securely authenticated, their academic identities are established through authoritative enrollment, and they are organized into communities reflecting their real-world academic contexts.

Lenar is built to solve the systemic problem of fragmented institutional contexts. Rather than relying on isolated systems for authentication, community grouping, and role-based authority, Lenar unifies these into a single, cohesive foundation where institutional truth (Organization, Academic Time, Enrollment) drives downstream participation (Community) and authority (Governance, Authorization).

## The Product Model
The system operates on a core set of principles defined in the canonical documentation:
- **Server Authority:** Institutional structures and academic truths are strictly server-authoritative. The client is considered an untrusted interface.
- **University-Relative Context:** Lenar natively models the reality that different institutions have different structures and calendars. It avoids imposing a single, rigid, universal academic hierarchy.
- **Separation of Concerns:** To prevent monolithic complexity, Lenar divides its core logic into nine distinct domains (e.g., Account Lifecycle, Organization, Governance). Each domain owns a specific piece of the truth, and they interact through well-defined boundaries.
- **Historical Preservation:** Changes in current status—such as an organizational rename or academic progression—do not silently rewrite past context. Historical truth is protected.
- **Offline Resilience:** The architecture anticipates unreliable connectivity, allowing safe client-side caching and UX continuity without sacrificing authoritative server-side state evaluation.

## Canonical References
To explore the broader purpose, architecture, and requirements that drove this foundation, refer to the root canonical documents:
- [01 Lenar Foundation](../product/01-Lenar-Foundation.md)
- [02 Problem, Users & Domain](../product/02-Problem-Users-Domain.md)
- [03 Product Requirements](../product/03-Product-Requirements.md)
- [07 Security, Privacy & Governance](../product/07-Security-Privacy-Governance.md)
