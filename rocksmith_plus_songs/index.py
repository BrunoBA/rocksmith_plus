# encoding: utf-8

import logging
import datetime
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from rocksmith_plus_songs.pages.LetterPage import LetterPage
from rocksmith_plus_songs.Driver import Driver
from rocksmith_plus_songs.pages.PagesUrl import PagesUrl
from bba_playlist.Soundtrack import Soundtrack

start_date = datetime.datetime.now()
logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(asctime)s %(message)s")
logging.info(f"Started {start_date.strftime('%Y-%m-%d %H:%M:%S')}")

driver = Driver().get_driver()

try:
    driver.get("https://www.ubisoft.com/en-us/game/rocksmith/plus/song-library/search/artists/symbol/1")
except TimeoutException as ex:
    driver.navigate().refresh()

try:
    wait = WebDriverWait(driver, 20)
    cookies_consent = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#privacy__modal__close")))
    cookies_consent.click()
except:
    pass

soundtrack = Soundtrack()
letters = PagesUrl().get_letters()
artists = []
expected = 0
for letter in letters:
    page = LetterPage(letter, driver)

    try:
        wait = WebDriverWait(driver, 10)
        my_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#artists-by-letter-results > h3')))

        quantity_of_artists = my_element.text.split("of")[1].strip()
    except Exception as error:
        quantity_of_artists = 0
        logging.info(f"---------------- Error to load {letter}")
        pass

    expected = expected + int(quantity_of_artists)

    next_page = True
    while next_page:
        time.sleep(5)

        page.fetch_data()
        next_page = page.next_page()

    loaded_art = page.get_artists()
    artists = artists + loaded_art
    logging.info(f"- Artists from {letter.upper()}: Expected ({quantity_of_artists}) Loaded: {len(loaded_art)}")

    for art in page.fetch_artists_songs():
        soundtrack.add_artist(art)

print(soundtrack.toJSON())


qtd_artists = len(artists)
end_date = datetime.datetime.now()

delta = end_date - start_date

logging.info(f"Artists: {qtd_artists} Expected: {expected} Time: {delta}")

driver.close()

