"""Trang chu va dieu huong sang trang dang nhap / dang ky."""
from selenium.common.exceptions import TimeoutException

from src.pages.base_page import BasePage
from src.pages.signin_page import SignInPage
from src.pages.signup_page import SignUpPage


class HomePage(BasePage):
    def open(self):
        self.driver.get(self.base_url + "/")
        return self

    def open_signin(self) -> SignInPage:
        self.helper.click("header.login_button")
        if not self.helper.wait_url_contains("/signin", 15):
            self.driver.get(self.base_url + "/signin")
        return SignInPage(self.driver, self.helper, self.base_url)

    def open_signup(self) -> SignUpPage:
        try:
            self.helper.click("header.signup_button", timeout=8)
        except TimeoutException:
            pass
        if not self.helper.wait_url_contains("/signup", 10):
            self.driver.get(self.base_url + "/signup")
        return SignUpPage(self.driver, self.helper, self.base_url)

    def is_login_button_visible(self, timeout: float = 8) -> bool:
        return self.helper.is_visible("header.login_button", timeout)
