# Lenar Specifications

## What this directory is
This directory contains the detailed behavioral specifications for important Lenar capabilities. It bridges the gap between the high-level canonical domain documentation and the actual implementation.

## What it is not
It is explicitly not:
- the canonical foundation;
- an ADR repository;
- source code;
- a database schema repository;
- an API-only documentation repository.

## Authority Relationship
Lenar's documentation and implementation follow a strict hierarchy of authority:
- **Canonical Docs** → define product identity, domain meaning, established architectural intent, major boundaries, and foundational principles.
- **Specifications** → define detailed behavior, states, rules, constraints, and acceptance criteria within that intent.
- **ADRs** → explain why major architectural/technical decisions were chosen.
- **Implementation** → realizes the approved model. It must not silently redefine product or architecture.

## Specification Ownership
Each specification has one clear subject and owns the detailed behavior of that subject without redefining unrelated systems. Examples of such subjects include:
- Authentication
- Onboarding
- Enrollment / Academic Context
- Community / Membership
- Governance
- Authorization

*(Note: Specifications will be added incrementally and only where detailed behavior is important enough to justify the additional documentation. Not every possible feature requires its own specification.)*

## Dependencies
Specifications must explicitly record their dependencies on other specifications, canonical concepts, or systems where meaningful.

## Status and Maturity
A specification follows a defined status lifecycle:
- **DRAFT**
- **IN REVIEW**
- **APPROVED**
- **IMPLEMENTATION-READY**
- **ACTIVE**
- **SUPERSEDED**

And progresses through these maturity levels:
- **CONCEPTUAL**
- **BEHAVIORAL**
- **IMPLEMENTATION-READY**

**Important Clarification:** `APPROVED` ≠ `IMPLEMENTATION-READY`. A conceptual specification can be approved without being ready for implementation.

## Open Questions
Unresolved issues must be explicitly documented rather than silently decided. They should be conceptually classified as:
- **BLOCKING**
- **NON-BLOCKING**
- **FUTURE**

## Explicit Non-Assumptions
A specification should explicitly identify important things an implementation agent MUST NOT assume.

## Canonical Conflict Rule
A specification must never silently override canonical documentation. When a conflict is discovered, the process is:
1. Discover Conflict
2. Resolve Decision
3. Update Canonical Source
4. Update Specification

## ADR Relationship
- **Specification** → defines *what* must happen.
- **ADR** → explains *why* a significant architectural or technical choice was made.

## Diagrams
Diagrams are supporting artifacts to aid understanding, not independent sources of truth. 

## AI Implementation Use
An implementation agent should normally receive:
`Relevant Canonical Docs + Relevant Specification + Relevant ADRs + Relevant Diagrams`

The implementation agent **must not** invent behavior where the specification is unresolved.
