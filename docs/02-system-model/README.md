# Lenar System Model

This directory bridges the gap between **User Requirements** and **Strict Specifications**. It provides the high-level mental models, domain relationships, and master user journeys that explain *how* Lenar conceptually solves the problems defined in `01-user-requirements/`.

## Recommended Reading Order

1. **[01-lenar-foundation-overview.md](./01-lenar-foundation-overview.md)**
   *The high-level introduction to Lenar's core behavioral domains and architecture principles.*

2. **[02-current-system-model.md](./02-current-system-model.md)**
   *The definitive chronological journey of how a student accesses the platform, and the exact static conditions that determine their authority.*

3. **[03-nine-domain-map.md](./03-nine-domain-map.md)**
   *A visual map grouping the 9 foundational domains (Identity, Academic, Community) to show how they conceptually relate.*

4. **[04-master-user-journey.md](./04-master-user-journey.md)**
   *Detailed step-by-step state diagrams charting a user's path through the system.*

5. **[05-domain-relationships.md](./05-domain-relationships.md)**
   *Explains how data and authority explicitly flow across boundaries.*

6. **[06-decision-and-boundary-map.md](./06-decision-and-boundary-map.md)**
   *Strict architectural boundaries dictating which domains are allowed to communicate or share state.*

---
> **Next Step:** After grasping how these domains interact, proceed to `../03-specifications/` to read the strict, rule-by-rule definitions for each individual domain.
