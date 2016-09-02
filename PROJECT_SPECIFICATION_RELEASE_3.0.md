### **Release 3.0: Advanced Features & Integrations**

This release focuses on adding project-based tracking, a leave management system, advanced reporting, and system notifications to make the Time Tracker a more comprehensive and indispensable tool for teams.

---

### **Epic 1: Project-Based Time Tracking**

**Description:** To enable more granular time tracking, this epic introduces the concept of "Projects." Users will now associate their work hours with specific projects, allowing for better cost allocation and productivity analysis.

*   **US-801: Admin can manage projects**
    *   **As an** Admin,
    *   **I want** to create, edit, and archive projects,
    *   **so that** I can set up the tracking categories for the entire organization.
    *   **Acceptance Criteria (AC):**
        1.  An admin user can access a "Projects" management page from the main navigation or admin dashboard.
        2.  On this page, the admin can add a new project by providing a unique Project Name and an optional Description.
        3.  The admin can edit the name and description of any existing project.
        4.  The admin can archive a project. Archived projects cannot be selected for new time entries but their data is retained for historical reporting.
        5.  The admin can reactivate an archived project.

*   **US-802: Manager can assign projects to users**
    *   **As a** Manager,
    *   **I want** to assign my team members to specific projects,
    *   **so that** they can only log time against the projects they are authorized to work on.
    *   **Acceptance Criteria (AC):**
        1.  A manager can access a "Project Assignments" page for their team.
        2.  The page lists all managed users.
        3.  For each user, the manager can select one or more active projects from a multi-select list to assign to them.
        4.  The user's project assignments are saved and immediately effective.
        5.  A manager can remove a project assignment from a user at any time.

*   **US-803: User logs time against a specific project**
    *   **As a** User,
    *   **I want** to select a project when I check-in,
    *   **so that** my work hours are correctly attributed to the task I am performing.
    *   **Acceptance Criteria (AC):**
        1.  When a user initiates a "Check-in," the UI now includes a mandatory dropdown field for "Project."
        2.  This dropdown is populated only with the projects the user has been assigned to.
        3.  The user cannot complete the check-in process without selecting a project.
        4.  The created `CheckInCheckOut` record is now linked to the selected project.
        5.  The user's time history page now displays the project associated with each time entry.

---

### **Epic 2: Leave Management System**

**Description:** This epic introduces a complete workflow for requesting, approving, and tracking employee time off, integrating it seamlessly with the timesheet data.

*   **US-901: User can request time off**
    *   **As a** User,
    *   **I want** to submit a request for time off (e.g., vacation, sick leave),
    *   **so that** I can get formal approval and have it recorded in the system.
    *   **Acceptance Criteria (AC):**
        1.  The user has a "Leave" or "Time Off" section in their dashboard.
        2.  The user can submit a new request by selecting a "Leave Type," a "Start Date," and an "End Date."
        3.  The request is created with a "Pending" status and sent to the user's manager for approval.
        4.  The user can view a history of all their leave requests and their current status (Pending, Approved, Denied).

*   **US-902: Manager can approve or deny leave requests**
    *   **As a** Manager,
    *   **I want** to review and approve or deny leave requests from my team members,
    *   **so that** I can manage my team's schedule and availability.
    *   **Acceptance Criteria (AC):**
        1.  A manager sees a notification or a dashboard widget for pending leave requests from their team.
        2.  The manager can view the details of each request (employee, dates, leave type).
        3.  The manager has "Approve" and "Deny" buttons for each pending request.
        4.  Upon action, the request's status is updated, and the user is notified of the decision.

*   **US-903: Admin can configure leave types**
    *   **As an** Admin,
    *   **I want** to configure the different types of leave available to employees,
    *   **so that** the system aligns with our company's HR policies.
    *   **Acceptance Criteria (AC):**
        1.  An admin can access a "Leave Types" management page.
        2.  The admin can create new leave types (e.g., "Vacation," "Sick Leave," "Personal Day").
        3.  The admin can define whether a leave type is paid or unpaid.
        4.  The admin can set an annual accrual allowance for each leave type if applicable.

---

### **Epic 3: Advanced Reporting & Notifications**

**Description:** This epic enhances the reporting capabilities to include project data and introduces a notification system to improve communication and user engagement.

*   **US-1001: Manager can generate project-based reports**
    *   **As a** Manager,
    *   **I want** to generate reports that show how many hours my team has logged against each project,
    *   **so that** I can monitor project progress and budget.
    *   **Acceptance Criteria (AC):**
        1.  A manager has access to a new "Project Report" generator.
        2.  The manager can filter the report by project, user, and date range.
        3.  The generated report displays a summary of total hours per project and a detailed breakdown of hours per user for each project.
        4.  The report can be exported to a CSV file.

*   **US-1002: System sends automated reminder notifications**
    *   **As a** User,
    *   **I want** to receive an email reminder if I forget to check out,
    *   **so that** I can maintain an accurate timesheet with minimal effort.
    *   **Acceptance Criteria (AC):**
        1.  The system automatically detects check-ins that have been active for more than 10 hours.
        2.  When such a check-in is found, an email notification is sent to the user as a reminder.
        3.  This feature can be enabled or disabled by the admin on a system-wide basis.

*   **US-1003: Manager receives a weekly team summary email**
    *   **As a** Manager,
    *   **I want** to receive a weekly email summarizing my team's logged hours,
    *   **so that** I can stay informed about my team's activity without having to log in.
    *   **Acceptance Criteria (AC):**
        1.  A scheduled task runs every Monday morning.
        2.  The task generates a summary for each manager, including total hours worked by their team in the previous week and a list of any pending leave requests.
        3.  This summary is delivered to the manager's email address.