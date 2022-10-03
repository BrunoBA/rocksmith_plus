# encoding: utf-8

import logging
import datetime
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from rocksmith_plus_songs.pages.ArtistPage import ArtistPage
from rocksmith_plus_songs.Driver import Driver
from rocksmith_plus_songs.pages.PagesUrl import PagesUrl

start_date = datetime.datetime.now()
logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(asctime)s %(message)s")

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

letters = PagesUrl().get_letters()
artists = []
expected = 0
for letter in letters:
    page = ArtistPage(letter, driver)

    try:
        wait = WebDriverWait(driver, 10)
        my_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#artists-by-letter-results > h3')))

        quantity_of_artists = my_element.text.split("of")[1].strip()
        print(f"- Artists from {letter.upper()}: ({quantity_of_artists})")
    except Exception as error:
        quantity_of_artists = 0
        print(error)
        print(f"---------------- Error to load {letter}")
        pass

    expected = expected + int(quantity_of_artists)

    next_page = True
    while next_page:
        time.sleep(5)

        page.fetch_artists()
        next_page = page.next_page()

    loaded_art = page.get_artists()
    artists = artists + loaded_art
    print(len(loaded_art), quantity_of_artists)

qtd_artists = len(artists)
end_date = datetime.datetime.now()

delta = end_date - start_date

logging.info(f"Artists: {qtd_artists} Expected: {expected} Time: {delta}")

driver.close()

#print(artists)
