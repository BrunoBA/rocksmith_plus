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
            artists = self.fetch_artists()
            print(artists)

            self.artists = self.artists + artists

    def get_artists(self):
        return self.artists

    def fetch_artists(self):
        artists = []
        time.sleep(3)
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'span.overflow-hidden')
        for element in elements:
            artists.append(element.text)

        return artists

    def next_page(self):
        try:
            wait = WebDriverWait(self.driver, 2)
            myElem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#redirected-pagination > div > a.pagination-button.pagination-next")))
            myElem.click()

            return True
        except:
            return False
        