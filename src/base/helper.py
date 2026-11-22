"""Cac thao tac an toan voi phan tu, dung kho dinh vi locators.yaml."""
import time

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Helper:
    def __init__(self, driver, locators: dict, timeout: int = 25):
        self.driver = driver
        self.locators = locators
        self.timeout = timeout

    # ---- locator ----
    def by(self, key: str):
        if key not in self.locators:
            raise KeyError(f"Chua khai bao locator '{key}' trong locators.yaml")
        raw = str(self.locators[key]).strip()
        for prefix, how in (("xpath=", By.XPATH), ("id=", By.ID), ("name=", By.NAME), ("css=", By.CSS_SELECTOR)):
            if raw.startswith(prefix):
                return how, raw[len(prefix):]
        return By.CSS_SELECTOR, raw

    def _wait(self, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout)

    # ---- tim / kiem tra ----
    def find(self, key: str, timeout=None):
        return self._wait(timeout).until(EC.visibility_of_element_located(self.by(key)))

    def is_visible(self, key: str, timeout: float = 3) -> bool:
        try:
            self.find(key, timeout)
            return True
        except TimeoutException:
            return False

    def visible_text(self, key: str) -> str:
        """Van ban cac phan tu dang hien thi (khong cho). Rong neu khong co."""
        texts = []
        for el in self.driver.find_elements(*self.by(key)):
            try:
                if el.is_displayed() and el.text.strip():
                    texts.append(el.text.strip())
            except WebDriverException:
                continue
        return " | ".join(texts)

    def validation_message(self, keys) -> str:
        """Thong bao kiem tra hop le cua trinh duyet (HTML5) o o nhap dau tien bi loi."""
        for key in keys:
            for el in self.driver.find_elements(*self.by(key)):
                try:
                    msg = self.driver.execute_script("return arguments[0].validationMessage || '';", el)
                except WebDriverException:
                    msg = ""
                if msg:
                    return msg
        return ""

    # ---- thao tac ----
    def click(self, key: str, timeout=None) -> None:
        el = self._wait(timeout).until(EC.element_to_be_clickable(self.by(key)))
        try:
            el.click()
        except WebDriverException:
            self.driver.execute_script("arguments[0].click();", el)

    def type_text(self, key: str, text: str, timeout=None):
        el = self.find(key, timeout)
        el.clear()
        if text:
            el.send_keys(text)
        return el

    # ---- URL ----
    def wait_url_contains(self, fragment: str, timeout=None) -> bool:
        try:
            self._wait(timeout).until(lambda d: fragment in d.current_url)
            return True
        except TimeoutException:
            return False

    def screenshot(self, path: str) -> None:
        try:
            self.driver.save_screenshot(path)
        except WebDriverException:
            pass

    @staticmethod
    def sleep(seconds: float) -> None:
        time.sleep(seconds)
