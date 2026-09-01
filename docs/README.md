# Lenar Documentation

## What is Lenar?
Lenar is a platform built for university students to connect, stay informed, and participate in their academic community. It uses a student's verified academic information to provide the right experience, ensuring secure and correct access to university resources, departments, and communities.

## Who Should Use These Docs?
These docs are intended for new contributors, partners, engineers, and product designers who need to understand Lenar's purpose, behavior, and technical design.

## How to Start (Recommended Reading Path)
**START HERE:**
1. **Foundation & System Model:** Start in `foundation/` to understand the nine domains, how they interact, and the core user journey.
2. **Behavioral Specifications:** Dive into `specifications/` for strict, authoritative rules on state transitions, constraints, and business logic for each domain.
3. **Architecture:** Read through `architecture/` to understand the technical stack, infrastructure, and offline capabilities.
4. **Decisions & Historical Material:** Review `decisions/` for technical rationale.

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
