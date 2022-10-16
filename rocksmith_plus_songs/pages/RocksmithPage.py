from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class RocksmithPage:
    def __init__(self, url, driver):
        self.driver = driver
        self.driver.get(url)
        self.data = []

    def max_wait(self):
        return 30

    def get_target(self):
        return 'span.overflow-hidden'

    def get_data(self):
        return self.data

    def query_selector_all(self, css_tag):
        return self.driver.find_elements(By.CSS_SELECTOR, css_tag)

    def insert_data(self, d):
        if d in self.data:
            return
        self.data.append(d)

    def fetch_data(self):
        target = self.get_target()

        if not self.element_exists(target, 10):
            return []

        elements = self.driver.find_elements(By.CSS_SELECTOR, target)
        for element in elements:
            self.insert_data(element.text)

    def element_exists(self, css_selector, timeout=5):
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

            return True
        except:
            return False

    def next_page(self):

        if self.element_exists("button.pagination-button-disabled.pagination-next", 5):
            return False

        next_page_id = "#redirected-pagination > div > a.pagination-button.pagination-next"
        if not self.element_exists(next_page_id):
            return False

        wait_time = self.max_wait()
        wait = WebDriverWait(self.driver, wait_time)
        next_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, next_page_id)))
        next_page.click()

        return True
