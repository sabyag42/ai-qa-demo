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
def test_successful_login(playwright):
    with playwright.chromium.launch() as browser:
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")
        assert page.url == "https://www.saucedemo.com/inventory.html"
        page.close()

@pytest.mark.smoke
@pytest.mark.regression
def test_login_with_invalid_credentials(playwright):
    with playwright.chromium.launch() as browser:
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("invalid_user", "invalid_password")
        assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service"
        page.close()

@pytest.mark.regression
def test_login_with_empty_fields(playwright):
    with playwright.chromium.launch() as browser:
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("", "")
        assert login_page.get_error_message() == "Epic sadface: Username is required"
        page.close()

@pytest.mark.regression
def test_login_with_locked_out_user(playwright):
    with playwright.chromium.launch() as browser:
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("locked_out_user", "secret_sauce")
        assert login_page.get_error_message() == "Epic sadface: Sorry, this user has been locked out."
        page.close()

@pytest.mark.regression
def test_login_with_password_only(playwright):
    with playwright.chromium.launch() as browser:
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("", "secret_sauce")
        assert login_page.get_error_message() == "Epic sadface: Username is required"
        page.close()

@pytest.mark.regression
def test_login_with_username_only(playwright):
    with playwright.chromium.launch() as browser:
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "")
        assert login_page.get_error_message() == "Epic sadface: Password is required"
        page.close()

@pytest.mark.regression
def test_login_with_nonexistent_user(playwright):
    with playwright.chromium.launch() as browser:
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("nonexistent_user", "password")
        assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service"
        page.close()

@pytest.mark.regression
def test_login_with_special_characters(playwright):
    with playwright.chromium.launch() as browser:
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("!@#$%^&*", "!@#$%^&*")
        assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service"
        page.close()