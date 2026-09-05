# Lenar Specifications

This directory contains the strict, undeniable rules for how the system behaves. These documents translate the conceptual models from `02-system-model/` into exact state machines, schemas, and technical constraints.

## Recommended Reading Order

The specifications are organized by domain. You do not need to read them all in order; consult them as needed when building specific features.

1. **[Account Lifecycle](./account-lifecycle/account-lifecycle-specification.md)**
   *Rules for user account states and transitions.*
2. **[Organization](./organization/organization-specification.md)**
   *Rules for modeling the university structural hierarchy.*
3. **[Academic Time](./academic-time/academic-time-specification.md)**
   *Rules for authoritative temporal tracking.*
4. **[Enrollment](./enrollment/enrollment-specification.md)**
   *Rules for establishing a student's academic context.*
5. **[Community](./community/community-membership-specification.md)**
   *Rules for Base Community membership and interaction.*
6. **[Governance](./governance/governance-specification.md)**
   *Rules for leader assignment and revocation.*

### Foundational Capabilities
- **[Authentication](./authentication/authentication-specification.md)**
- **[Authorization](./authorization/authorization-specification.md)**
- **[Onboarding](./onboarding/onboarding-specification.md)**

*(Note: Feature-level specifications for Content, Issues, and Search will be added here in the future when implementation begins).*

---
> **Next Step:** After understanding the strict rules for the domains, proceed to `../04-architecture/` to understand the physical systems and infrastructure that will run this code.
