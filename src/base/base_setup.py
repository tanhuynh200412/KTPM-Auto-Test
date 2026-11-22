"""Doc cau hinh, khoi tao trinh duyet, danh thuc server Render."""
import os
import urllib.request

import yaml
from dotenv import load_dotenv
from selenium import webdriver

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(os.path.join(ROOT, ".env"))


def load_yaml(relative_path: str) -> dict:
    with open(os.path.join(ROOT, relative_path), encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_config() -> dict:
    return load_yaml("config.yaml")


def wake_server(url: str, timeout: int = 90) -> None:
    """Render goi mien phi se 'ngu' khi khong dung; goi thu de danh thuc truoc khi test."""
    print(f"Dang danh thuc server {url} (co the mat toi {timeout}s)...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        urllib.request.urlopen(req, timeout=timeout).read(1)
        print("Server da san sang.")
    except Exception as exc:  # noqa: BLE001
        print(f"[CANH BAO] Server chua phan hoi ({exc}), van tiep tuc.")


class BaseSetup:
    def __init__(self, config: dict, browser: str = None, headless: bool = None):
        self.config = config
        self.base_url = config.get("base_url", "").rstrip("/")
        self.browser = (browser or config.get("browser", "chrome")).lower()
        self.headless = config.get("headless", False) if headless is None else headless
        self.driver = None

    def init_driver(self):
        if self.browser == "chrome":
            opts = webdriver.ChromeOptions()
            if self.headless:
                opts.add_argument("--headless=new")
            opts.add_argument("--window-size=1366,900")
            self.driver = webdriver.Chrome(options=opts)  # Selenium Manager tu tim driver
        elif self.browser == "edge":
            opts = webdriver.EdgeOptions()
            if self.headless:
                opts.add_argument("--headless=new")
            opts.add_argument("--window-size=1366,900")
            self.driver = webdriver.Edge(options=opts)
        elif self.browser == "firefox":
            opts = webdriver.FirefoxOptions()
            if self.headless:
                opts.add_argument("-headless")
            self.driver = webdriver.Firefox(options=opts)
        else:
            raise ValueError(f"Trinh duyet khong ho tro: {self.browser}")
        self.driver.set_page_load_timeout(self.config.get("timeouts", {}).get("page_load", 90))
        return self.driver

    def reset_session(self) -> None:
        """Xoa cookie va bo nho trinh duyet de moi test case doc lap (phai dang o trang cua site)."""
        try:
            self.driver.delete_all_cookies()
            self.driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
        except Exception:  # noqa: BLE001
            pass

    def quit(self) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None
