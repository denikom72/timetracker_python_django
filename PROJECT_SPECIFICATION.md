# Project Specification: AI-Powered Time Tracker (V2)

## 1. Project Overview

**Project Name:** Time Tracker
**Goal:** To develop a robust, scalable, and user-friendly time tracking application using Django and PostgreSQL. The system will support manual and QR code-based check-in/out, provide a detailed time history for users, and feature a sophisticated Role-Based Access Control (RBAC) system for granular permission management.
**Target Audience:** Businesses requiring employee time tracking, fitness centers, or any organization needing to log presence in a specific location.

---

## 2. Estimation Methodology

### Story Points
This project uses **Story Points (SP)** for estimation. A Story Point is an abstract unit of measure that represents the overall effort required to implement a piece of work. It accounts for:
-   **Complexity:** How difficult is the work to implement?
-   **Uncertainty:** How much is unknown about the requirements?
-   **Volume of Work:** How much is there to do?

### Time Conversion
For planning purposes, we will use the following approximate conversion:
**1 Story Point ≈ 0.5 Person-Days of work.**
This means a 2 SP task is expected to take one full day for a single developer.

---

## 3. Project Summary & Timeline

| Epic                          | Total Story Points | Estimated Person-Days |
|-------------------------------|--------------------|-----------------------|
| User Management & Auth        | 8 SP               | 4 Days                |
| Role-Based Access Control     | 21 SP              | 10.5 Days             |
| Time Tracking Core            | 16 SP              | 8 Days                |
| QR Code System                | 13 SP              | 6.5 Days              |
| **TOTALS**                    | **58 SP**          | **29 Person-Days**    |

---

## 4. Detailed User Stories, Acceptance Criteria & Subtasks

### **Epic 1: User Management & Authentication**

---

#### **US-101: User Login**
-   **User Story:** As a registered user, I want to log in with my username and password so that I can access the system.
-   **Estimation Breakdown:**
    -   **Development:** 1 SP
    -   **Testing:** 1 SP
    -   **Total:** 2 SP (~1 Day)
-   **Acceptance Criteria:**
    1.  **Given** I am on the login page, **when** I enter valid credentials and click "Login", **then** I am redirected to my dashboard/index page.
    2.  **Given** I am on the login page, **when** I enter invalid credentials, **then** an error message is displayed, and I remain on the login page.
-   **Technical Subtasks:**
    -   **Development:**
        -   `views.py`: Implement `user_login` view using Django's `AuthenticationForm`.
        -   `urls.py`: Add URL pattern for the login view.
        -   `templates/tracker/login.html`: Create the login form template.
        -   `templates/tracker/base.html`: Ensure base template supports displaying messages for login errors.
    -   **Testing:**
        -   `tests.py`: Write a unit test to verify that a user with valid credentials can log in successfully (HTTP 200 -> 302 redirect).
        -   `tests.py`: Write a unit test to verify that a user with invalid credentials sees an error and is not logged in (HTTP 200).

---

#### **US-102: User Logout**
-   **User Story:** As a logged-in user, I want to log out of the system to end my session securely.
-   **Estimation Breakdown:**
    -   **Development:** 0.5 SP
    -   **Testing:** 0.5 SP
    -   **Total:** 1 SP (~0.5 Days)
-   **Acceptance Criteria:**
    1.  **Given** I am logged in, **when** I click the "Logout" link/button, **then** my session is terminated, and I am redirected to the login or index page.
-   **Technical Subtasks:**
    -   **Development:**
        -   `views.py`: Implement `user_logout` view using Django's `logout` function.
        -   `urls.py`: Add URL pattern for the logout view.
        -   `templates/tracker/base.html`: Add a logout button/link that is only visible to authenticated users.
    -   **Testing:**
        -   `tests.py`: Write a unit test to verify a logged-in user is successfully logged out and redirected.

---

#### **US-103: Admin User Management (CRUD)**
-   **User Story:** As an Admin, I want to create, read, update, and delete users via the Django Admin panel so that I can manage system access.
-   **Estimation Breakdown:**
    -   **Development:** 3 SP
    -   **Testing:** 2 SP
    -   **Total:** 5 SP (~2.5 Days)
-   **Acceptance Criteria:**
    1.  **Given** I am an Admin, **when** I navigate to the admin panel, **then** I can see a list of all users.
    2.  **Given** I am an Admin, **when** creating a new user, **then** I can assign one or more roles to them.
    3.  **Given** I am an Admin, **when** editing a user, **then** I can modify their details and role assignments.
-   **Technical Subtasks:**
    -   **Development:**
        -   `models.py`: Define `CustomUser` model inheriting from `AbstractUser`, add `roles` ManyToManyField.
        -   `settings.py`: Set `AUTH_USER_MODEL = 'tracker.CustomUser'`.
        -   `admin.py`: Register `CustomUser` with a custom `UserAdmin` class.
        -   `admin.py`: Use `fieldsets` or `filter_horizontal` to make role assignment user-friendly in the admin panel.
    -   **Testing:**
        -   `tests.py`: Write a test to create a user programmatically and verify role assignment works.
        -   Manual Test: Document steps to verify CRUD functionality for `CustomUser` in the Django Admin UI.

---

### **Epic 2: Role-Based Access Control (RBAC)**

---

#### **US-201: Admin Role & Permission Management (CRUD)**
-   **User Story:** As an Admin, I want to create, read, update, and delete Roles and Rights (permissions) in the admin panel.
-   **Estimation Breakdown:**
    -   **Development:** 3 SP
    -   **Testing:** 2 SP
    -   **Total:** 5 SP (~2.5 Days)
-   **Acceptance Criteria:**
    1.  **Given** I am an Admin, **when** I go to the admin panel, **then** I can create a new role (e.g., "Manager", "Employee").
    2.  **Given** I am an Admin, **when** I go to the admin panel, **then** I can create a new right (e.g., "create_user", "delete_entry").
-   **Technical Subtasks:**
    -   **Development:**
        -   `models.py`: Implement `Role` and `Right` models with `name` fields.
        -   `admin.py`: Register `Role` and `Right` models with the Django admin.
    -   **Testing:**
        -   `tests.py`: Write model tests to verify `Role` and `Right` objects can be created and saved correctly.
        -   Manual Test: Document steps to verify CRUD functionality for `Role` and `Right` in the Django Admin UI.

---

#### **US-202: Admin Permission Assignment**
-   **User Story:** As an Admin, I want to define what actions a "manager" role can perform on a "managed" role.
-   **Estimation Breakdown:**
    -   **Development:** 5 SP
    -   **Testing:** 3 SP
    -   **Total:** 8 SP (~4 Days)
-   **Acceptance Criteria:**
    1.  **Given** I am an Admin, **when** I am managing roles, **then** I can specify that a `manager` role has `create` and `update` rights over an `employee` role.
    2.  The system must prevent illogical assignments, such as a role managing itself.
-   **Technical Subtasks:**
    -   **Development:**
        -   `models.py`: Implement the `ManagedRole` model with ForeignKeys to `Role` and a ManyToManyField to `Right`.
        -   `admin.py`: Register `ManagedRole` model. Use a clear representation (e.g., `__str__` method) to show the relationship.
        -   `models.py`: Add validation to the `ManagedRole` model's `save` method to prevent a role from managing itself.
    -   **Testing:**
        -   `tests.py`: Write a model test to create a `ManagedRole` relationship and assign rights.
        -   `tests.py`: Write a test to ensure the self-management validation logic works correctly and raises an error.

---

### **Epic 3: Time Tracking Core Functionality**

---

#### **US-301: Manual Check-in / Check-out**
-   **User Story:** As a logged-in user, I want to click a "Check-in" button to record my arrival time and a "Check-out" button to record my departure time.
-   **Estimation Breakdown:**
    -   **Development:** 2 SP
    -   **Testing:** 1 SP
    -   **Total:** 3 SP (~1.5 Days)
-   **Acceptance Criteria:**
    1.  **Given** I am logged in and not checked in, **when** I click "Check-in", **then** a new `CheckInCheckOut` entry is created.
    2.  **Given** I am checked in, **when** I click "Check-out", **then** my current entry is updated with the `check_out_time`.
    3.  The UI only shows the relevant button ("Check-in" or "Check-out").
-   **Technical Subtasks:**
    -   **Development:**
        -   `models.py`: Implement the `CheckInCheckOut` model.
        -   `views.py`: Create a view (`toggle_check_in_out`) to handle the logic. It should find the user's last entry and either create a new one or update the existing one.
        -   `urls.py`: Add a URL for the new view.
        -   `views.py`: Update the `index` view to pass the user's current check-in status to the template.
        -   `templates/tracker/index.html`: Add a form/button and use template logic (`{% if %}`) to show the correct button based on the user's status.
    -   **Testing:**
        -   `tests.py`: Write a test for the `toggle_check_in_out` view to verify a new object is created on the first call for a user.
        -   `tests.py`: Write a test to verify the `check_out_time` is set on the second call.

---

### **Epic 4: QR Code System**

---

#### **US-401: System Generates Unique QR Codes**
-   **User Story:** As a user, I want the system to generate a unique, permanent QR code for my account so I can use it for scanning.
-   **Estimation Breakdown:**
    -   **Development:** 3 SP
    -   **Testing:** 2 SP
    -   **Total:** 5 SP (~2.5 Days)
-   **Acceptance Criteria:**
    1.  **Given** a new user is created, **when** their account is saved, **then** a unique `QRCode` object is automatically generated and associated with them.
    2.  **Given** I am a logged-in user, **when** I navigate to my profile page, **then** I can see my personal QR code displayed as an image.
-   **Technical Subtasks:**
    -   **Development:**
        -   `models.py`: Implement the `QRCode` model with a `UUIDField` and a OneToOne relationship to `CustomUser`.
        -   `models.py`: Use a Django signal (e.g., `post_save` on `CustomUser`) to automatically create a `QRCode` instance for each new user.
        -   Install a QR code generation library (e.g., `qrcode`).
        -   `views.py`: Create a `profile` view that retrieves the user's QR code UUID and uses the library to generate a QR code image data URI.
        -   `templates/tracker/profile.html`: Create a template to display the user's profile information and the generated QR code image.
        -   `urls.py`: Add a URL for the `profile` view.
    -   **Testing:**
        -   `tests.py`: Write a test to verify the `post_save` signal works and a `QRCode` is created when a `CustomUser` is created.
        -   `tests.py`: Write a test for the `profile` view to ensure it returns a 200 status code for a logged-in user.

---

#### **US-402: Check-in / Check-out via QR Code Scan**
-   **User Story:** As a user, I want to scan my personal QR code at a designated station to automatically check-in or check-out.
-   **Estimation Breakdown:**
    -   **Development:** 5 SP
    -   **Testing:** 3 SP
    -   **Total:** 8 SP (~4 Days)
-   **Acceptance Criteria:**
    1.  **Given** a dedicated scanning interface, **when** my QR code is scanned and I am currently checked out, **then** I am automatically checked in.
    2.  **Given** the same interface, **when** my QR code is scanned and I am currently checked in, **then** I am automatically checked out.
    3.  The system provides clear visual feedback (e.g., "Welcome, [Username]!" or "Goodbye, [Username]!") upon a successful scan.
-   **Technical Subtasks:**
    -   **Development:**
        -   `views.py`: Create an API-like view (`qr_scan_handler`) that accepts a POST request with the QR code UUID.
        -   `views.py`: Implement the logic in this view to find the user, check their latest `CheckInCheckOut` status, and perform the toggle action (same logic as `toggle_check_in_out`).
        -   `urls.py`: Add a URL for the `qr_scan_handler` view.
        -   `templates/tracker/scanner.html`: Create a simple page for the scanning station.
        -   `static/js/scanner.js`: Add JavaScript to the scanner page to access the camera (e.g., using the `html5-qrcode` library), scan for a QR code, and send the result to the backend via an AJAX POST request.
        -   `static/js/scanner.js`: Implement logic to display the success/error message returned from the backend.
    -   **Testing:**
        -   `tests.py`: Write an API-style test for the `qr_scan_handler` view, simulating POST requests with a valid UUID and verifying the check-in/out logic.
        -   `tests.py`: Test the view's response for an invalid/unknown UUID.
        -   Manual Test: Document the steps to perform an end-to-end test using a physical device (or webcam) on the scanner page.


____________________________________________________________________


##
improved USER STORIES wiht ROBUST ACCEPTANCE CRITERIA ( HEAPY PATH, ERROR HANDLING, EDGE CASES/VALIDATON, CONSTRAINS/FORBIDDEN ACTIONS ) AND CLEAR TASKs/SUBTASKS FOR DEVs
##


Epic 1: User Management & Authentication
US-101: User Login

User Story:
As a registered user, I want to log in with my username and password so that I can access the system.

Acceptance Criteria:
Happy Path:

    Enter valid username/password → redirect to dashboard → show welcome message.

    Logout ends session → redirect to login page.

Edge Cases / Validation:

    Username field empty → show error “Username is required”.

    Password field empty → show error “Password is required”.

    Username with invalid chars → show “Invalid username format”.

    Password <8 chars → show “Password too short”.

Error Handling:

    Wrong credentials → “Invalid username or password”.

    Locked user → “Account locked”.

    System unavailable → “Service temporarily unavailable”.

Constraints / Forbidden Actions:

    Logged-out users cannot access dashboard → redirect to login.

    Locked accounts cannot log in.

Tasks / Subtasks (Jira-style):

    DEV-101.1 Implement login view (views.py)

    DEV-101.2 Add URL route for login (urls.py)

    DEV-101.3 Create login template (login.html)

    DEV-101.4 Implement session logout (logout)

    DEV-101.5 Unit tests for valid login

    DEV-101.6 Unit tests for invalid login / edge cases

    DEV-101.7 Manual QA checklist

US-102: User Logout

User Story:
As a logged-in user, I want to log out securely to end my session.

Acceptance Criteria:

    Click logout → session terminated → redirect to login page.

    Attempt to access dashboard after logout → redirected to login.

Tasks / Subtasks:

    DEV-102.1 Implement logout view (views.py)

    DEV-102.2 Add logout button in templates (base.html)

    DEV-102.3 Unit tests for logout functionality

    DEV-102.4 Manual QA checklist

US-103: Admin User Management (CRUD)

User Story:
As an Admin, I want to create, read, update, and delete users via the Django Admin panel so that I can manage system access.

Acceptance Criteria:
Happy Path:

    Admin sees user list in admin panel.

    Admin can create user and assign roles.

    Admin can edit user details and roles.

    Admin can delete users.

Edge Cases / Validation:

    Attempt to create user with existing username → show error.

    Invalid email or empty mandatory fields → show error.

Constraints / Forbidden Actions:

    Non-admin users cannot access admin panel.

Tasks / Subtasks:

    DEV-103.1 Define CustomUser model (models.py)

    DEV-103.2 Register CustomUser in admin (admin.py)

    DEV-103.3 Add role assignment UI (fieldsets or filter_horizontal)

    DEV-103.4 Unit tests for CRUD operations

    DEV-103.5 Manual QA checklist

Epic 2: Role-Based Access Control (RBAC)
US-201: Admin Role & Permission Management (CRUD)

User Story:
As an Admin, I want to create, read, update, and delete Roles and Rights in the admin panel.

Acceptance Criteria:
Happy Path:

    Admin can create roles (Manager, Employee).

    Admin can create rights (create_user, delete_entry).

    Admin can update or delete roles/rights.

Edge Cases / Validation:

    Duplicate role/right name → show error.

    Attempt to delete role currently assigned to users → error.

Constraints / Forbidden Actions:

    Non-admins cannot manage roles or rights.

Tasks / Subtasks:

    DEV-201.1 Implement Role and Right models

    DEV-201.2 Register models in admin (admin.py)

    DEV-201.3 Unit tests for role/right CRUD

    DEV-201.4 Manual QA checklist

US-202: Admin Permission Assignment

User Story:
As an Admin, I want to define what actions a "manager" role can perform on a "managed" role.

Acceptance Criteria:
Happy Path:

    Admin assigns rights for a manager over employee.

    Manager can only perform assigned actions.

Edge Cases / Validation:

    Manager cannot manage themselves.

    Invalid assignment → error.

Constraints / Forbidden Actions:

    Only admin can assign permissions.

Tasks / Subtasks:

    DEV-202.1 Implement ManagedRole model with ForeignKeys + ManyToMany to Rights

    DEV-202.2 Validation: role cannot manage itself

    DEV-202.3 Admin UI for managing assignments

    DEV-202.4 Unit tests for assignment logic

    DEV-202.5 Manual QA checklist

Epic 3: Time Tracking Core Functionality
US-301: Manual Check-in / Check-out

User Story:
As a logged-in user, I want to click a "Check-in" button to record my arrival time and a "Check-out" button to record my departure.

Acceptance Criteria:
Happy Path:

    Click “Check-in” → new entry created.

    Click “Check-out” → update entry with check_out_time.

Edge Cases / Validation:

    Double check-in → error “Already checked in”.

    Check-out without check-in → error “Cannot check out without check-in”.

Constraints / Forbidden Actions:

    Cannot check in/out for another user.

Tasks / Subtasks:

    DEV-301.1 Implement CheckInCheckOut model

    DEV-301.2 Implement toggle_check_in_out view

    DEV-301.3 Add URL route (urls.py)

    DEV-301.4 Update template (index.html)

    DEV-301.5 Unit tests for check-in/out logic

    DEV-301.6 Manual QA checklist

Epic 4: QR Code System
US-401: System Generates Unique QR Codes

User Story:
As a user, I want the system to generate a unique QR code for my account so I can use it for scanning.

Acceptance Criteria:
Happy Path:

    New user → QR code generated → displayed in profile.

Edge Cases / Validation:

    Duplicate QR generation → error.

    Invalid user → error.

Constraints / Forbidden Actions:

    Only the account owner sees their QR.

Tasks / Subtasks:

    DEV-401.1 Implement QRCode model (UUIDField)

    DEV-401.2 Create post_save signal for new users

    DEV-401.3 Profile page template to display QR code

    DEV-401.4 Unit tests for QR code creation

    DEV-401.5 Manual QA checklist

US-402: Check-in / Check-out via QR Code Scan

User Story:
As a user, I want to scan my personal QR code at a station to automatically check-in/out.

Acceptance Criteria:
Happy Path:

    Scan QR → check-in if currently checked out.

    Scan QR → check-out if currently checked in.

Edge Cases / Validation:

    Scan invalid QR → error.

    Scan QR of another user → error.

    System unavailable → error.

Constraints / Forbidden Actions:

    Only logged-in users can scan.

    QR can only be used once per cycle.

Tasks / Subtasks:

    DEV-402.1 Implement /qr-scan/ view

    DEV-402.2 Create scanner page template (scanner.html)

    DEV-402.3 JS logic for camera scan + AJAX POST

    DEV-402.4 Unit tests for scan logic

    DEV-402.5 Integration/E2E tests

    DEV-402.6 Manual QA checklist

 Now you have a complete Jira-ready roadmap:

    Strong acceptance criteria for all edge cases

    Tasks/subtasks separate from stories

    Traceable from user story → tasks → tests

    Ready for TDD + BDD workflows



