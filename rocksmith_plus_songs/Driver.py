import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pyvirtualdisplay import Display
from webdriver_manager.chrome import ChromeDriverManager


class Driver:
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--verbose")
        options.add_argument("--headless")  # if you want it headless
        options.add_argument('--no-sandbox')
        options.add_argument("--enable-automation")
        options.add_argument('--disable-gpu')

        if platform.system() == "Linux" and platform.machine() == "armv7l":
            display = Display(visible=0, size=(800, 600))
            display.start()

            options.BinaryLocation = "/usr/bin/chromium-browser"
            service = Service("/usr/bin/chromedriver")

            self.driver = webdriver.Chrome(service=service, options=options)
        else:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def get_driver(self):
        return self.driver
