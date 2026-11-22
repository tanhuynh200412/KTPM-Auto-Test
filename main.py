"""Diem khoi chay chinh: kiem thu tu dong Dang nhap + Dang ky (Selenium + Page Object Model).

Cach chay:
    python main.py                              # chay tat ca (Signup roi Login)
    python main.py --sheet Login                # chi chay sheet Login
    python main.py --only LOGIN_001,SIGNUP_002  # chay cac test case chi dinh
    python main.py --headless                   # an trinh duyet
    python main.py --browser edge               # chrome | edge | firefox
"""
import argparse
import os
import sys
from datetime import datetime
from types import SimpleNamespace

ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.base.base_setup import BaseSetup, load_config, load_yaml, wake_server
from src.base.helper import Helper
from src.pages.home_page import HomePage
from src.report.reporter import load_cases, write_excel, write_html
from src.testcases.executor import Blocked, Result, execute


def parse_args():
    p = argparse.ArgumentParser(description="Kiem thu tu dong Dang nhap / Dang ky")
    p.add_argument("--only", help="Danh sach ma test case, cach nhau bang dau phay")
    p.add_argument("--sheet", choices=["Login", "Signup"], help="Chi chay mot sheet")
    p.add_argument("--headless", action="store_true", help="An trinh duyet")
    p.add_argument("--browser", choices=["chrome", "edge", "firefox"])
    p.add_argument("--no-wake", action="store_true", help="Khong danh thuc server truoc khi chay")
    return p.parse_args()


def main():
    args = parse_args()
    cfg = load_config()
    paths = cfg["paths"]
    testdata = os.path.join(ROOT, paths["testdata"])
    out_dir = os.path.join(ROOT, paths["output"])
    shot_dir = os.path.join(out_dir, "screenshots")
    os.makedirs(shot_dir, exist_ok=True)

    sheets = [args.sheet] if args.sheet else cfg.get("run_order", ["Signup", "Login"])
    only = {x.strip().upper() for x in args.only.split(",")} if args.only else None

    plan = []
    for sheet in sheets:
        for case in load_cases(testdata, sheet):
            if only is None or case["id"].upper() in only:
                plan.append((sheet, case))
    if not plan:
        print("Khong co test case nao de chay (kiem tra --only / --sheet).")
        return 2

    if not args.no_wake:
        wake_server(cfg["base_url"], cfg.get("timeouts", {}).get("page_load", 90))

    setup = BaseSetup(cfg, browser=args.browser, headless=True if args.headless else None)
    driver = setup.init_driver()
    helper = Helper(driver, load_yaml(paths["locators"]), cfg.get("timeouts", {}).get("element", 25))
    env = SimpleNamespace(
        driver=driver, setup=setup, cfg=cfg, ctx={}, run_id=datetime.now().strftime("%m%d%H%M%S"),
        home=HomePage(driver, helper, setup.base_url),
    )

    results = []
    try:
        for sheet, case in plan:
            tc_id, title = case["id"], str(case.get("title") or "")
            print(f"[{tc_id}] {title} ... ", end="", flush=True)
            try:  # dong alert con sot lai tu test case truoc (neu co)
                driver.switch_to.alert.accept()
            except Exception:  # noqa: BLE001
                pass
            try:
                status, actual = execute(case, sheet, env)
            except Blocked as exc:
                status, actual = "Blocked", str(exc)
            except Exception as exc:  # noqa: BLE001
                status, actual = "Error", f"{type(exc).__name__}: {str(exc).splitlines()[0] if str(exc) else ''}"
            shot_name = f"{tc_id}.png"
            helper.screenshot(os.path.join(shot_dir, shot_name))
            results.append(Result(sheet, tc_id, title, status, str(case.get("expected") or ""),
                                  actual, f"../screenshots/{shot_name}"))
            print(status)
            print(f"      -> {actual}")
    finally:
        setup.quit()

    meta = {"time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "base_url": cfg["base_url"],
            "browser": setup.browser + (" (headless)" if setup.headless else "")}
    write_excel(testdata, os.path.join(out_dir, "reports", "results.xlsx"), results, meta)
    write_html(os.path.join(out_dir, "reports", "report.html"), results, meta)

    total = len(results)
    counts = {s: sum(1 for r in results if r.status == s) for s in ("Pass", "Fail", "Blocked", "Error")}
    print("\n" + "=" * 60)
    print(f"Tong: {total} | Pass: {counts['Pass']} | Fail: {counts['Fail']} | "
          f"Blocked: {counts['Blocked']} | Error: {counts['Error']}")
    print("Bao cao: test-output/reports/report.html va results.xlsx")
    return 0 if counts["Fail"] == 0 and counts["Error"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
