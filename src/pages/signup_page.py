"""Trang dang ky (/signup)."""
from src.pages.base_page import AuthPage


class SignUpPage(AuthPage):
    PAGE_FRAGMENT = "/signup"
    FIELD_KEYS = ["signup.email", "signup.password", "signup.password_confirm"]

    def register(self, email: str, password: str, confirm: str = None):
        # Form gom: E-mail, Password, Password Confirm, nut Sign Up
        self.helper.type_text("signup.email", email)
        self.helper.type_text("signup.password", password)
        # O 'Password Confirm': mac dinh giong password
        if self.helper.is_visible("signup.password_confirm", timeout=3):
            self.helper.type_text("signup.password_confirm", password if confirm is None else confirm)
        self.helper.click("signup.submit")
        return self
