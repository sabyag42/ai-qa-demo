import pytest
from playwright.sync_api import Page, sync_playwright

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator('input[data-test="username"]')
        self.password_input = page.locator('input[data-test="password"]')
        self.login_button = page.locator('input[data-test="login-button"]')
        self.error_message = page.locator('h3[data-test="error"]')

    def navigate(self):
        self.page.goto("https://www.saucedemo.com")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self):
        return self.error_message.inner_text()

@pytest.fixture(scope="function")
def setup(page: Page):
    yield LoginPage(page)

@pytest.mark.regression
def test_successful_login(setup):
    setup.navigate()
    setup.login("standard_user", "secret_sauce")
    assert setup.page.url == "https://www.saucedemo.com/inventory.html"

@pytest.mark.smoke
@pytest.mark.regression
def test_login_with_invalid_credentials(setup):
    setup.navigate()
    setup.login("invalid_user", "invalid_password")
    assert setup.get_error_message() == "Epic sadface: Username and password do not match any user in this service"

@pytest.mark.regression
def test_login_with_empty_fields(setup):
    setup.navigate()
    setup.login("", "")
    assert setup.get_error_message() == "Epic sadface: Username is required"

@pytest.mark.regression
def test_login_with_locked_out_user(setup):
    setup.navigate()
    setup.login("locked_out_user", "secret_sauce")
    assert setup.get_error_message() == "Epic sadface: Sorry, this user has been locked out."

@pytest.mark.regression
def test_login_with_password_only(setup):
    setup.navigate()
    setup.login("", "secret_sauce")
    assert setup.get_error_message() == "Epic sadface: Username is required"

@pytest.mark.regression
def test_login_with_username_only(setup):
    setup.navigate()
    setup.login("standard_user", "")
    assert setup.get_error_message() == "Epic sadface: Password is required"

@pytest.mark.regression
def test_login_with_special_characters(setup):
    setup.navigate()
    setup.login("!@#$%^&*", "!@#$%^&*")
    assert setup.get_error_message() == "Epic sadface: Username and password do not match any user in this service"

@pytest.mark.regression
def test_login_with_sql_injection(setup):
    setup.navigate()
    setup.login("' OR '1'='1", "' OR '1'='1")
    assert setup.get_error_message() == "Epic sadface: Username and password do not match any user in this service"

@pytest.mark.regression
def test_login_with_long_username(setup):
    setup.navigate()
    setup.login("a" * 256, "secret_sauce")
    assert setup.get_error_message() == "Epic sadface: Username and password do not match any user in this service"