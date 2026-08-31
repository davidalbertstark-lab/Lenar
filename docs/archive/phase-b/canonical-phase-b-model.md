# Canonical Phase B Model

**Status:** COMPLETE  
**Phase:** B  

This document serves as the authoritative Phase B propagation reference. It distinguishes between confirmed decisions, current directions, deferred specification topics, and explicitly unresolved matters.

## 1. Confirmed Decisions

### 1.1 Foundation
- Lenar is a student-centered digital platform with the core purpose of making university life easier to navigate digitally.
- Initial context is FUTA.
- Core principles: Student value, Simplicity, Security, Privacy, Correctness, Modularity, Resilience, Accessibility, Evidence, Evolution, Documentation, AI alignment.

### 1.2 Domain Entities
- **Identity:** User Identity ≠ Academic Identity ≠ Academic Profile ≠ Enrollment. Academic Identity is a distinct conceptual concern.
- **Registration:** Establishes User Identity.
- **Academic Profile:** User-submitted claims.
- **Enrollment:** The formal attachment established upon profile approval. **Enrollment establishes Academic Context.**
- **Academic Context:** Intersection of organization and academic time (e.g., Level, Session, Semester).
- **Academic Time:** A first-class domain (Academic Session → Semester).
- **Community:** Represents participation/belonging. Every active user has a required, automatic, foundational Base Community established from their approved Academic Context.
- **Membership:** The relational concept denoting participation in a Community.
- **Governance:** Manages power (Creator Assignments, Revocations, Transfers). Distinct from generic Membership.
- **Organization:** The institutional structural hierarchy (University, Faculty, Department, Level). The hierarchy is flexible and respects valid institution-specific relationships (Level is first-class, but not universally subordinate solely to Department in a rigid tree).
- **Programme is EXCLUDED.** It is not part of the current Lenar model.

### 1.3 Onboarding Journey
- **Flow:** PERSON → REGISTRATION → EMAIL VERIFICATION → ACADEMIC PROFILE COMPLETION → PROFILE SUBMISSION → PENDING REVIEW
  - **If Rejected:** → PROFILE COMPLETION (correction) → RESUBMIT
  - **If Approved:** → ENROLLMENT → ACADEMIC CONTEXT → BASE COMMUNITY → MEMBERSHIP → ACTIVE ACCESS

### 1.4 Governance and Authorization
- **Primary User Category:** Student.
- **Administrative Roles:** Admin (university-level authority, can approve anywhere within scope, creates Communities, assigns Leader), Super Admin (platform-wide).
- **Governance Roles:** Leader (department-level context, approves applicable submissions, assigns Sub-Leader, Manager, Writer), Sub-Leader, Manager (department-level), Writer (department-level).
- **Authorization Equation:** Authorization = RBAC + Scope + Context. Role is not identical to Authority. Membership is not Governance Authority.

### 1.5 Architecture and Security
- **Architecture:** FastAPI + PostgreSQL modular monolith.
- **Admin Control Plane:** An architectural responsibility/boundary for authoritative system state (Organization, Academic Time, Governance, Community administration). Not just a UI dashboard.
- **Security:** Server is authoritative. Client is untrusted. Offline state does not bypass server authority. Role and scope are distinct.
- **Authentication:** Lenar-controlled authentication (JWT / Credentials / Sessions). **Supabase Auth is excluded.**

## 2. Current Direction
- **Mobile:** Flutter + Dart (Android, iOS).
- **Web:** React + TypeScript + Vite (PWA).
- **Data:** PostgreSQL (authoritative relational), SQLite (mobile local persistence for drafts, cached info, pending ops).

## 3. Deferred to Specification (Out of Scope for Documentation)
- Exact database schema.
- Exact API endpoint contracts.
- Exact JWT implementation (claims, TTL, refresh strategies, revocation mechanisms).
- Exact UI flow and screen design for registration/onboarding.
- Complete RBAC permission matrix for roles (Manager, Writer, Sub-Leader, etc.).
- Analytics event taxonomy.
- Test suite definitions.
- Parser design.

## 4. Unresolved
- Exact enrollment attachment algorithm and cardinality (multiple enrollments).
- Exact Academic Context composition.
- Exact Community matching algorithm.
- Exact mechanisms for additional Community memberships.
- Exact community lifecycle (deletion rules, request workflow).
- Exact scope representation and authorization policy engine.
- Exact assignment revocation and transfer authority rules.
- Multiple-role rules.
- Exact registration API workflow mechanics.
- Exact state machine for account lifecycle (Verification → Approval → Suspension) versus Authentication.
