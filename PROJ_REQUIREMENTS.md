## Project: Time Tracker (V2)

### 1. Purpose
This document translates the user stories from `PROJECT_SPECIFICATION.md` into formal, testable requirements.  
It defines *what the system must do* (functional requirements) and *how well it should perform* (non-functional requirements).  
Each requirement traces back to the corresponding User Story (US-xxx).

---

## 2. Functional Requirements

### Epic 1: User Management & Authentication

| ID | Requirement | Derived from |
|----|--------------|---------------|
| FR-101 | The system must allow registered users to authenticate using a username and password. | US-101 |
| FR-102 | The system must validate credentials and display an error for invalid login attempts. | US-101 |
| FR-103 | The system must terminate user sessions securely upon logout and redirect to the login page. | US-102 |
| FR-104 | Admin users must be able to create, view, update, and delete user accounts. | US-103 |
| FR-105 | Each user must have at least one assigned role. | US-103 |
| FR-106 | The system must prevent unauthorized access to restricted areas for unauthenticated users. | US-101, US-102 |

---

### Epic 2: Role-Based Access Control (RBAC)

| ID | Requirement | Derived from |
|----|--------------|---------------|
| FR-201 | The system must allow Admins to create, edit, and delete Roles and Rights (permissions). | US-201 |
| FR-202 | Each Role must support assignment of one or more Rights. | US-201 |
| FR-203 | The system must allow defining management relationships between Roles (e.g., Manager → Employee). | US-202 |
| FR-204 | The system must prevent a Role from managing itself. | US-202 |
| FR-205 | Access to all system operations must be governed by assigned Rights. | US-201, US-202 |

---

### Epic 3: Time Tracking Core

| ID | Requirement | Derived from |
|----|--------------|---------------|
| FR-301 | The system must record a check-in timestamp when a logged-in user initiates a check-in. | US-301 |
| FR-302 | The system must record a check-out timestamp when a user checks out. | US-301 |
| FR-303 | The interface must dynamically show the relevant button (“Check-in” or “Check-out”) depending on current status. | US-301 |
| FR-304 | Each time record must be associated with the authenticated user’s account. | US-301 |
| FR-305 | Users must be able to view their complete check-in/out history. | US-301 (implicit functional extension) |

---

### Epic 4: QR Code System

| ID | Requirement | Derived from |
|----|--------------|---------------|
| FR-401 | A unique QR code must be generated automatically when a user account is created. | US-401 |
| FR-402 | Each user must be able to view their unique QR code on their profile page. | US-401 |
| FR-403 | The system must allow a scanning interface that reads user QR codes and triggers automatic check-in/out. | US-402 |
| FR-404 | Upon scanning, the system must provide real-time feedback (success/error message). | US-402 |
| FR-405 | The system must reject invalid or unrecognized QR codes. | US-402 |

---

## 3. Non-Functional Requirements (NFR)

| ID | Requirement | Description |
|----|--------------|-------------|
| NFR-1 | **Security** | User passwords must be hashed using Django’s authentication system; all login and QR interactions must use HTTPS. |
| NFR-2 | **Scalability** | The application must support at least 500 concurrent users without significant delay in check-in/out operations. |
| NFR-3 | **Performance** | The check-in/out operation must complete (including DB write) within 2 seconds under normal load. |
| NFR-4 | **Maintainability** | Code must follow Django best practices, with modular apps for `auth`, `rbac`, and `time_tracking`. |
| NFR-5 | **Usability** | The UI must be responsive and clearly distinguish available actions (check-in vs check-out). |
| NFR-6 | **Auditability** | All check-in/out actions must be logged with timestamps and user identifiers. |
| NFR-7 | **Test Coverage** | Each major view/model must have ≥80% unit test coverage. |

---

## 4. Derived Data Model Requirements

| ID | Requirement | Source |
|----|--------------|--------|
| DR-1 | The database must store user profiles, roles, permissions, and relationships between them. | US-103, US-201, US-202 |
| DR-2 | The `CheckInCheckOut` model must include `user_id`, `check_in_time`, and `check_out_time` fields. | US-301 |
| DR-3 | The `QRCode` model must include a `UUID` and link to exactly one user. | US-401 |
| DR-4 | Each `ManagedRole` must define a `manager_role_id`, `managed_role_id`, and `rights[]`. | US-202 |

---

## 5. Backlog / Roadmap Overview

| Phase | Epic | Goal | Est. Duration |
|--------|------|------|---------------|
| Phase 1 | User Management & Auth | Basic authentication and user CRUD | * |
| Phase 2 | RBAC | Define role/permission system and enforcement | * |
| Phase 3 | Time Tracking Core | Manual check-in/out and time logs |* | 
| Phase 4 | QR System | Automated QR-based attendance | * |

> Each phase can be iterated and released incrementally.  
> Dependencies: Phase 1 → Phase 2 → Phase 3 → Phase 4.  

---

## 6. Traceability Matrix

| User Story | Related Requirement(s) |
|-------------|------------------------|
| US-101 | FR-101, FR-102, FR-106 |
| US-102 | FR-103 |
| US-103 | FR-104, FR-105 |
| US-201 | FR-201, FR-202, FR-205 |
| US-202 | FR-203, FR-204 |
| US-301 | FR-301, FR-302, FR-303, FR-304 |
| US-401 | FR-401, FR-402 |
| US-402 | FR-403, FR-404, FR-405 |

---

## 7. Acceptance Reference
All acceptance criteria defined in `PROJECT_SPECIFICATION.md` serve as test validation points for each Functional Requirement.  
Each FR shall be verified by a unit test and a manual UI test scenario before acceptance.


