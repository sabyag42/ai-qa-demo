import pytest
from playwright.sync_api import Page, sync_playwright

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("h3[data-test='error']")
    
    def navigate(self):
        self.page.goto("https://www.saucedemo.com")
    
    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
    
    def get_error_message(self):
        return self.error_message.inner_text()

@pytest.mark.regression
class TestLogin:
    
    @pytest.mark.smoke
    def test_successful_login(self, page: Page):
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")
        assert page.url == "https://www.saucedemo.com/inventory.html"

    def test_login_with_invalid_credentials(self, page: Page):
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("invalid_user", "invalid_password")
        assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service"

    def test_login_with_empty_fields(self, page: Page):
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("", "")
        assert login_page.get_error_message() == "Epic sadface: Username is required"

    def test_login_with_locked_out_user(self, page: Page):
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("locked_out_user", "secret_sauce")
        assert login_page.get_error_message() == "Epic sadface: Sorry, this user has been locked out."

    def test_login_with_password_only(self, page: Page):
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("", "secret_sauce")
        assert login_page.get_error_message() == "Epic sadface: Username is required"

    def test_login_with_username_only(self, page: Page):
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "")
        assert login_page.get_error_message() == "Epic sadface: Password is required"

    def test_login_with_nonexistent_user(self, page: Page):
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("nonexistent_user", "some_password")
        assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service"

    def test_login_with_special_characters(self, page: Page):
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("!@#$%^&*", "!@#$%^&*")
        assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service"

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()