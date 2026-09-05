# Master User Journey

> [!NOTE]  
> **Purpose:** Maps detailed state diagrams charting a user's path through the system.  
> **Prerequisites:** `03-nine-domain-map.md`  
> **Primary Audience:** Engineers, Product Managers, Designers.


This document outlines the standard path a user takes from first contact to normal platform access, alongside critical return behaviors.

To ensure clarity and avoid visual overload, the journey is separated into two focused diagrams:
1. **The Standard Onboarding Journey**: The chronological progression from initial registration to normal platform access.
2. **Return & Resume Routing**: How login routing, status checkpoints, and session interruptions behave.

### Diagram A: The Standard Onboarding Journey
This diagram illustrates the chronological progression of a user from registration through verification, institutional review, and community placement to normal platform access.

*(Reference Diagram:)*

```mermaid
flowchart TD
    classDef step fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#1e40af,font-weight:bold
    classDef decision fill:#fef08a,stroke:#ca8a04,stroke-width:2px,color:#854d0e,font-weight:bold
    classDef outcome fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#15803d,font-weight:bold

    subgraph Entry ["1. Entry & Authentication"]
        direction TB
        Reg["Registration<br/>(Account: Created)"]:::step
        Verify["Email Verification<br/>(OTP / Link)"]:::step
        Auth["Automatic Authentication<br/>(Session Issued)"]:::step

        Reg --> Verify
        Verify --> Auth
    end

    subgraph Onboard ["2. Academic Onboarding & Review"]
        direction TB
        Prof["Profile Completion<br/>(Personal & Academic Details)"]:::step
        Sub["Profile Submission"]:::step
        Pend["Pending Review<br/>(Awaiting Verification)"]:::step
        Appr{"Institutional<br/>Approval?"}:::decision

        Prof --> Sub
        Sub --> Pend
        Pend --> Appr
        Appr -.->|Rejected / Corrections| Prof
    end

    subgraph Placement ["3. Institutional Placement & Access"]
        direction TB
        Acc["Account: Active"]:::step
        Enr["Authoritative Enrollment"]:::step
        Ctx["Current Academic Context<br/>(Enrollment + Org + Time)"]:::step
        Comm["Base Community Assigned"]:::step
        Mem["Base Membership Granted"]:::step
        Access(((Normal Platform Access))):::outcome

        Enr --> Ctx
        Ctx --> Comm
        Comm --> Mem
        Mem --> Access
        Acc --> Access
    end

    Auth --> Prof
    Appr -->|Approved: Trigger Active| Acc
    Appr -->|Approved: Establish Record| Enr
```

### Diagram B: State-Aware Return and Resume Behavior
This diagram illustrates how login attempts and lifecycle events route returning users to their exact state without resetting progress.

*(Reference Diagram:)*

```mermaid
flowchart TD
    classDef trigger fill:#f8fafc,stroke:#64748b,stroke-width:2px,font-weight:bold
    classDef check fill:#fef08a,stroke:#ca8a04,stroke-width:2px,color:#854d0e,font-weight:bold
    classDef screen fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#1e40af
    classDef success fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#15803d,font-weight:bold
    classDef blocked fill:#fef2f2,stroke:#ef4444,stroke-width:2px,color:#991b1b,font-weight:bold

    subgraph Triggers ["1. Session & Lifecycle Triggers"]
        direction TB
        SessExp(["Session Expired / Logout"]):::trigger
        PassRec(["Password Reset Completed"]):::trigger
        SuspEvent(["Account Suspended"]):::trigger
    end

    subgraph Routing ["2. State-Aware Return Routing"]
        direction TB
        ReturnLogin(["User Returns & Logs In"]):::trigger
        CheckState{"Check Persistent<br/>Account State"}:::check
        ScreenVerify["Email Verification Screen<br/>(Prompt OTP)"]:::screen
        ScreenProfile["Profile Completion Screen<br/>(Resume / Correct Data)"]:::screen
        ScreenPending["Pending Review Status Screen<br/>(Access Blocked)"]:::blocked
        ScreenAccess(((Normal Platform Access))):::success
        ScreenSuspended["Suspension Notice<br/>(Login Denied)"]:::blocked

        ReturnLogin --> CheckState
        CheckState -->|Created & Unverified| ScreenVerify
        CheckState -->|Incomplete or Rejected| ScreenProfile
        CheckState -->|Pending Review| ScreenPending
        CheckState -->|Active & Enrolled| ScreenAccess
        CheckState -->|Suspended| ScreenSuspended
    end

    %% Trigger mappings
    SessExp -->|Invalidates session<br/>Progress preserved| ReturnLogin
    PassRec -->|Invalidates all sessions<br/>New credentials set| ReturnLogin
    SuspEvent -->|Invalidates all sessions<br/>Account locked| ScreenSuspended
```

## 1. The Standard Journey

**Registration**
The user submits initial identity credentials. The system creates the Account in a `Created` state.

**Verification**
An OTP or link is sent. The user proves ownership of the credential.

**Automatic Authentication**
Upon successful verification, the system issues an authenticated session, seamlessly transitioning the user into onboarding.

**Profile Completion**
The user provides required academic and personal information to build their Academic Profile.

**Submission**
The completed profile is submitted to the system, officially moving the onboarding state.

**Pending Review**
The profile awaits institutional verification.

**Approval**
An authorized reviewer (or automated institutional gate) approves the profile.

**Account Active**
The Approval triggers the Account Lifecycle to move the account state to `Active`.

**Enrollment**
The Approval simultaneously establishes the user's authoritative Enrollment record (academic attachment).

**Academic Context**
The Enrollment combines with Organization and Academic Time to form the user's Current Academic Context (e.g., University + Department + Level + Time).

**Base Community**
The system identifies the Community that matches the user's Academic Context.

**Base Membership**
The user is automatically granted membership in that Base Community.

**Normal Access**
With an Active Account, valid Session, authoritative Enrollment, established Academic Context, and Base Membership all in place, the user is granted Normal Platform Access.

---

## 2. Return & Resume Behavior

The system utilizes persistent, state-aware returns to ensure users are placed exactly where they left off, without destroying existing context.

- **Unverified return:** If a user registers but leaves before verifying, attempting to log in or return later will prompt the Verification step.
- **Incomplete return:** If a user verifies but drops off during profile completion, logging in resumes directly at Profile Completion.
- **Pending Review return:** If a user logs in while their profile is Pending Review, they see a status screen. They cannot access the normal platform.
- **Rejected return:** If a profile is rejected, logging in places the user back at Profile Completion (to make corrections), rather than suspending the account.
- **Active login:** A fully onboarded user logs in and goes straight to the normal platform experience.
- **Session expiration:** If a session expires, the user is logged out. Upon next login, their onboarding/enrollment state is perfectly preserved. Session expiration does **not** reset Onboarding or Enrollment.
- **Logout:** Explicit logout invalidates the session. Next login behaves like an Active login.
- **Password recovery:** "Forgot Password" triggers email OTP → user verifies OTP → sets New Password → confirms. **All existing sessions are invalidated.** The user must then Login with the new password.
- **Suspension:** If an Active Account is suspended, any active sessions are invalidated. The user is logged out. Future login attempts are explicitly denied with a suspension notice.
