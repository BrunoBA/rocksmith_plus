#encoding: utf-8

import logging
import datetime
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from string import ascii_lowercase as alc
from rocksmith_plus_songs.pages.ArtistPage import ArtistPage
from selenium.webdriver.chrome.service import Service
from pyvirtualdisplay import Display


logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(asctime)s %(message)s")
display = Display(visible=0, size=(800, 600))
display.start()

options = Options()
options.add_argument("--window-size=1920x1080")
options.add_argument("--verbose")
options.add_argument("--headless") # if you want it headless
options.add_argument('--no-sandbox')
options.add_argument("--enable-automation")
options.add_argument('--disable-gpu')

start_date = datetime.datetime.now()

#driver = webdriver.Chrome(ChromeDriverManager().install())
options.BinaryLocation = ("/usr/bin/chromium-browser")
#service = Service("/home/admin/chromedriver_linux")
#service = Service("/usr/bin/chromedriver")
service = Service("/usr/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=options)
try:
    driver.get("https://www.ubisoft.com/en-us/game/rocksmith/plus/song-library/search/artists/symbol/1")
except TimeoutException as ex:
   print(ex.Message)
   driver.navigate().refresh()

try:
    wait = WebDriverWait(driver, 7)
    cookies_consent = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#privacy__modal__close")))
    cookies_consent.click()
except:
    pass


artists = []
for letter in alc:
    page = ArtistPage(letter, driver)
    artists = artists + page.get_artists()

    try:
        wait = WebDriverWait(driver, 7)
        myElem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#artists-by-letter-results > h3')))
    except:
        pass

qtd_artists = len(artists)
end_date = datetime.datetime.now()

delta = end_date - start_date

logging.info(f"Artists: {qtd_artists} Time: {delta}")

driver.close()