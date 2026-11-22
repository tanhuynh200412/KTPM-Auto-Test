"""Trang dang nhap (/signin)."""
from selenium.common.exceptions import TimeoutException

from src.pages.base_page import AuthPage


class SignInPage(AuthPage):
    PAGE_FRAGMENT = "/signin"
    FIELD_KEYS = ["signin.email", "signin.password"]

    def login(self, email: str, password: str):
        self.helper.type_text("signin.email", email)
        self.helper.type_text("signin.password", password)
        self.helper.click("signin.submit")
        return self

    def logout(self) -> bool:
        """Bam Logout (mo menu nguoi dung truoc neu co). Tra ve True neu bam duoc."""
        try:
            if not self.helper.is_visible("nav.logout", timeout=2) and "nav.user_menu" in self.helper.locators:
                try:
                    self.helper.click("nav.user_menu", timeout=3)
                except TimeoutException:
                    pass
            self.helper.click("nav.logout", timeout=8)
            return True
        except TimeoutException:
            return False
