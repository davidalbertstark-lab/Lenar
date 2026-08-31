# Post-Propagation Audit

## Status
COMPLETE

## Scope Audited
- docs/01–17
- docs/diagrams/
- docs/archive/phase-b/
(Note: docs/adr/ and docs/specifications/ do not currently exist in the repository).

## Canonical Model Validation
The repository has successfully eradicated obsolete concepts like `Programme` and `Supabase Auth`, replacing them with current Phase B abstractions (Level, Lenar-controlled JWT auth). However, several areas show missing propagation regarding the detailed Onboarding flow, the strict separation of Identity vs. Profile, and the avoidance of a rigid organizational tree.

## Domain Findings

File: `docs/product/02-Problem-Users-Domain.md`
Section: 4.1 Foundational Domains
Finding: Lists "Identity" and "Enrollment" but fails to define Academic Profile, Registration, Approval, and Base Community as distinct conceptual stages/domains.
Why it conflicts with the canonical model: Rule 4 requires strict preservation of User Identity vs. Academic Profile vs. Enrollment boundaries. Rule 14 requires Base Community as a foundational concept.
Severity: HIGH
Type: MISSING PROPAGATION
Recommended correction: Expand the foundational domains to explicitly separate Registration, User Identity, Academic Profile, and Approval, and define Base Community.

## Organization Findings

File: `docs/diagrams/domain/organizational-context.mmd`
Section: Entire diagram
Finding: Visually forces a rigid universal tree (`University --> Faculty`, `Faculty --> Department`, `Department --> Level`).
Why it conflicts with the canonical model: Rule 5 explicitly states Organization is NOT a universal rigid tree, and Level is a first-class concept not universally subordinate to Department.
Severity: HIGH
Type: STRUCTURAL PROBLEM
Recommended correction: Redesign the diagram to show valid possible relationships (e.g., Level could sit under University) rather than a single fixed hierarchy.

## Identity / Enrollment Findings

File: `docs/product/06-Data-Content.md`
Section: 2.1 Core Conceptual Entities
Finding: Groups "User / Profile" as "The identity and preferences of an individual".
Why it conflicts with the canonical model: Rule 4 requires preserving User Identity, Academic Profile, and Enrollment as distinct concepts. This description collapses them into a single generic concept.
Severity: HIGH
Type: SPECIFICATION BOUNDARY / MISSING PROPAGATION
Recommended correction: Break "User / Profile" down into Identity, Registration claims, Academic Profile, and Enrollment.

## Onboarding Findings

File: `docs/product/04-UX-UI.md`
Section: 2.1 The Onboarding Journey
Finding: Lists profile claims as "(Matric No, Level, Faculty, Department)".
Why it conflicts with the canonical model: Rule 8 requires "Full Name, Matric No, Level, Faculty, Department" as current onboarding information. "Full Name" is missing.
Severity: LOW
Type: MISSING PROPAGATION
Recommended correction: Add "Full Name" to the listed profile claims.

File: `docs/product/03-Product-Requirements.md`
Section: 3. The V1 Scope Boundary
Finding: Mentions "Authentication & Student Context" but completely omits the Registration, Profile Submission, and Approval flows.
Why it conflicts with the canonical model: Registration/Onboarding is a critical V1 product flow that must be recognized in requirements.
Severity: HIGH
Type: MISSING PROPAGATION
Recommended correction: Explicitly define the Registration and Onboarding Approval workflow in the V1 Scope Boundary.

File: `docs/diagrams/product/feature-dependencies.mmd`
Section: Entire diagram
Finding: Omits the entire Onboarding/Approval lifecycle. It connects Authentication directly to Student Context.
Why it conflicts with the canonical model: Omits the critical Profile Submission -> Review -> Approval -> Enrollment -> Context flow.
Severity: MEDIUM
Type: MISSING PROPAGATION
Recommended correction: Inject Registration, Profile, and Approval dependencies between Authentication and Student Context.

File: `docs/diagrams/ux` (Multiple)
Section: N/A
Finding: No diagram visualizes the critical Onboarding state transitions (Registration -> Verification -> Submission -> Pending -> Approved/Rejected).
Why it conflicts with the canonical model: The onboarding flow is a core UX model that requires visual representation per Phase B rules.
Severity: MEDIUM
Type: MISSING PROPAGATION
Recommended correction: Create an onboarding-journey UX diagram.

## Community / Membership Findings

File: `docs/diagrams/domain/domain-map.mmd`
Section: Entire diagram
Finding: Missing `Membership`, `Registration`, and `Academic Profile` nodes. Identity is shown as a monolithic node connected directly to Enrollment.
Why it conflicts with the canonical model: Fails to preserve Membership as a distinct relationship from Community, and skips the Registration -> Profile flow.
Severity: HIGH
Type: MISSING PROPAGATION
Recommended correction: Add Membership as a relationship node for Community. Expand Identity to show Registration and Profile leading to Enrollment.

File: `docs/diagrams/data/information-model.mmd`
Section: Entire diagram
Finding: Missing Registration, Verification, Academic Profile, and Membership data entities.
Why it conflicts with the canonical model: Omits the foundational data structures established during onboarding.
Severity: HIGH
Type: MISSING PROPAGATION
Recommended correction: Add the missing onboarding data entities.

## Governance / Role Findings
No major governance conflicts found. Recent propagation correctly established Admin and Leader roles.

## Authorization / Security Findings

File: `docs/diagrams/security/authorization-context.mmd`
Section: Inputs
Finding: Misses `Context` as an input (lists Identity, Role, Scope, Resource, Action).
Why it conflicts with the canonical model: Rule 29 dictates Authorization = RBAC + Scope + Context.
Severity: HIGH
Type: CONTRADICTION
Recommended correction: Add Context to the authorization decision inputs.

File: `docs/product/02-Problem-Users-Domain.md`
Section: 3.2 The Authorization Model
Finding: References `diagrams/security/authorization-context.svg` which is missing the Context input, while `07-Security-Privacy-Governance.md` correctly references `authorization-model.svg` (which has Context).
Why it conflicts with the canonical model: Creates an internal cross-document contradiction regarding the authorization formula.
Severity: MEDIUM
Type: CONTRADICTION
Recommended correction: Consolidate the diagrams or fix `authorization-context.mmd` to include Context.

## Authentication Findings
Clean. No Supabase Auth remaining.

## Control Plane Findings
Clean.

## Data Findings
(See Identity / Enrollment Findings above regarding `06-Data-Content.md`).

## Architecture Findings
Clean. Modular monolith accurately represented.

## Product / UX Findings
(See Onboarding Findings above).

## Platform Findings
Clean.

## Offline / Resilience Findings
Clean. Offline constraints accurately reflected.

## Testing Findings
Clean.

## Analytics / Observability Findings
Clean.

## Infrastructure Findings
Clean.

## Legal / Business Findings
Clean.

## Diagram Findings
(Covered in Domain, Organization, Identity, Onboarding, Community, Authorization).

## Markdown / Documentation Quality Findings
Clean. No escaped syntax, broken headings, or unreadable formatting found.

## Cross-Document Contradictions
- `02-Problem-Users-Domain.md` references `authorization-context.svg` (which lacks Context) whereas `07-Security-Privacy-Governance.md` references `authorization-model.svg` (which has Context).

## Missing Propagation
- Registration, Academic Profile, Approval omitted from `02-Problem-Users-Domain.md`, `03-Product-Requirements.md`, `06-Data-Content.md`, `domain-map.mmd`, `information-model.mmd`.
- Full Name omitted from Profile Completion in `04-UX-UI.md`.
- No UX diagram for onboarding states.

## Accidental Invention / Over-Specification
Clean.

## Broken References
Clean.

## Specification-Boundary Violations
Clean. The docs remain high-level and defer exact schemas, JWT claims, and endpoint contracts.

## Recommended Corrections
- Update `02`, `03`, `04`, `06` to fully integrate the distinct Onboarding flow (Registration -> Verification -> Profile Submission -> Pending -> Approval -> Enrollment).
- Correct `organizational-context.mmd` to avoid a strict tree.
- Consolidate and correct `authorization-context.mmd`.
- Add Registration, Academic Profile, and Membership to `domain-map.mmd` and `information-model.mmd`.

## Phase B Readiness

Overall result:
READY WITH CORRECTIONS

Critical findings:
0

High findings:
7

Medium findings:
3

Low findings:
1

Files requiring correction:
- docs/product/02-Problem-Users-Domain.md
- docs/product/03-Product-Requirements.md
- docs/product/04-UX-UI.md
- docs/product/06-Data-Content.md
- docs/diagrams/domain/organizational-context.mmd
- docs/diagrams/domain/domain-map.mmd
- docs/diagrams/data/information-model.mmd
- docs/diagrams/product/feature-dependencies.mmd
- docs/diagrams/security/authorization-context.mmd

Phase B sign-off:
NOT YET

## Final Correction Status
- **02-Problem-Users-Domain.md:** Separated Identity into User Identity, Academic Profile, Governance Review, Enrollment, and Academic Context.
- **03-Product-Requirements.md:** Expanded V1 scope to fully define Authentication & Onboarding.
- **04-UX-UI.md:** Added 'Full Name' to profile claims. Linked newly created onboarding diagram.
- **06-Data-Content.md:** Corrected 'User / Profile' grouping to preserve Registration, User Identity, Academic Profile, and Enrollment.
- **diagrams/domain/organizational-context.mmd:** Corrected false rigid hierarchy. Rendered SVG.
- **diagrams/domain/domain-map.mmd:** Expanded Identity to preserve Academic Profile, Registration. Added Membership. Rendered SVG.
- **diagrams/data/information-model.mmd:** Added Registration, Verification, Academic Profile, and Membership. Rendered SVG.
- **diagrams/product/feature-dependencies.mmd:** Inserted the Profile, Approval, and Enrollment sequence. Rendered SVG.
- **diagrams/security/authorization-context.mmd:** Added Context. Renamed generic inputs. Rendered SVG.
- **diagrams/security/authorization-model.mmd:** Renamed generic inputs. Rendered SVG.
- **diagrams/ux/onboarding-journey.mmd:** Created and rendered new onboarding UX visual.
