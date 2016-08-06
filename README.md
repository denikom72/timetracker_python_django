# Time Tracker Application

This is a Django-based time tracking application with role-based access control (RBAC), QR code-based check-in/out, and a PostgreSQL database.

## Setup Instructions

1.  **Clone the repository (if applicable):**

    ```bash
    git clone <repository-url>
    cd timetracker
    ```

2.  **Install Python dependencies:**

    ```bash
    pip3 install -r requirements.txt
    ```

3.  **Install PostgreSQL:**

    ```bash
    sudo apt-get update
    sudo apt-get install -y postgresql
    sudo service postgresql start
    ```

4.  **Create PostgreSQL user and database:**

    ```bash
    sudo -u postgres psql -c "CREATE USER gemini WITH PASSWORD 'gemini';"
    sudo -u postgres psql -c "CREATE DATABASE gemini;"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE gemini TO gemini;"
    ```

5.  **Apply Django migrations:**

    ```bash
    python3 manage.py makemigrations tracker
    python3 manage.py migrate
    ```

6.  **Create a superuser:**

    ```bash
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python3 manage.py shell
    ```

    **Admin Credentials:**
    *   Username: `admin`
    *   Password: `admin`

7.  **Run the development server:**

    ```bash
    python3 manage.py runserver
    ```

    The application will be accessible at `http://127.0.0.1:8000/`.
    The admin panel will be accessible at `http://127.0.0.1:8000/admin/`.

## Running Tests

To run the unit tests for the `tracker` app, use the following command:

```bash
python3 manage.py test tracker
```

---

## Project Roadmap

This project is organized into releases. For a detailed breakdown of user stories, estimations, and technical subtasks, please see the `PROJECT_SPECIFICATION.md` file.

### **Release 1.0 — Core Functionality (MVP)**

This release focuses on establishing the core features of the application.

*   **Epic 1: User Management & Authentication**
    *   **US-101:** User Login with credentials.
    *   **US-102:** User Logout.
    *   **US-103:** Admin User Management in Django Admin.
*   **Epic 2: Role-Based Access Control (RBAC)**
    *   **US-201:** Admin can manage Roles and Rights.
    *   **US-202:** Admin can assign permissions for roles to manage other roles.
*   **Epic 3: Time Tracking Core Functionality**
    *   **US-301:** Manual Check-in / Check-out from the dashboard.
*   **Epic 4: QR Code System**
    *   **US-401:** System generates a unique QR code for each user.
    *   **US-402:** Users can check-in or check-out by scanning their QR code.

### **Release 2.0 — Future Enhancements**

This release will build upon the core functionality to provide more comprehensive features for managers and administrators.

*   **Epic 5: Reporting & Analytics**
    *   **US-501:** As a Manager, I want to view a weekly timesheet for all employees I manage, so that I can track their hours.
    *   **US-502:** As an Admin, I want to export a monthly timesheet for all users as a CSV file, so that I can use it for payroll processing.
    *   **US-503:** As a User, I want to see a dashboard with my total hours worked this week and this month, so I can track my own time.
*   **Epic 6: Time Entry Management**
    *   **US-601:** As a Manager, I want to manually correct a check-in or check-out time for an employee I manage, so that I can fix errors (e.g., a forgotten check-out).
    *   **US-602:** As an Admin, I want to add a new time entry for any user, so that I can correct the record if a user was unable to check in.
    *   **US-603:** When a time entry is manually edited, the system should log who made the change and when, so that there is an audit trail.
*   **Epic 7: Enhanced User Interface**
    *   **US-701:** As a User, I want a dedicated dashboard page to view my time history with pagination, so I can easily review my past entries.
    *   **US-702:** As a Manager, I want the user management interface to be available outside of the Django Admin, so I can manage my team from the main application.
