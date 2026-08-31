# Phase B / Pass 2 — Domain Decisions

**Status:** COMPLETE  
**Phase:** B / Pass 2  

## 1. Purpose and Scope
This document is a Domain / Architecture Consistency Audit. It reconciles newly provided first-hand product evidence regarding the user-entry flow with the historical canonical domain model. The goal is to define clear conceptual boundaries between identity, registration, profile, enrollment, and authorization without inventing detailed feature specifications or database schemas.

## 2. Domain-Level Evidence from the First-Hand User Journey
The provided first-hand evidence establishes the following conceptual user-entry flow:
1. Account creation.
2. Identity/account email verification.
3. User provides academic/profile information.
4. Information is submitted (enters a pending/review state).
5. A relevant class-level leader reviews the submission.
6. The submission is approved or rejected (requiring correction and resubmission).
7. If approved, the user proceeds into the platform.

*Domain Implications:* 
- Account creation is distinct from academic attachment.
- The user's supplied profile is initially unverified (pending).
- Approval is a distinct lifecycle gate.
- Existing roles (e.g., class-level leader) participate in the approval of new identities.

## 3. Historical Domain Evidence
The historical architectural model maintains the following conceptual pillars:
- **Identity:** User Identity (JWT/Auth) vs. Account Lifecycle (Verification, Approval).
- **Academic Hierarchy:** Academic Identity → Academic Profile → Enrollment → Academic Context.
- **Organization:** University → Faculty → Department → Level.
- **Academic Time:** Academic Session → Semester.
- **Community:** Defined by Membership.
- **Governance & Authorization:** Creator Assignment dictates Roles. Authorization = RBAC + Scope + Context.
- **Enrollment Rule:** Enrollment establishes Academic Context.

## 4. Reconciliation of the Two
The first-hand product evidence maps cleanly onto the historical domain model if we enforce strict boundaries between what the user claims and what the system formally recognizes. Account creation handles "Identity". Providing academic info handles "Academic Profile". The leader's review handles the "Account Lifecycle (Approval)", and a successful approval formalizes the "Academic Identity" and establishes "Enrollment".

## 5. Identity / Registration Boundary
**Boundary:** Registration (account creation) solely establishes a base **User Identity** (who the person is, e.g., email/password). It does *not* establish academic standing. Registration is the prerequisite to the Account Lifecycle.

## 6. Academic Identity / Academic Profile Boundary
**Boundary:** 
- **Academic Profile** is the collection of academic information *supplied by the user* during onboarding. It is essentially a set of claims.
- **Academic Identity** is a distinct conceptual concern from the user's base identity or profile claims. User Identity ≠ Academic Identity ≠ Academic Profile ≠ Enrollment.

## 7. Profile / Enrollment Boundary
**Boundary:** The Academic Profile contains the data/claims submitted for review. Enrollment is the formal relational linkage created *after* the profile is approved. A user has a profile while pending, but they do not have an active Enrollment until approved.

## 8. Approval / Enrollment Boundary
**Boundary:** Approval is a state transition within the **Account Lifecycle**. When a class-level leader executes an "Approval", this action triggers the formal creation of an **Enrollment**.

## 9. Enrollment / Academic Context Boundary
**Boundary:** Enrollment is the relationship (the bridge). **Academic Context** is the destination (the formal institutional reality, such as Level, Session, and Semester). *Enrollment establishes Academic Context.*

## 10. Organization / Academic Context Boundary
**Boundary:** **Organization** is the static structural hierarchy of the institution (University → Faculty → Department → Level). **Academic Context** is a specific intersection of Organization and Academic Time that a user is attached to via Enrollment. 

## 11. Organization / Community Boundary
**Boundary:** **Organization** represents the official administrative hierarchy. **Community** represents participation, interest groups, or ad-hoc cohorts. They are distinct; a Department is an Organization, but a study group within it is a Community.

## 12. Community / Membership Boundary
**Boundary:** **Community** is the entity. **Membership** is the relational concept denoting participation and belonging within that entity.

## 13. Governance / Role / Scope / Authorization Boundary
**Boundary:** 
- **Governance** manages the lifecycle of power (Creator Assignments, Revocations).
- **Creator Assignment** grants a **Role** to a user.
- **Role** is a static title (e.g., Writer).
- **Scope** defines the boundary of that role (e.g., Department-level).
- **Authorization** is the active enforcement mechanism combining Role + Scope + Context to determine if an action is permitted.

## 14. Academic Context / Authorization Context Boundary
**Boundary:** **Academic Context** defines where a student formally sits for their studies (e.g., enrolled in Level 200). **Authorization Context** is the specific environment in which an action is being evaluated (e.g., trying to post an announcement). While a user's Academic Context strongly informs what their Authorization Context might allow, they are conceptually separate domains (one is academic state, the other is security state).

## 15. The Unresolved Issues from Pass 1
The following issues correctly remain unresolved from Pass 1:
- Exact registration workflow (UI/API steps).
- Exact enrollment attachment algorithm and cardinality (e.g., multiple enrollments).
- Exact Community types, ownership, and creation authority.
- Exact Membership structure.
- Exact mapping and permission sets of Student, Writer, Manager, Leader, Admin, Super Admin.
- Exact Scope semantics and Authorization Context semantics.
- Exact relationship between Academic Context and Authorization Context.
- Exact Academic Identity vs Academic Profile semantics (partially conceptually mapped above, but implementation remains unresolved).

## 16. Newly Discovered Domain-Level Questions
- **Cross-Domain Governance:** If a "class-level leader" (Governance/Role) approves an "Academic Profile" (Account Lifecycle), how does the Admin Control Plane securely map governance roles to onboarding workflows?
- **Rejection Lifecycle:** If a profile is rejected and resubmitted, does it mutate the existing Academic Profile or create a new submission record?
- **Leader Context:** How is a class-level leader's Authorization Context securely matched against an incoming user's claimed Academic Profile to ensure the correct leader reviews the correct student?

## 17. DECIDED
- **Registration vs. Enrollment:** Registration establishes User Identity; Enrollment establishes Academic Context post-approval.
- **Profile vs. Identity:** Academic Profile is user-supplied data (claims). User Identity ≠ Academic Identity ≠ Academic Profile ≠ Enrollment. Academic Identity is a distinct conceptual concern.
- **Enrollment Purpose:** Enrollment establishes Academic Context.
- **Organization vs. Community:** Organization is institutional structure; Community is participation/belonging.

## 18. CONFLICT
- None identified at the pure conceptual domain level between the first-hand evidence and the historical model.

## 19. UNSPECIFIED
- Exact cardinality of enrollments per user.
- Exact data structure of the Academic Profile.
- Whether class-level leaders are the *only* roles capable of approving profiles.
- The exact state machine for rejection and resubmission.

## 20. OUT OF SCOPE
- Exact JWT token claims and TTLs.
- UI flow for the registration and onboarding screens.
- Specific database tables, foreign keys, and indexes for Enrollment.

## 21. NEEDS ADR
- **Onboarding Governance:** An ADR is needed to formally define how Creator Roles (e.g., class-level leaders) are authorized to perform Account Lifecycle actions (Approvals) on unverified users.

## 22. Implications for the Canonical Domain Model
The canonical model holds up well against the real-world product evidence. The most significant implication is that the **Account Lifecycle** (Verification & Approval) is the central orchestrator that transitions user-supplied claims (Academic Profile) into authoritative state (Enrollment / Academic Context). Additionally, the Governance domain intersects heavily with the Account Lifecycle, as existing roles (Leaders) govern the entry of new users.

## 23. Documents That May Require Later Propagation
Based on this audit, future propagation passes should review:
- `docs/product/02-Problem-Users-Domain.md` (to clarify Profile vs. Identity boundaries).
- `docs/product/06-Data-Content.md` (to reflect the Profile-to-Enrollment state transition).
- `docs/product/07-Security-Privacy-Governance.md` (to cover how Governance interacts with the Account Lifecycle).

## 24. Explicit Core Governance and Membership Decisions
- **Approval:** Approval establishes Enrollment.
- **Rejection:** Rejected Submission → Profile Completion (requires correction and resubmission).
- **Leader:** Holds department-level approval context and authority. ("Class Leader" and "Leader" refer to the same role).
- **Admin:** Holds university-level approval authority.
- **Admin Rights:** Admin creates Communities and assigns Leaders.
- **Membership:** Every active user receives automatic Base Community Membership based on their approved Academic Context.
