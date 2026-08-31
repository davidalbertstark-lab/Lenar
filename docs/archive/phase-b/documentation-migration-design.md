# Documentation Migration Design

## Status
COMPLETE

## Existing Documentation Model
The current repository reflects a chronological build sequence rather than a pedagogical reading path. Root `01-17` documents contain foundational product and technical strategy. `specifications/` contain strict behavioral contracts. `phase-b/` holds the audit trails that proved consistency. `partner-review/` was created as an orientation layer for the specifications but operates as a parallel silo. This structure creates overlapping authority, poor discoverability for newcomers, and a missing central front door.

## Information-Type Authority Model
To avoid a simplistic hierarchy, authority is mapped by information type:
| Information Type | Authoritative Source | Supporting Sources | Historical Sources |
|---|---|---|---|
| Product Vision & Strategy | `docs/product/` (derived from `01-17`) | `docs/foundation/` | `docs/archive/` |
| Behavioral Rules & Contracts | `docs/specifications/` | None (Single Source of Truth) | `docs/archive/phase-b/` |
| System Overview & Onboarding | `docs/foundation/` | `docs/README.md` | `partner-review` (deprecated) |
| Technical Architecture | `docs/architecture/` (derived from `01-17`) | None | Original ADRs |
| Implementation Decisions | `docs/adr/` | Component docs | `docs/archive/` |

## 17 Canonical Documents — Detailed Classification
The 17 numbered documents (`01-17`) represent vital, non-duplicated product strategy, UX, and technical architecture. They do NOT own behavioral domains anymore, but they still own the *why* and the *how* of the system.
- **Product Strategy & Requirements:** 01, 02, 03, 04, 06, 07, 15.
- **Technical Architecture & Ops:** 05, 08, 09, 10, 11, 12, 13, 14, 16.
- **Decisions/Risks:** 17.
*Recommendation:* Keep numbering intact within their new semantic directories (`product/` and `architecture/`) to preserve the established logical reading order, which remains highly effective for learning the technical context.

## Specification Authority Model
The 9 domains in `docs/specifications/` are the absolute and undisputed source of truth for behavioral state, transitions, and boundaries. No summary document or root architecture document may override them.

## Foundation Layer Evaluation
The files currently in `partner-review/` (`01-lenar-foundation-overview.md` through `06-decision-and-boundary-map.md`) are the most cohesive system-wide explanation in the repository. They are NOT partner-specific; they are the missing Level 1 & 2 orientation for *all* readers. They should be promoted to a permanent `docs/foundation/` directory.

## Partner-Review Evaluation
The directory `docs/foundation/` implies a temporary or restricted audience. This creates a silo. Its useful orientation files should become the core `foundation/` layer, its review process files merged into a unified contributor guide, and the directory itself removed.

## Partner Domain Summary Evaluation
The files in `docs/foundation/domains/01-09` summarize the authoritative specifications. **This violates the single source of truth.** Maintaining a "lite" version of behavioral contracts guarantees future drift and contradiction. These files must be **DELETED**. Readers will be routed directly from the `foundation/` layer to the actual `specifications/` using direct links.

## Phase-B Evaluation
The files in `docs/archive/phase-b/` are invaluable historical audit logs (e.g., proving that Academic Time does not promote students, fixing Account Lifecycle diagrams). They must not be deleted, as they explain *why* boundaries exist. However, they clutter the active reading path. They must be moved to `docs/archive/phase-b/`.

## Diagram Ownership Evaluation
- **Domain-Specific Diagrams:** Keep strictly inside `docs/specifications/<domain>/diagrams/`.
- **Global System Models:** Move from `foundation/diagrams/` to `docs/foundation/diagrams/`.
- **Product/UX/Architecture Diagrams:** Keep in `docs/product/diagrams/` or `docs/architecture/diagrams/`.
This prevents diagram fragmentation and co-locates visuals with their authoritative text.

## Duplicate Content Evaluation
The primary duplication identified is the domain summaries in `partner-review/domains/`. By deleting these and relying purely on `specifications/`, we eliminate the risk of duplicate truth.

## Active Reference Impact
Moving `01-17` and `partner-review/` will break numerous relative links inside the `specifications/` (which frequently point to `../../product/01-Lenar-Foundation.md`). The final stage of migration must include a global search-and-replace to rewrite `../../product/01-Lenar-Foundation.md` to `../../product/01-Lenar-Foundation.md`.

## Documentation Front Door Design
**File:** `docs/README.md`
**Content:**
1. **What is Lenar?** (Brief 2-sentence vision).
2. **Where to Start (Reading Journey):** 
   - Start with Foundation (`docs/foundation/`).
   - Deep dive into Behavior (`docs/specifications/`).
   - Explore Architecture (`docs/architecture/`).
3. **Source of Truth Hierarchy:** Explicitly stating that specifications override all other docs for domain behavior.
4. **Collaboration & Review:** Link to the change process.

## Zero-Context Reader Findings
Currently, a zero-context reader opens `docs/` and sees 17 numbered files and random folders. They fail the test. Post-migration, they will see a `README.md` that explicitly points them to `foundation/02-current-system-model.md`, instantly giving them the required context.

## Partner Reader Findings
Partners need clear system models without technical implementation details. The promoted `foundation/` layer serves this perfectly without keeping them in a siloed "partner" folder.

## Engineering Reader Findings
Engineers need to know what is decided vs. unresolved. The `foundation/06-decision-and-boundary-map.md` clarifies this. They can then read `specifications/` for strict logic, and `architecture/` for the implementation stack.

## Minimum Complexity Findings
The proposed tree adds only semantic grouping (`foundation/`, `product/`, `architecture/`, `archive/`). It removes artificial silos (`partner-review/`) and deletes duplicate files (`partner-review/domains/`). It is the minimum viable structure for coherence.

## Recommended Permanent Documentation Tree
```text
docs/
├── README.md                      (The Front Door)
├── foundation/                    (Orientation & System Model)
├── specifications/                (Authoritative Behavioral Contracts)
├── product/                       (Vision, UX, Requirements)
├── architecture/                  (Tech Stack, Infra, Ops)
├── adr/                           (Decisions & Risks)
└── archive/                       (Historical Audits & Phase-B)
```

## Artifact-by-Artifact Migration Classification

### KEEP
- **Target:** `docs/specifications/**`
  - **Action:** Retain entirely as-is. 
  - **Reason:** Absolute source of truth for behavioral domains.
  - **Risk:** Low.

### KEEP BUT REPOSITION
- **Target:** `docs/foundation/01` to `06` and `foundation/diagrams/`
  - **Action:** Move to `docs/foundation/`.
  - **Reason:** Provides the critical missing Level 1 & 2 orientation. 
  - **References:** Will require updating internal links to point directly to `../specifications/`.
- **Target:** `docs/01` to `04`, `06`, `07`, `15`
  - **Action:** Move to `docs/product/`. Keep numbering.
  - **Reason:** Groups product strategy separately from technical implementation.
- **Target:** `docs/05`, `08` to `14`, `16`
  - **Action:** Move to `docs/architecture/`. Keep numbering.
  - **Reason:** Consolidates technical and operational requirements.
- **Target:** `docs/decisions/17-Decisions-Risks-Evolution.md`
  - **Action:** Move to `docs/adr/`.
  - **Reason:** Standardizes the location of architectural decision records.

### MERGE
- **Target:** `docs/foundation/README.md`
  - **Action:** Extract its "START HERE" and "What is Lenar" concepts into a new `docs/README.md`.
  - **Reason:** Creates the missing master front door.
- **Target:** `docs/foundation/00-review-guide.md` & `07-review-and-change-process.md`
  - **Action:** Merge into a single `docs/foundation/review-process.md`.
  - **Reason:** Unifies the collaboration rules for the team and partners.

### ARCHIVE
- **Target:** `docs/archive/phase-b/**`
  - **Action:** Move entirely to `docs/archive/phase-b/`.
  - **Reason:** Preserves vital audit history and decision proofs without cluttering the active reading path.
  - **Unique info preserved:** Yes, all audit traces remain intact.

### DELETE
- **Target:** `docs/foundation/domains/01-09`
  - **Action:** Delete entirely.
  - **Reason:** Summarizes authoritative specifications, violating the single source of truth.
  - **Unique info preserved:** None. The authoritative rules live in `specifications/`.
  - **Risk:** Positive (removes drift risk).
- **Target:** `docs/foundation/` directory (after contents moved/merged).
  - **Action:** Remove.
  - **Reason:** Eliminates the "partner silo" concept.

## Migration Stages
1. **Stage 1 (Front Door):** Create `docs/README.md`.
2. **Stage 2 (Foundation Promotion):** Create `docs/foundation/`, move `partner-review/01-06` and diagrams into it. Merge review process docs.
3. **Stage 3 (Canonical Reorganization):** Create `product/`, `architecture/`, and `adr/`. Move `01-17` accordingly.
4. **Stage 4 (Archive):** Create `archive/`, move `phase-b/` into it.
5. **Stage 5 (Duplicate Removal):** Delete `partner-review/domains/` and the empty `partner-review/` folder.
6. **Stage 6 (Link Validation):** Run repository-wide find-and-replace to correct all relative markdown paths (e.g., `../../01-Lenar...` to `../../product/01-Lenar...`).

## Validation Requirements
After execution, verify:
1. `docs/README.md` exists and routes correctly.
2. `partner-review/` no longer exists.
3. `specifications/` is untouched internally (other than relative link fixes).
4. No broken `.svg` embeds.

## Rollback / Safety Considerations
Since this is purely a documentation file-system reorganization, it is inherently safe if executed as a single git commit. If links break, a `git revert` instantly restores the current state.

## Final Recommendation
Execute the phased migration. The current structure served the team well during the behavioral modeling phase (Phase B), but it is now actively hostile to new readers due to fragmentation and missing front doors. The proposed design maximizes discoverability, eliminates duplicate truths, and creates a clear reading journey from zero-context to deep technical mastery.
