# Documentation Architecture Audit

## Status
COMPLETE

## Current Documentation Inventory
- **17 Canonical Documents (`docs/01-17*.md`)**: Original product, architecture, UX, and technical strategy.
- **Specifications (`docs/specifications/`)**: The 9 authoritative behavioral contracts (Account Lifecycle, Authentication, Onboarding, Organization, Academic Time, Enrollment, Community, Governance, Authorization) plus templates.
- **Phase B (`docs/archive/phase-b/`)**: Audit history, domain decision logs, correction reports, and working files.
- **Partner Review Package (`docs/foundation/`)**: Recent orientation guides, system models, domain relationships, journey maps, and domain summaries.
- **Diagrams (`docs/diagrams/` and scattered)**: MMD/SVG pairs across the root diagrams folder, partner review, and specifications.

## Current Documentation Architecture
The current architecture is organic and chronological rather than pedagogical. It reflects *how* the system was built (initial canonical docs -> behavioral specification pass -> phase B audits -> partner review package) rather than *how it should be read*. 
As a result, a new reader faces an overwhelming flat list of 17 root documents, multiple sub-directories, and no clear entry point (`README.md` is missing).

## Historical Context
The 17 canonical documents established the initial vision and requirements. During Phase B, the team realized that complex interconnected behaviors (like Governance vs. Authorization, or Enrollment vs. Organization) required strict, undeniable behavioral contracts. This birthed the 9 Foundational Specifications. To ensure consistency, rigorous audits were placed in `phase-b/`. Finally, `partner-review/` was created because the 9 specifications were too dense for a newcomer to immediately grasp without a connecting overview.

## User / Partner Discoverability Findings
Discoverability is currently poor for a newcomer. A partner or new engineer entering `docs/` has no "START HERE" sign. They might start reading `01-Lenar-Foundation.md`, then jump to `09-System-Architecture.md`, completely missing the rigorous behavioral rules in `specifications/` or the cohesive system model in `partner-review/02-current-system-model.md`.

## Documentation Front Door Findings
**Missing.** There is no `docs/README.md`. A front door is desperately needed to orient the reader, explain the repository's purpose, define the source-of-truth hierarchy, and route them to the correct reading path (Orientation → Foundation → Specifications → Architecture).

## 17 Canonical Document Findings
The 17 documents contain incredibly valuable product strategy, UX, technical architecture, and operational requirements. However, their behavioral domain rules have been superseded by the `specifications/`. Retaining them as a flat numbered list at the root competes with the newer, more accurate foundations. They should be re-layered into `product/`, `architecture/`, and `adr/` categories.

## Specification System Findings
The `specifications/` directory is the crown jewel of the behavioral model. It is the undeniable source of truth for the 9 domains. It is well-structured, consistent, and strictly behavioral. Its internal README and template are effective. This structure must be preserved exactly as is, but it needs a better "on-ramp" from the root.

## Phase-B Findings
`docs/archive/phase-b/` is entirely historical process evidence. It contains readiness audits, propagation reports, and domain decisions. While vital for proving the system's consistency at a point in time, it is clutter for a new reader trying to understand the final product. It belongs in an `archive/` or `historical/` directory.

## Partner-Review Findings
The `docs/foundation/` package is misnamed. It is not just for partners; documents like `02-current-system-model.md`, `04-master-user-journey.md`, `05-domain-relationships.md`, and `06-decision-and-boundary-map.md` are the missing Level 1/Level 2 documentation for *everyone*. However, the `domains/` subdirectory inside `partner-review/` introduces a dangerous pattern of summarizing authoritative specifications in a second location, risking a competing source of truth over time. 

## Diagram Architecture Findings
Diagrams are currently fragmented. Some live in `docs/diagrams/`, others in `specifications/**/diagrams/`, and others in `foundation/diagrams/`. The co-location of diagrams with their specific markdown files (like in the specifications) is excellent for maintenance. However, global system diagrams should be centralized in the overview layer.

## Duplicate Content Findings
1. **Behavioral Rules:** The 17 canonical docs contain early versions of behavioral rules that are now strictly governed by the `specifications/`. 
2. **Domain Summaries:** `docs/foundation/domains/` summarizes the exact same content as `docs/specifications/`. This is unnecessary cognitive load and a maintenance liability.

## Source-of-Truth Findings
The current structure lacks a clear declaration of authority. A reader might assume `07-Security-Privacy-Governance.md` is the final word on Governance, missing `docs/specifications/governance/governance-specification.md`. The hierarchy must be explicitly defined in the front door: Specifications > Foundation Overviews > Canonical Product Docs.

## Audience / Reading Path Findings
The current flat structure forces all audiences through the same confusing list. We need distinct paths:
- **Partners/Designers:** Orientation → Foundation → Product
- **Domain Reviewers:** Foundation → Specifications
- **Engineers:** Foundation → Specifications → Architecture

## Documentation Layer Findings
The repository naturally supports the requested layered model, but the files are currently mixed.
- Level 1 & 2 (Orientation & Connected System): Currently hidden in `partner-review/`.
- Level 3 & 4 (Domain Model & Specifications): Currently in `specifications/`.
- Level 5 & 6 (Architecture & Decisions): Currently scattered across `01-17`.

## Complexity Findings
The documentation is unnecessarily complex due to folder bloat and historical artifacts. Renaming and regrouping the existing files into a few strong directories (`foundation/`, `specifications/`, `architecture/`, `product/`, `archive/`) will drastically reduce cognitive load without deleting valuable context.

## Collaboration / GitHub Findings
GitHub navigation relies heavily on `README.md` files auto-rendering in directories. The lack of a root `README.md` hinders collaboration. The heavy reliance on numbered files (`01-17`, `00-07`) is good for ordering but bad for contextual grouping.

## Recommended Permanent Documentation Architecture
```text
docs/
├── README.md                      (The Front Door: Start Here, Source of Truth hierarchy)
├── foundation/                    (Level 1 & 2: Promoted from partner-review)
│   ├── 01-overview.md
│   ├── 02-master-system-model.md
│   ├── 03-nine-domain-map.md
│   ├── 04-master-user-journey.md
│   ├── 05-domain-relationships.md
│   ├── 06-decision-and-boundary-map.md
│   └── diagrams/
├── specifications/                (Level 3 & 4: Authoritative Behavioral Contracts)
│   ├── README.md
│   ├── templates/
│   ├── account-lifecycle/
│   ├── authentication/
│   ├── onboarding/
│   ├── organization/
│   ├── academic-time/
│   ├── enrollment/
│   ├── community/
│   ├── governance/
│   └── authorization/
├── product/                       (Level 5: Strategy, UX, Requirements)
│   ├── problem-users-domain.md
│   ├── product-requirements.md
│   ├── ux-ui.md
│   ├── data-content.md
│   └── legal-business.md
├── architecture/                  (Level 6: Tech Stack, Infra, Ops)
│   ├── system-architecture.md
│   ├── technology-stack.md
│   ├── platform.md
│   ├── offline-sync-resilience.md
│   ├── security-privacy.md
│   ├── performance-reliability.md
│   ├── infrastructure-operations.md
│   └── testing-quality.md
├── adr/                           (Decisions & Risks)
│   └── decisions-risks-evolution.md
└── archive/                       (Historical Context)
    └── phase-b/                   (All audit reports and propagation logs)
```

## Recommended Reading Journey
1. **START:** `docs/README.md`
2. **ORIENT:** `docs/foundation/01-overview.md` through `06-decision-and-boundary-map.md`.
3. **DEEP DIVE:** `docs/specifications/` to read the exact behavioral rules for specific domains.
4. **BUILD:** `docs/architecture/` for technical design and stack details.

## Artifact Classification

### KEEP
- All 9 foundational specifications (`docs/specifications/**`).
- Specification template and README.
- `docs/diagrams/ux/**` (move to `product/diagrams/`).

### KEEP BUT REPOSITION
- `docs/foundation/01` to `06` → Promote to `docs/foundation/`.
- `docs/foundation/diagrams/` → Promote to `docs/foundation/diagrams/`.
- `docs/01-17` canonical documents → Rename (remove numbers) and categorize into `product/`, `architecture/`, and `adr/`.

### MERGE
- `docs/foundation/00-review-guide.md` and `07-review-and-change-process.md` → Merge into a single `docs/CONTRIBUTING.md` or `docs/foundation/review-process.md`.
- `docs/foundation/README.md` → Merge into the new root `docs/README.md`.

### ARCHIVE
- `docs/archive/phase-b/**` → Move to `docs/archive/phase-b/`.
- Obsolete root `docs/diagrams/` that contradict the new foundation.

### DELETE
- `docs/foundation/domains/` → Delete entirely. They are dangerous summaries that duplicate the authoritative `specifications/`. Readers should be routed directly to the specifications.
- `docs/foundation/` folder itself (once its contents are promoted/merged).

## Risks of Reorganization
- **Broken Links:** Moving files will break relative links across the markdown files (especially diagram links and cross-references between 01-17 and specs).
- **Git History Loss:** If files are moved without `git mv`, historical attribution might be disrupted.
- **Lost Context:** Over-aggressive deletion of 01-17 could destroy valuable product rationale not captured in the behavioral specs.

## Migration Sequence
1. Create `docs/README.md` as the permanent front door.
2. Create directories: `foundation/`, `product/`, `architecture/`, `adr/`, `archive/`.
3. Move `docs/archive/phase-b/` to `docs/archive/phase-b/`.
4. Move `docs/foundation/01` through `06` and its diagrams to `docs/foundation/`.
5. Integrate the review process docs into the foundation layer.
6. Delete `docs/foundation/domains/` and the empty `docs/foundation/` folder.
7. Categorize and move the 17 canonical docs into `product/`, `architecture/`, and `adr/`, stripping the leading numbers.
8. Run a global search-and-replace to fix all broken relative links.

## What Must NOT Change
- The **content and boundaries** of the 9 foundational behavioral specifications.
- The **decisions established** in the Phase-B models (Account Active ≠ Normal Access, Server Authority, Non-Cascading Governance, etc.).
- The **co-location** of domain-specific diagrams within their respective specification folders.

## Final Recommendation
Execute the Migration Sequence described above. This transforms the documentation from an organic, chronological file dump into a pedagogical, layered knowledge base. It eliminates the risk of `partner-review/` becoming a duplicate source of truth, preserves all historical evidence in `archive/`, and provides a seamless "Zero-to-Expert" reading journey starting from a single Front Door.
