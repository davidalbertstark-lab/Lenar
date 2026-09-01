# Lenar Foundation Overview

## What is Lenar?
Lenar is a platform built for university students to connect, stay informed, and participate in their academic community. It provides a secure environment where users log in, verify their official student status (Enrollment), and join groups based on their real-world university courses and departments (Base Community).

Lenar solves the problem of fragmented campus apps. Instead of using separate tools for logging in, finding groups, and managing student leadership roles, Lenar brings them together into one unified system. A student's official university record drives what they can see, join, and manage.

## The Product Model
The system operates on a core set of principles:
- **Server Authority:** The server decides what is true. The app (client) cannot bypass security rules.
- **University-Relative Context:** Lenar is flexible. Because every university is organized differently and uses different academic calendars, Lenar adapts to each university's unique structure.
- **Separation of Concerns:** To keep the system simple, Lenar is divided into nine clear behavioral domains (like Account Lifecycle, Organization, and Governance). Each domain handles one specific job.
- **Historical Preservation:** When a student graduates or a department changes its name, past records are not erased. Historical truth is protected.
- **Offline Resilience:** The platform works smoothly even on slow or unreliable internet connections, while still enforcing security when syncing with the server.

## Canonical References
To explore the original product vision, UX, and requirements, refer to the product documents:
- [01 Lenar Foundation](../product/01-Lenar-Foundation.md)
- [02 Problem, Users & Domain](../product/02-Problem-Users-Domain.md)
- [03 Product Requirements](../product/03-Product-Requirements.md)
- [07 Security, Privacy & Governance](../product/07-Security-Privacy-Governance.md)
