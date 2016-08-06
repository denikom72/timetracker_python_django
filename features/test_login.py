import pytest
from playwright.sync_api import Page, expect
from django.urls import reverse
from django.contrib.auth import get_user_model

# Manually define the base URL for the running Django server
BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture(scope="session", autouse=True)
def setup_test_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')

def test_successful_login(page: Page, setup_test_user):
    page.goto(f"{BASE_URL}{reverse('login')}")
    page.fill('[name="username"]', 'admin')
    page.fill('[name="password"]', 'admin')
    page.click('button:has-text("Login")')
    expect(page).to_have_url(f"{BASE_URL}{reverse('index')}")
    expect(page.locator('h1')).to_have_text('Welcome to the Time Tracker')

def test_unsuccessful_login(page: Page, setup_test_user):
    page.goto(f"{BASE_URL}{reverse('login')}")
    page.fill('[name="username"]', 'wronguser')
    page.fill('[name="password"]', 'wrongpassword')
    page.click('button:has-text("Login")')
    expect(page.locator('body')).to_contain_text('Please enter a correct username and password')