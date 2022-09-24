from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


class ArtistPage:
    def __init__(self, letter, driver):
        self.artists = []
        self.driver = driver
        driver.get(f"https://www.ubisoft.com/en-us/game/rocksmith/plus/song-library/search/artists/{letter}/1")

        res = True
        while (res):
            res = self.next_page()
            self.artists = self.artists + self.fetch_artists()
            time.sleep(1)

    def get_artists(self):
        return self.artists

    def fetch_artists(self):
        artists = []
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'span.overflow-hidden')
        for element in elements:
            artists.append(element.text)

        return artists

    def next_page(self):
        try:
            wait = WebDriverWait(self.driver, 3)
            myElem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#redirected-pagination > div > a.pagination-button.pagination-next")))
            myElem.click()

            return True
        except:
            return False
        