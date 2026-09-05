# Foundation Behavior Review

## What is Lenar?
Lenar is a platform built for university students to connect, stay informed, and participate in their academic community. 

This document explains how Lenar behaves behind that simple idea. It is designed to help our team and partners review the system's current rules, understand how a user moves through the platform, and see where authority and boundaries exist. The goal is to make it easy for you to review the current model and say, "I agree with this," or "I think this part should change."

---

## SECTION 1 — THE WHOLE SYSTEM

Lenar is designed to ensure that a student's official university record drives what they can see, join, and manage. Here is a simple picture of the major journey a student takes:

**The Major Journey:**
Registration 
→ Account Created 
→ Email Verification 
→ Authentication / Session 
→ Onboarding 
→ Academic Profile 
→ Submission 
→ Pending Review 
→ Approval 
→ Account Active + Enrollment 
→ Current Academic Context 
→ Base Community 
→ Base Membership 
→ Normal Platform Access

**The Authority Path:**
Governance 
→ Role + Authority Context 
→ Authorization 
→ Allow / Deny

This means a user must be approved to become an active student. Once approved, the system uses their verified academic details to automatically place them in the correct academic community. If they are granted a leadership role, the system uses strict rules to check exactly what they are allowed to do.

---

## SECTION 2 — THE NINE BEHAVIOURAL AREAS

Lenar is divided into nine clear areas (domains) to keep the system organized and secure. 

### 1. Account Lifecycle
- **What it is:** The timeline of a user's account from creation to closure.
- **What it controls:** Whether an account is Created, Active, Suspended, or Closed.
- **Current behavior:** An account only becomes "Active" after a student's submitted profile is formally approved.
- **What it does NOT control:** It does not control temporary login sessions or specific permissions.
- **Review prompt:** Should approval really be the exact point where the account becomes Active? 
- **Canonical Specification:** [Account Lifecycle](../03-specifications/account-lifecycle/account-lifecycle-specification.md)

### 2. Authentication
- **What it is:** Proving who you are and keeping you securely logged in.
- **What it controls:** Login, password reset, and active sessions.
- **Current behavior:** Successfully logging in grants a temporary session. If a session expires, you must log in again.
- **What it does NOT control:** Email verification does not activate the account, and authentication does not check permissions.
- **Review prompt:** Is it clear that verifying an email address is just an authentication step and does not grant platform access?
- **Canonical Specification:** [Authentication](../03-specifications/authentication/authentication-specification.md)

### 3. Onboarding
- **What it is:** The process of a new user building their academic profile.
- **What it controls:** Profile drafts, submission, pending review, and final approval/rejection.
- **Current behavior:** A user submits their academic details. The system locks it in "Pending Review" until a decision is made.
- **What it does NOT control:** Rejection does not suspend or delete the account; it just sends the user back to fix their submission.
- **Review prompt:** Does the transition from Pending Review to Approved/Rejected make sense?
- **Canonical Specification:** [Onboarding](../03-specifications/onboarding/onboarding-specification.md)

### 4. Organization
- **What it is:** The structure of a university (faculties, departments, etc.).
- **What it controls:** The valid academic units that a student can belong to.
- **Current behavior:** Because every university is different, organizational structure is strictly "University-relative." There is no universal, rigid hierarchy.
- **What it does NOT control:** It does not dictate how communities function on the platform.
- **Review prompt:** Do we agree that the platform shouldn't force every university into the exact same organizational hierarchy?
- **Canonical Specification:** [Organization](../03-specifications/organization/organization-specification.md)

### 5. Academic Time
- **What it is:** How a university divides the calendar (semesters, terms, academic years).
- **What it controls:** The current effective academic period versus future planned periods.
- **Current behavior:** The system separates future "configured" academic time from the "current effective" academic time.
- **What it does NOT control:** Moving time forward (e.g., starting a new semester) does not automatically promote students to a new level.
- **Review prompt:** Should advancing Academic Time be completely separate from student promotion?
- **Canonical Specification:** [Academic Time](../03-specifications/academic-time/academic-time-specification.md)

### 6. Enrollment
- **What it is:** The official record connecting a student to the university.
- **What it controls:** A student's authoritative academic attachment and their "Current Academic Context" (their university, department, and level).
- **Current behavior:** Enrollment is continuous. Moving from 300L to 400L updates the Current Academic Context but does not create a brand-new enrollment record.
- **What it does NOT control:** It does not control community creation.
- **Review prompt:** Does a single, continuous Enrollment record per student per university make sense for progression?
- **Canonical Specification:** [Enrollment](../03-specifications/enrollment/enrollment-specification.md)

### 7. Community
- **What it is:** The spaces where students interact and participate.
- **What it controls:** A student's "Base Community" (University + Department + Level) and their "Base Membership."
- **Current behavior:** The system automatically maps a student's Current Academic Context to a matching Base Community. Users cannot manually join or leave their Base Community.
- **What it does NOT control:** Community does not control academic truth or governance roles.
- **Review prompt:** Should users be strictly locked into the Base Community dictated by their official academic context?
- **Canonical Specification:** [Community](../03-specifications/community/community-membership-specification.md)

### 8. Governance
- **What it is:** The system of roles and authority.
- **What it controls:** Who is a Leader, Admin, or Manager, and where their authority applies (Authority Context).
- **Current behavior:** Governance assignments consist of a User, a Role, and an Authority Context. Revoking a role is non-cascading (it does not automatically delete everything that person did or assigned).
- **What it does NOT control:** Being a member of a community does not automatically grant governance authority.
- **Review prompt:** Do we agree that removing a Leader should not automatically fire all the Managers they hired?
- **Canonical Specification:** [Governance](../03-specifications/governance/governance-specification.md)

### 9. Authorization
- **What it is:** The strict security check that happens right before an action is performed.
- **What it controls:** Evaluating the user, their role, their scope, the current context, and the requested action to return ALLOW or DENY.
- **Current behavior:** Default Deny. If any piece is missing, mismatched, or revoked, the server denies the action. 
- **What it does NOT control:** It does not assign roles; it only enforces them.
- **Review prompt:** Does the strict matching of Scope and Context provide the right level of security?
- **Canonical Specification:** [Authorization](../03-specifications/authorization/authorization-specification.md)

---

## SECTION 3 — USERS, ACCOUNT, AND ENTRY

The journey from a visitor to an active student is strictly controlled.

1. **Registration:** A user signs up. The account is **Created**.
2. **Email Verification:** The user proves they own their email. The account is still only **Created**.
3. **Authentication:** The user logs in and receives a temporary **Session**.
4. **Onboarding:** The user fills out their academic profile.
5. **Submission:** The user submits the profile for review. The state becomes **Pending Review**.
6. **Review Decision:**
   - **Rejection:** The user is sent back to Onboarding to fix errors. Rejection is *not* Account Suspension.
   - **Approval:** The system accepts the academic profile.
7. **Active Account:** Only upon Approval does the account become **Active**, establishing an official Enrollment.

**Important Note:** Email verification does NOT make the account Active. "Pending Review" does NOT mean the account is suspended. 

---

## SECTION 4 — ACADEMIC IDENTITY

Academic identity in Lenar revolves around **Enrollment** and **Current Academic Context**.

- **Organization (University):** Each university has its own structure. Lenar does not force a rigid "Faculty → Department → Course" tree on every institution. 
- **Enrollment:** This is a student's authoritative academic attachment to the university.
- **Current Academic Context:** This describes exactly where the student is right now, primarily their University, Department, and **Level** (e.g., 300L, 400L).

**Progression and Levels:**
When a student moves from 300L Semester 2 to 400L Semester 1, their Current Academic Context updates. This continues their existing, active Enrollment—it does *not* create a new enrollment. 

**Carryover Courses:**
A student taking a carryover or repeated course does NOT automatically drop to a lower Level. Their Level reflects their overall academic standing. 

Furthermore, academic progression does not automatically revoke a student's Governance roles.

---

## SECTION 5 — COMMUNITY

Communities are where interaction happens. A **Base Community** is the core space built around a specific context: **University + Department + Level**.

- **Membership:** When a student's Current Academic Context matches a Base Community, they are automatically granted **Base Membership**. 
- **Movement:** Because Membership is tied to academic truth, users cannot manually leave or join their Base Community. If their Current Academic Context changes (e.g., they progress to the next Level), their Base Membership follows them to the new Base Community.
- **Missing Base Community:** If a student is enrolled, but the specific Base Community does not exist yet in the system, this does NOT invalidate or reject their Enrollment. Instead, normal platform access is blocked until the appropriate Base Community exists and matching users receive their Base Membership.

---

## SECTION 6 — ROLES AND GOVERNANCE

Governance establishes who has authority and where.

**The Roles:**
- **Super Admin:** Has platform-wide authority. They administer the system and assign Admins to universities.
- **Admin:** Has University-scoped authority. Assigned by a Super Admin to oversee a specific University. They assign Leaders.
- **Leader:** Has Base Community-scoped authority. Assigned by an Admin to lead a specific Base Community. 
  - *Eligibility:* To be a Leader, a candidate's current authoritative academic context must exactly match the target Base Community's University, Department, and Level.
- **Subordinate Roles (Sub-Leader / Manager / Writer):** Operational roles within a Base Community. Assigned by the Leader.
  - *Eligibility:* The candidate must currently belong to (be a member of) the target Base Community.

**Important Distinctions:**
- **Governance Assignment = User + Role + Authority Context.**
- **Membership ≠ Governance.** A user being a member of a community does not automatically mean they have governance authority.
- **Governance ≠ Authorization.** Governance establishes who has authority and where. Authorization strictly checks that authority when a user tries to do something.

---

## SECTION 7 — AUTHORIZATION

Authorization strictly determines what a person can actually do. 

When a user tries to perform an action, the server checks:
**Authenticated Actor + Role + Scope + Context + Resource + Operation → ALLOW / DENY**

**The Rules of Authorization:**
- The default is always **Deny**.
- Missing authority means **Deny**.
- Scope mismatch (trying to act outside your assigned level) means **Deny**.
- Context mismatch (trying to act outside your specific department or university) means **Deny**.
- Revoked authority means **Deny**.
- The server is always authoritative.

**Simple Examples:**
- A Leader in the Computer Science 300L Community should not automatically have Leader authority in the Mathematics 300L Community.
- An Admin assigned to University A should not automatically administer University B.

---

## SECTION 8 — TIME AND CHANGE

**Academic Time** determines the university calendar (sessions, semesters, terms).

- **Configured vs. Current:** A university may have a "Configured" future academic period planned out, but the system relies on the "Current effective" academic period for active rules. 
- **Advancing Time:** Advancing Academic Time to a new semester does NOT automatically promote every student. Student progression determines their individual academic level progression.

**Historical Truth:**
The system preserves historical truth rather than silently rewriting the past. If a department changes its name, past records reflect the historical reality.

---

## SECTION 9 — IMPORTANT STATE CHANGES

It is critical to remember that these are separate state systems. They are not one giant state machine.

| Domain | Example State Transition | Description |
|---|---|---|
| **Account** | Created → Active | Happens only upon Onboarding Approval. |
| **Account** | Active → Suspended | Platform access is blocked, but historical data remains intact. |
| **Onboarding** | Draft → Pending Review | User submits profile; awaits decision. |
| **Onboarding** | Pending Review → Rejected | User must fix submission errors (Account remains Created). |
| **Academic** | Level 300L → Level 400L | Current Level changes; the exact same Enrollment continues. |
| **Community** | Base Context Updates | Current Academic Context changes → Base Community changes → Base Membership follows. |
| **Governance** | Granted / Revoked | Assignments are created or revoked independently of general membership. |

---

## SECTION 10 — IMPORTANT "WHAT DOES NOT HAPPEN" RULES

Understanding what Lenar specifically rejects is just as important as knowing what it allows.

- Email verification does **NOT** activate the account.
- Rejection does **NOT** mean Account Suspension.
- Session expiry does **NOT** reset onboarding.
- Session expiry does **NOT** erase enrollment.
- Carryover courses do **NOT** change Level.
- Academic progression does **NOT** create a new Enrollment.
- Academic progression does **NOT** automatically revoke Governance.
- Membership does **NOT** automatically grant governance authority.
- Missing Base Community does **NOT** invalidate Enrollment.
- Revoking a Leader does **NOT** automatically revoke every subordinate assignment.
- Revoking an Admin does **NOT** automatically erase assignments they previously made (non-cascading revocation).
- Organization changes do **NOT** silently rewrite historical Enrollment.
- Organization changes do **NOT** automatically delete Communities.
- Organization changes do **NOT** automatically revoke Governance.
- Closed Account does **NOT** mean immediate physical deletion.
- Client/offline state **cannot** manufacture authoritative server state.

---

## SECTION 11 — CROSS-DOMAIN BEHAVIOURAL EXAMPLES

**Example 1 — Normal new student**
Registration → email verification → onboarding → pending review → approval (Account becomes Active) → enrollment established → academic context mapped → base community found → membership granted → normal platform access.

**Example 2 — Student changes Level**
A student moves from 300L to 400L. Their Enrollment remains exactly the same. Their Current Academic Context updates to 400L. Their Base Membership moves to the 400L Base Community. 

**Example 3 — Student has a carryover**
A 400L student takes a 300L carryover course. The course does not cause a Level rollback. The student remains at the 400L Level and their Base Community remains the 400L Base Community.

**Example 4 — Base Community does not exist yet**
A student is approved for 100L Physics, but the 100L Physics Base Community hasn't been created yet. Their Enrollment is completely valid. However, their normal platform access is paused until the required Base Community exists.

**Example 5 — Leader assignment**
An Admin assigns a Leader to the 300L Law Community. The candidate must be a 300L Law student. The assignment creates Governance Authority strictly scoped to the 300L Law context.

**Example 6 — Admin scope**
An Admin is assigned to University A. If they attempt to modify University B, Authorization evaluates their assignment context (University A), sees a mismatch with the target resource (University B), and strictly returns DENY.

**Example 7 — Session expires**
A student is filling out their profile and their session expires. Authentication state is lost, but they simply log back in. Their onboarding data and historical state remain completely intact.

**Example 8 — Account suspension**
A student's account is Suspended. Normal access is blocked, and active sessions are destroyed. However, their historical academic records and past governance actions remain preserved in the system.

---

## SECTION 12 — DECISIONS WE ARE CURRENTLY REVIEWING

This is a list of the important existing decisions that the team should consciously review. 

### When Account becomes Active
- **Current behavior:** The account transitions from Created to Active only upon Onboarding Approval.
- **Why it currently works this way:** It ensures unverified users cannot bypass academic requirements to access platform features.
- **Example:** A registered user cannot browse communities until the university approves their student status.
- **Things to question:** Should an account be active before approval with restricted features, or is a strict barrier better?
- **Review status:** Open
- **Canonical specification:** [Account Lifecycle](../03-specifications/account-lifecycle/account-lifecycle-specification.md)

### Relationship between Approval and Enrollment
- **Current behavior:** Approval simultaneously activates the account and establishes the authoritative Enrollment.
- **Why it currently works this way:** An active student inherently requires a valid academic attachment.
- **Example:** Approving an onboarding submission instantly sets the user's university, department, and level.
- **Things to question:** Should Enrollment be decoupled from account activation? 
- **Review status:** Open
- **Canonical specification:** [Enrollment](../03-specifications/enrollment/enrollment-specification.md)

### University-relative Organization
- **Current behavior:** Organizational structure (faculties, departments) is determined by each specific university rather than a forced global tree.
- **Why it currently works this way:** Universities differ wildly; imposing a rigid universal hierarchy fails in the real world.
- **Example:** University A uses "Faculty of Arts" while University B uses "College of Humanities." Both are supported.
- **Things to question:** Does this create too much complexity for cross-university analytics? 
- **Review status:** Open
- **Canonical specification:** [Organization](../03-specifications/organization/organization-specification.md)

### Academic Level and Base Community
- **Current behavior:** A student's Base Community is dictated by their Level, and taking a carryover course does not change their Level or Base Community.
- **Why it currently works this way:** A student's primary social and academic cohort is defined by their overall standing, not a single failed class.
- **Example:** A 400L student taking a 300L class stays in the 400L Base Community.
- **Things to question:** Do students need simultaneous primary memberships in multiple levels?
- **Review status:** Open
- **Canonical specification:** [Community](../03-specifications/community/community-membership-specification.md)

### Missing Base Community
- **Current behavior:** If a required Base Community does not exist, Enrollment remains valid but normal access is blocked.
- **Why it currently works this way:** We do not invalidate academic truth just because a community container hasn't been instantiated yet.
- **Example:** A new department is added, students are approved, but the community hasn't been initialized. Students are enrolled but wait for access.
- **Things to question:** Should the system automatically instantiate missing Base Communities on demand?
- **Review status:** Open
- **Canonical specification:** [Community](../03-specifications/community/community-membership-specification.md)

### Non-Cascading Governance Revocation
- **Current behavior:** Revoking a leader's role does not automatically delete the subordinate assignments or content they created.
- **Why it currently works this way:** It preserves operational continuity and historical truth. Firing a manager shouldn't erase the department's work.
- **Example:** A Leader is removed. The Sub-Leaders they appointed remain in place until reviewed.
- **Things to question:** Does this leave too many orphaned permissions if a malicious leader is removed?
- **Review status:** Open
- **Canonical specification:** [Governance](../03-specifications/governance/governance-specification.md)

---

## SECTION 13 — OPEN / UNCLEAR / DEFERRED AREAS

*Only areas genuinely unresolved in the canonical documentation are listed here.*

### Physical Data Deletion (Account Closure)
- **What is currently known:** The "Closed" account state logically deactivates the user and prevents all access.
- **What is intentionally not yet defined:** The exact timeline, GDPR compliance mechanics, and database sweeping mechanics for physical data deletion.
- **Why it is deferred:** Platform infrastructure and legal compliance tools will dictate the safest physical deletion mechanics in a later technical phase.

---

## SECTION 14 — HOW A CHANGE SHOULD HAPPEN

If you identify a problem or have an improvement during this review:
1. You propose a change to the behavioural model.
2. The team discusses the change and its cross-domain impacts.
3. A final decision is made.
4. The appropriate **canonical specification** is officially updated.
5. All affected domains and specifications are audited for consistency.
6. This review document is then updated to reflect the new current model.

*This review document is a collaboration surface, not the place where formal behavioural rules are finalized or stored.*
