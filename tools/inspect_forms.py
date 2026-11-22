"""Doc cac o nhap / nut tren trang dang nhap va dang ky de xac nhan locators.yaml.

Chay (tu thu muc goc du an):   python tools/inspect_forms.py
Ket qua luu o form_info.txt -> gui noi dung de chinh locators neu can.
"""
import os
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from selenium.webdriver.common.by import By

from src.base.base_setup import BaseSetup, load_config

cfg = load_config()
setup = BaseSetup(cfg)
driver = setup.init_driver()
lines = []


def log(text=""):
    print(text)
    lines.append(text)


def dump(title, path):
    url = setup.base_url + path
    log("=" * 70)
    log(f"{title}: {url}")
    driver.get(setup.base_url + "/")
    time.sleep(6)
    # Di bang header de tranh loi route khi vao thang URL
    links = driver.find_elements(By.CSS_SELECTOR, f'a[href="{path}"]')
    if links:
        try:
            links[0].click()
        except Exception:  # noqa: BLE001
            driver.get(url)
    else:
        driver.get(url)
    time.sleep(6)
    log(f"URL hien tai: {driver.current_url}")
    for tag in ("input", "button", "a", "label", "form"):
        log(f"--- <{tag}> ---")
        for el in driver.find_elements(By.TAG_NAME, tag):
            log(f"{tag} | type={el.get_attribute('type')} | name={el.get_attribute('name')} | "
                f"id={el.get_attribute('id')} | placeholder={el.get_attribute('placeholder')} | "
                f"href={el.get_attribute('href')} | text={el.text.strip()[:40]!r}")


try:
    dump("TRANG DANG NHAP", "/signin")
    dump("TRANG DANG KY", "/signup")
finally:
    setup.quit()
    with open(os.path.join(ROOT, "form_info.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\nDa luu vao form_info.txt")
