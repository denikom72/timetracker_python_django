TEST_CASES.md (Revised MVP-Focused )

Time Tracker (V2) – Test Case Specification
1. Purpose

Define critical acceptance and integration tests derived directly from user stories.
Unit and UI tests are partially defined, with TBD placeholders for future development.

2. Acceptance Tests (Must-have)
ID  User Story  Test Scenario   Steps   Expected Outcome

AT-101  US-101 / US-102 Login → Logout
1. Navigate to login page → 2. Enter valid credentials → 3. Click login → 4. Click logout   User successfully logs in and session terminates on logout

AT-102  US-301  Manual Check-In/Out
1. Login → 2. Click "Check-in" → 3. Click "Check-out"   Check-in and check-out timestamps recorded correctly in DB

AT-103  US-402  QR Check-in/Out 
1. Navigate to scanner → 2. Scan valid QR → 3. Scan again   User toggled check-in/out; visual feedback shown

AT-104  US-103 / US-201 / US-202    RBAC enforcement    
1. Login as admin → 2. Create role & assign permissions → 3. Login as managed user  Permissions enforced correctly; unauthorized access blocked


these are directly traceable to acceptance criteria.


3. Integration Tests (Should-have / MVP-critical)

ID  Feature Test Scenario   Expected Outcome

IT-201  Login + Time Tracking   Login → Check-in → Logout → Check-out next day  Correct session handling + check-in/out entries
IT-202  QR + RBAC   Scan QR as user without permission for admin panel  Access denied (403)

4. Unit Tests (TBD / Could-have)

ID  Module  Test Name   Priority    Notes

UT-301  models.CheckInCheckOut  test_toggle_check_in_out    TBD Critical logic, define after core MVP
UT-302  signals.py  test_qr_created_on_user_save    TBD Signal validation for QR auto-create
UT-303  models.ManagedRole  test_no_self_management TBD Prevent self-management
UT-304  utils.py    format_timestamp    TBD Minor utility; low priority for MVP

These are not required for first MVP, but tracked for future unit testing.

5. Frontend / UI Tests (TBD / Could-have)

ID  Component   Test Name   Priority    Notes

FT-301  index.html  test_button_visibility  TBD Dynamically hide/show check-in/out button
FT-302  scanner.js  test_qr_scan_success    TBD Mock QR scan callback; visual feedback
FT-303  login.html  test_invalid_login_message  TBD Error banner appears on invalid login

These can be implemented later, after backend MVP is stable.

6. Strategy Notes

- Acceptance & Integration Tests = MVP-critical → Must define and automate first

- Unit/UI Tests = supplementary → TBD, added progressively

- Tests are traceable to user stories → simplifies Jira/GitHub issue linking

- CI/CD Integration: Run acceptance + integration tests automatically; unit/UI tests gradually added


______________


TODO

1. Project Structure for Cypress + Gherkin

project-root/
├─ cypress/
│  ├─ e2e/
│  │  ├─ login.feature
│  │  ├─ checkin_checkout.feature
│  │  └─ qr_scan.feature
│  ├─ step_definitions/
│  │  ├─ login_steps.js
│  │  ├─ checkin_checkout_steps.js
│  │  └─ qr_scan_steps.js
│  └─ support/
│     └─ commands.js
├─ cypress.config.js

2. Feature Files (.feature)
2.1 login.feature → cypress/e2e/login.feature

Feature: User Login

  Scenario: User logs in with valid credentials
    Given the user is on the login page
    When they enter valid username and password
    And click the login button
    Then they should be redirected to the dashboard
    And see "Welcome, j.smith!"

  Scenario: User enters invalid credentials
    Given the user is on the login page
    When they enter invalid username or password
    And click the login button
    Then they should see an error message

2.2 checkin_checkout.feature → cypress/e2e/checkin_checkout.feature

Feature: Manual Check-In / Check-Out

  Scenario: User checks in
    Given the user is logged in
    And the user is currently checked out
    When they click the "Check-in" button
    Then a new check-in entry should be created
    And the dashboard should show status "Checked In"

  Scenario: User checks out
    Given the user is logged in
    And the user is currently checked in
    When they click the "Check-out" button
    Then the current entry should be updated with check-out time
    And the dashboard should show status "Checked Out"

2.3 qr_scan.feature → cypress/e2e/qr_scan.feature

Feature: QR Code Check-In / Check-Out

  Scenario: User scans QR to check in
    Given the user is logged in
    And the user is currently checked out
    When they scan their personal QR code
    Then the system should mark them as checked in
    And display "Welcome, j.smith!"

  Scenario: User scans QR to check out
    Given the user is logged in
    And the user is currently checked in
    When they scan their personal QR code
    Then the system should mark them as checked out
    And display "Goodbye, j.smith!"

3. Step Definitions (.js)
3.1 login_steps.js → cypress/step_definitions/login_steps.js

import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";

Given('the user is on the login page', () => {
  cy.visit('/login');
});

When('they enter valid username and password', () => {
  cy.get('input[name="username"]').type('j.smith');
  cy.get('input[name="password"]').type('password123');
});

When('they enter invalid username or password', () => {
  cy.get('input[name="username"]').type('wronguser');
  cy.get('input[name="password"]').type('wrongpass');
});

When('click the login button', () => {
  cy.get('button[type="submit"]').click();
});

Then('they should be redirected to the dashboard', () => {
  cy.url().should('include', '/dashboard');
});

Then('see {string}', (message) => {
  cy.contains(message).should('be.visible');
});

Then('they should see an error message', () => {
  cy.contains('Invalid credentials').should('be.visible');
});

3.2 checkin_checkout_steps.js → cypress/step_definitions/checkin_checkout_steps.js

import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";

Given('the user is logged in', () => {
  cy.login('j.smith', 'password123'); // custom command
});

Given('the user is currently checked out', () => {
  cy.setCheckInStatus(false); // mock or API call
});

Given('the user is currently checked in', () => {
  cy.setCheckInStatus(true); // mock or API call
});

When('they click the {string} button', (buttonText) => {
  cy.contains(buttonText).click();
});

Then('a new check-in entry should be created', () => {
  cy.verifyCheckInStatus(true); // custom assertion
});

Then('the current entry should be updated with check-out time', () => {
  cy.verifyCheckOutTime(); // custom assertion
});

Then('the dashboard should show status {string}', (status) => {
  cy.contains(`Status: ${status}`).should('be.visible');
});

3.3 qr_scan_steps.js → cypress/step_definitions/qr_scan_steps.js

import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";

Given('the user is logged in', () => {
  cy.login('j.smith', 'password123'); // custom command
});

Given('the user is currently checked out', () => {
  cy.setCheckInStatus(false);
});

Given('the user is currently checked in', () => {
  cy.setCheckInStatus(true);
});

When('they scan their personal QR code', () => {
  // simulate QR scan via mock API
  cy.intercept('POST', '/qr-scan/', { fixture: 'qr-success.json' }).as('qrScan');
  cy.get('#simulate-scan-button').click();
  cy.wait('@qrScan');
});

Then('the system should mark them as checked in', () => {
  cy.verifyCheckInStatus(true);
});

Then('the system should mark them as checked out', () => {
  cy.verifyCheckInStatus(false);
});

Then('display {string}', (message) => {
  cy.contains(message).should('be.visible');
});

4. Custom Commands (Optional Helpers)

cypress/support/commands.js:

Cypress.Commands.add('login', (username, password) => {
  cy.visit('/login');
  cy.get('input[name="username"]').type(username);
  cy.get('input[name="password"]').type(password);
  cy.get('button[type="submit"]').click();
});

Cypress.Commands.add('setCheckInStatus', (status) => {
  // e.g., mock API or reset DB for test
  cy.request('POST', '/api/test/set_status/', { checkedIn: status });
});

Cypress.Commands.add('verifyCheckInStatus', (expected) => {
  cy.request('/api/test/current_status').its('body.checkedIn').should('eq', expected);
});

Cypress.Commands.add('verifyCheckOutTime', () => {
  cy.request('/api/test/current_entry').its('body.checkOutTime').should('exist');
});



Summary

    Feature files → cypress/e2e/*.feature

    Step definitions → cypress/step_definitions/*.js

    Custom commands / helpers → cypress/support/commands.js

    Tests simulate real user flows, can mock backend APIs for deterministic results.

    Can extend for more roles, RBAC, error handling, or real device testing.


