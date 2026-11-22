"""Lop cha cua cac trang: dung chung cach cho ket qua sau khi bam nut gui form."""
import re
import time

from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException

from src.base.helper import Helper

# Thong bao co noi dung "thanh cong" (khong khop 'unsuccessful')
SUCCESS_PATTERN = re.compile(r"\b(success(ful(ly)?)?|created|welcome)\b|thành công", re.IGNORECASE)


class BasePage:
    def __init__(self, driver, helper: Helper, base_url: str):
        self.driver = driver
        self.helper = helper
        self.base_url = base_url.rstrip("/")

    def current_url(self) -> str:
        return self.driver.current_url


class AuthPage(BasePage):
    """Trang co form gui di (dang nhap / dang ky)."""

    PAGE_FRAGMENT = ""      # vd '/signin' - con trong URL nghia la chua roi khoi trang
    FIELD_KEYS = []         # cac locator o nhap, dung doc thong bao HTML5

    def _pop_alert(self, exc=None):
        """Doc va dong hop thoai alert cua trinh duyet (neu co). Tra ve noi dung hoac None."""
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            return text
        except NoAlertPresentException:
            # Selenium co the da tu dong dong alert; lay noi dung tu ngoai le
            return getattr(exc, "alert_text", None) if exc is not None else None

    @staticmethod
    def _from_alert(text: str):
        text = text or ""
        if SUCCESS_PATTERN.search(text):
            return "success", f"Hop thoai alert: {text}"
        return "stay", f"Hop thoai alert: {text}"

    def wait_outcome(self, timeout: float = 8.0):
        """Doi ket qua sau khi bam nut gui.

        Tra ve (ket_qua, thong_bao):
          ('success', ...) neu roi khoi trang hien tai, hoac hien alert/thong bao thanh cong,
          ('stay', ...)    neu van o lai trang (kem thong bao loi / thong bao cua trinh duyet).
        """
        end = time.time() + timeout
        first_message_at = None
        message = ""
        while time.time() < end:
            try:
                alert = self._pop_alert()
                if alert:
                    return self._from_alert(alert)
                if self.PAGE_FRAGMENT not in self.current_url():
                    return "success", "Da chuyen khoi trang " + self.PAGE_FRAGMENT
                message = self.helper.visible_text("message.any")
                if message:
                    if SUCCESS_PATTERN.search(message):
                        return "success", message
                    # Cho them chut de xem co chuyen trang khong, roi ket luan la o lai
                    if first_message_at is None:
                        first_message_at = time.time()
                    elif time.time() - first_message_at >= 2:
                        return "stay", message
            except UnexpectedAlertPresentException as exc:
                return self._from_alert(self._pop_alert(exc) or "")
            time.sleep(0.4)
        try:
            native = self.helper.validation_message(self.FIELD_KEYS)
        except UnexpectedAlertPresentException as exc:
            return self._from_alert(self._pop_alert(exc) or "")
        if message:
            return "stay", message
        if native:
            return "stay", "Trinh duyet bao: " + native
        return "stay", "(khong thay thong bao nao)"
