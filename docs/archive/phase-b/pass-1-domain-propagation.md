# Pass 1 Domain Propagation Report

**Status:** COMPLETE  
**Phase:** B / Pass 1  

## Summary
Corrected and propagated foundational domain corrections across the Lenar documentation suite without inventing unsupported definitions or resolving unresolved questions. 

## Confirmed Changes
- **Programme Excluded:** Removed all active references to "Programme" as a current domain entity.
- **Level Included:** Formally integrated "Level" into the organizational context (University → Faculty → Department → Level).
- **Academic Time & Enrollment:** Clarified that the Admin Control Plane maintains authoritative Academic Time (Academic Session → Semester). Documented that Enrollment establishes Academic Context.
- **Community & Governance:** Distinctly separated Community (and Membership) from Organization, and established Governance for managing Creator Assignments.
- **Admin Control Plane:** Defined the Admin Control Plane as a conceptual architectural boundary responsible for governing authoritative state (Organization, Academic Time, Governance).
- **Authorization Precision:** Refined the authorization model to strictly require `Authorization = RBAC + Scope + Context`.
- **Authentication Update:** Removed "Supabase Auth" as the primary identity provider, replacing it with "Lenar-controlled JWT / Credentials / Sessions."

## Files Modified
- `docs/product/02-Problem-Users-Domain.md`: Replaced Programme with Level in organizational hierarchy. Replaced Administration with Admin Control Plane. Clarified foundational domains.
- `docs/product/03-Product-Requirements.md`: Replaced Programme with Level in organizational requirements.
- `docs/product/06-Data-Content.md`: Replaced Programme with Level. Added Community and Governance to data boundaries.
- `docs/product/07-Security-Privacy-Governance.md`: Updated Role vs. Authorization explicitly defining Context.
- `docs/architecture/09-System-Architecture.md`: Documented the Admin Control Plane responsibilities explicitly.
- `docs/architecture/10-Technology-Stack.md`: Replaced Supabase Auth with Lenar-controlled JWT auth.
- `docs/architecture/14-Infrastructure-Operations.md`: Replaced Supabase Auth with Lenar-controlled JWT auth. Removed Supabase from dependency failure list.
- `docs/product/15-Legal-Business.md`: Removed Supabase Auth from the third-party dependencies list.
- `docs/decisions/17-Decisions-Risks-Evolution.md`: Updated current major decisions table to reflect Lenar-controlled authentication.

## Diagrams Modified
- `docs/diagrams/domain/organizational-context.mmd` & `.svg`: Swapped Programme for Level.
- `docs/diagrams/domain/domain-map.mmd` & `.svg`: Integrated Academic Time, Enrollment, Community, and Governance. Renamed Administration to Admin Control Plane.
- `docs/diagrams/data/information-model.mmd` & `.svg`: Realigned root data concepts with Academic Time, Enrollment, Community, and Governance.
- `docs/diagrams/technology/technology-stack.mmd` & `.svg`: Replaced Supabase Auth with Lenar JWT Auth.
- `docs/diagrams/technology/technology-responsibility.mmd` & `.svg`: Replaced Supabase Auth with Lenar JWT Auth.
- `docs/diagrams/product/feature-dependencies.mmd` & `.svg`: Renamed Administration to Admin Control Plane.
- `docs/diagrams/product/product-area-map.mmd` & `.svg`: Renamed Administration to Admin Control Plane.
- `docs/diagrams/legal-business/provider-dependency.mmd` & `.svg`: Replaced Supabase Auth with Lenar JWT Auth.
- `docs/diagrams/security/authorization-model.mmd` & `.svg`: Adjusted inputs to RBAC / ROLE, SCOPE, and CONTEXT.

## Supabase References Removed/Corrected
- `docs/architecture/10-Technology-Stack.md`
- `docs/architecture/14-Infrastructure-Operations.md`
- `docs/product/15-Legal-Business.md`
- `docs/decisions/17-Decisions-Risks-Evolution.md`
- `docs/diagrams/technology/technology-stack.mmd`
- `docs/diagrams/technology/technology-responsibility.mmd`
- `docs/diagrams/legal-business/provider-dependency.mmd`

## Programme References Corrected
- `docs/product/02-Problem-Users-Domain.md`
- `docs/product/03-Product-Requirements.md`
- `docs/product/06-Data-Content.md`
- `docs/diagrams/domain/organizational-context.mmd`

## Unresolved Issues Found
The following remain explicitly unresolved and were left untouched as per instructions:
- Exact registration workflow.
- Exact enrollment attachment algorithm and cardinality (e.g., multiple enrollments).
- Exact Community types, ownership, and creation authority.
- Exact Membership structure.
- Exact mapping and permission sets of Student, Writer, Manager, Leader, Admin, Super Admin.
- Exact Scope semantics and Authorization Context semantics.
- Exact relationship between Academic Context and Authorization Context.
- Exact Academic Identity vs Academic Profile semantics.

## Follow-up Phase B Work
- Reconcile specific Manager/Leader roles and explicit permission structures within the RBAC+Scope+Context model.
- Define JWT claims, signing, token TTL, refresh strategies, revocation mechanisms, and session lifecycles for Lenar-controlled auth.
- Draft clear state diagrams for Account Lifecycle (Verification -> Approval -> Suspension) versus Authentication.
- Elaborate on the Community domain model (types, ownership, creation rights).
