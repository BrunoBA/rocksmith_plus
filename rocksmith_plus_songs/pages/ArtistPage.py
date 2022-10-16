from rocksmith_plus_songs.pages.RocksmithPage import RocksmithPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ArtistPage(RocksmithPage):
    def __init__(self, url, driver):
        super().__init__(url, driver)

    def next_page(self):
        if self.has_more_than_one_page():
            return False

        super().next_page()

    def fetch_data(self):
        target = self.get_target()

        if not self.element_exists(target, 30):
            return []

        elements = self.driver.find_elements(By.CSS_SELECTOR, target)
        for element in elements:
            self.insert_data(element.get_attribute("textContent"))

    def has_more_than_one_page(self) -> bool:
        wait = WebDriverWait(self.driver, 10)
        my_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#songs-results > h3')))

        quantity_of_artists = my_element.text.split("of")[1].strip()

        if int(quantity_of_artists) > 25:
            return True

        return False

    def max_wait(self):
        return 40

    def get_target(self):
        return "div.d-flex.marquee-container.ml-4.mr-3.table-text-bold > span"
