# Review Guide

This guide explains how team members and partners should review Lenar's foundational model.

## The Review Philosophy

The review process follows a structured lifecycle to ensure decisions are deliberate and their impacts are fully understood across the system:

**UNDERSTAND**
→ **QUESTION**
→ **DISCUSS**
→ **COMPARE ALTERNATIVES**
→ **DECIDE**
→ **RECORD DECISION**
→ **ASSESS IMPACT**
→ **UPDATE CANONICAL SPECIFICATION**
→ **AUDIT**
→ **PROPAGATE**

## You Are Allowed to Challenge Decisions

Explicitly: **You are allowed to challenge existing decisions.**
The existing audits prove that the current model is internally consistent. They do NOT make the model permanently unquestionable. We welcome challenges to ensure the foundation is as robust and adaptable as possible.

### What to Challenge
- **Definition:** Is a concept correctly defined?
- **State:** Are the states complete and accurate?
- **Transition:** Are the triggers between states correct?
- **Boundary:** Is a domain overstepping its boundary?
- **Ownership:** Who owns a piece of data or decision?
- **Dependency:** Are cross-domain dependencies safe?
- **Exception:** What edge cases exist?
- **Security consequence:** Can a malicious/untrusted client exploit this?
- **Historical consequence:** What happens historically when state changes later?
- **Offline consequence:** How does this behave in offline caches?
- **Scalability consequence:** Will this make sense if Lenar supports more Universities?
- **Cross-domain consequence:** Does this create hidden coupling?

### Questions to Ask Repeatedly
- Is this actually correct?
- Is it the best model?
- Is something missing?
- Is something unnecessarily complicated?
- Does another domain own this better?
- Does this create hidden coupling?
- What happens in edge cases?
- Can a malicious/untrusted client exploit it?
- What happens when state changes later?
- What happens historically?
- Will this still make sense if Lenar supports more Universities?
- Does this make sense outside V1/FUTA?

## Prohibited Actions

During this behavioral review phase, please **DO NOT**:
- Jump directly into implementation.
- Solve domain problems with database tricks.
- Solve behavioral ambiguity with API design.
- Assume current application code is automatically authoritative.

The goal is to perfect the behavioral model first. Implementation follows behavior.
# Review and Change Process

Lenar's foundation is built on cross-domain consistency. Changing a rule in one domain often creates ripples across several others. To maintain system integrity, all team members and partners should follow this formal review process.

## The Review Process

1. **QUESTION:** Write down the exact issue or concern. (e.g., "Why doesn't Academic Time automatically promote students?")
2. **ANALYZE:** Identify every affected domain. (In the example: Academic Time, Enrollment, Community).
3. **OPTIONS:** Develop alternative behavioral rules.
4. **DISCUSS:** Compare trade-offs with the team.
5. **DECIDE:** Choose the superior alternative.
6. **RECORD:** Update the formal decision log.
7. **IMPACT:** Identify which canonical specifications and diagrams must change.
8. **AUDIT:** Run a conceptual boundary audit on the proposed change.
9. **PROPAGATE:** Update the canonical documentation.
10. **FREEZE:** Treat the new rule as an accepted foundation decision.

**CRITICAL RULE:** No behavioral change becomes "official" merely because somebody edited a summary document in this partner review package. The canonical specification must be updated, and cross-domain impact must be formally assessed.

## Intentionally Unresolved Topics

During the formulation of this behavioral foundation, several topics were intentionally deferred. These are technical implementation or specific business-logic issues that belong to the next phase of design.

**Do not attempt to resolve these during the foundational behavioral review:**
- JWT/session implementation mechanisms.
- OTP exact behavior and timeout rules.
- Session lifetime, renewal, and invalidation mechanisms.
- Exact historical representation of Enrollment (e.g., event sourcing vs. temporal tables).
- Exact progression mechanics (pass/fail, GPA calculation).
- Organization migration mechanics (how to merge/split departments physically in the database).
- Academic Time implementation (exact scheduler, cron logic, or event bus).
- Specialized Community behavior outside the Base Community.
- Handling of multiple simultaneous Governance assignments per user.
- The exact RBAC permission matrix (the list of specific endpoints and roles).
- Policy-engine representation (e.g., OPA, hardcoded middleware).

*Unresolved does not mean forgotten; it means intentionally deferred to a later decision stage.*
