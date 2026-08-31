# Lenar Documentation

## What is Lenar?
Lenar is an authoritative academic platform designed to handle complex institutional structures, academic progression, grouping, and governance. It provides a secure foundation for user authentication, enrollment, community participation, and authorization, all governed by strict server-side rules.

## Who Should Use These Docs?
These docs are intended for new contributors, partners, engineers, and product designers who need to understand Lenar's purpose, behavior, and technical architecture.

## How to Start (Recommended Reading Path)
**START HERE:**
1. **Foundation & System Model:** Start in `foundation/` to understand the nine domains, how they interact, and the core user journey.
2. **Behavioral Specifications:** Dive into `specifications/` for strict, authoritative rules on state transitions, constraints, and business logic for each domain.
3. **Architecture:** Read through `architecture/` to understand the technical stack, infrastructure, and offline capabilities.
4. **Decisions & Historical Material:** Review `decisions/` for technical rationale, and `archive/` for historical audits.

## Documentation Layers & Source of Truth

**1. Behavioral Domain Truth (Absolute Authority)**
- Location: `specifications/`
- Purpose: The nine behavioral specifications are the undeniable source of truth for their respective domains (Account Lifecycle, Enrollment, Governance, etc.).

**2. System Overview (Orientation)**
- Location: `foundation/`
- Purpose: High-level maps, master user journeys, and relationships linking the nine domains.

**3. Product & Strategy**
- Location: `product/`
- Purpose: Original product vision, UX, requirements, and legal/business constraints.

**4. Engineering & Architecture**
- Location: `architecture/`
- Purpose: Technical implementation, system architecture, performance, testing, and operational constraints.

**5. Decisions & Risk**
- Location: `decisions/`
- Purpose: Architectural decision records, risks, and project evolution.

**6. Historical Archive**
- Location: `archive/`
- Purpose: Historical audit reports, propagation logs, and Phase-B work.
