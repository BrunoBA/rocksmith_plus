from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class ArtistPage:
    def __init__(self, letter, driver):
        self.artists = []
        self.driver = driver
        driver.get(f"https://www.ubisoft.com/en-us/game/rocksmith/plus/song-library/search/artists/{letter}/1")

    def insert_artist(self, artist):
        if artist in self.artists:
            return
        self.artists.append(artist)

    # def load_artists(self):
    #     artists = self.fetch_artists()
    #     self.insert_artists(artists)

    def get_artists(self):
        return self.artists

    def element_exists(self, css_selector, timeout=5):
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

            return True
        except:
            return False

    def fetch_artists(self):
        if not self.element_exists('span.overflow-hidden', 10):
            return []

        elements = self.driver.find_elements(By.CSS_SELECTOR, 'span.overflow-hidden')
        for element in elements:
            self.insert_artist(element.text)

    def next_page(self):
        next_page_id = "#redirected-pagination > div > a.pagination-button.pagination-next"
        if not self.element_exists(next_page_id):
            return False

        wait = WebDriverWait(self.driver, 10)
        next_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, next_page_id)))
        next_page.click()

        return True
