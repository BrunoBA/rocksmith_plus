
import json
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

display = Display(visible=0, size=(800, 600))
display.start()

options = Options()
options.add_argument("--window-size=1920x1080")
options.add_argument("--verbose")
options.add_argument("--headless") # if you want it headless
options.add_argument('--no-sandbox')
options.add_argument("--enable-automation")
options.add_argument('--disable-gpu')

options.BinaryLocation = ("/usr/bin/chromium-browser")
service = Service("/usr/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=options)
try:
    driver.get("https://www.ubisoft.com/en-us/game/rocksmith/plus/song-library/search/artists/symbol/1")
except TimeoutException as ex:
   print(ex.Message)
   driver.navigate().refresh()

try:
    wait = WebDriverWait(driver, 3)
    cookies_consent = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#privacy__modal__close")))
    cookies_consent.click()
except:
    pass


artists = []
for letter in alc:
    page = ArtistPage(letter, driver)
    artists = artists + page.get_artists()

    try:
        wait = WebDriverWait(driver, 2)
        myElem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#artists-by-letter-results > h3')))
    except:
        pass

print(json.dumps(artists, default=lambda o: o.__dict__, sort_keys=True, indent=4))
# print(artists)
driver.close()