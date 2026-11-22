"""Thuc thi mot test case doc tu Excel (du lieu -> thao tac tren trang -> Pass/Fail).

Quy uoc cot 'Expected':
  success : he thong phai chap nhan (chuyen khoi trang dang nhap/dang ky)
  fail    : he thong phai tu choi (o lai trang)
  logout  : (chi sheet Login) dang nhap xong bam Logout, nut Login tren header phai hien lai

Bien trong du lieu:
  {same}                -> (cot Confirm Password) giong cot Password
  {unique}              -> chuoi theo thoi gian, moi lan chay mot gia tri (tranh trung email)
  ${REGISTERED_EMAIL}   -> email vua dang ky thanh cong o SIGNUP o lan chay nay (hoac TEST_EMAIL trong .env)
  ${REGISTERED_PASS}    -> mat khau tuong ung (hoac TEST_PASS trong .env)
  ${TEN_BIEN}           -> bat ky bien moi truong / .env
"""
import os
import re
from dataclasses import dataclass

ENV_FALLBACK = {"REGISTERED_EMAIL": "TEST_EMAIL", "REGISTERED_PASS": "TEST_PASS"}


class Blocked(Exception):
    """Test case khong the chay (thieu du lieu dau vao)."""


@dataclass
class Result:
    sheet: str
    id: str
    title: str
    status: str            # Pass | Fail | Blocked | Error
    expected: str
    actual: str
    screenshot: str = ""


def resolve(value, ctx: dict, run_id: str) -> str:
    text = "" if value is None else str(value)
    text = text.replace("{unique}", run_id)

    def sub(match):
        name = match.group(1)
        found = ctx.get(name) or os.environ.get(ENV_FALLBACK.get(name, name))
        if not found:
            raise Blocked(f"Thieu gia tri cho bien ${{{name}}} (hay chay sheet Signup truoc hoac khai bao trong .env)")
        return found

    return re.sub(r"\$\{(\w+)\}", sub, text)


def evaluate(expected: str, outcome: str, message: str, page_name: str):
    """Doi chieu ket qua ky vong va thuc te -> (status, actual)."""
    if expected == "success":
        if outcome == "success":
            return "Pass", f"Thanh cong: {message}"
        return "Fail", f"Ky vong thanh cong nhung van o trang {page_name}. Thong bao: {message}"
    if expected == "fail":
        if outcome == "stay":
            return "Pass", f"Bi tu choi dung ky vong. Thong bao: {message}"
        return "Fail", f"Ky vong bi tu choi nhung he thong lai chap nhan ({message})"
    return "Error", f"Gia tri cot Expected khong hop le: '{expected}'"


def execute(case: dict, sheet: str, env) -> tuple:
    """Chay mot test case. env gom: home (HomePage), setup (BaseSetup), cfg, ctx, run_id."""
    expected = str(case.get("expected") or "").strip().lower()
    email = resolve(case.get("email"), env.ctx, env.run_id)
    password = resolve(case.get("password"), env.ctx, env.run_id)
    # Cot 'Confirm Password': {same} (hoac khong co cot) = giong Password; de trong = bo trong o xac nhan
    if "confirm_password" in case:
        raw_confirm = "" if case["confirm_password"] is None else str(case["confirm_password"])
        confirm = password if raw_confirm == "{same}" else resolve(raw_confirm, env.ctx, env.run_id)
    else:
        confirm = password

    # Moi test case bat dau tu trang thai sach
    env.home.open()
    env.setup.reset_session()
    env.driver.refresh()

    timeout = env.cfg.get("timeouts", {}).get("result", 8)

    if sheet == "Signup":
        page = env.home.open_signup()
        page.register(email, password, confirm)
        outcome, message = page.wait_outcome(timeout)
        status, actual = evaluate(expected, outcome, message, "/signup")
        if outcome == "success" and expected == "success" and "REGISTERED_EMAIL" not in env.ctx:
            env.ctx["REGISTERED_EMAIL"] = email
            env.ctx["REGISTERED_PASS"] = password
        return status, actual

    # sheet Login
    page = env.home.open_signin()
    page.login(email, password)
    outcome, message = page.wait_outcome(timeout)

    if expected == "logout":
        if outcome != "success":
            return "Fail", f"Khong dang nhap duoc de thu Logout. Thong bao: {message}"
        if not page.logout():
            return "Fail", "Dang nhap duoc nhung khong tim thay nut Logout (kiem tra nav.logout trong locators.yaml)"
        env.home.open()
        if env.home.is_login_button_visible():
            return "Pass", "Dang xuat thanh cong: nut Login hien lai tren header"
        return "Fail", "Da bam Logout nhung nut Login khong hien lai"

    return evaluate(expected, outcome, message, "/signin")
