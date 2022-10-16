from rocksmith_plus_songs.pages.RocksmithPage import RocksmithPage
from rocksmith_plus_songs.pages.ArtistPage import ArtistPage
from selenium.webdriver.common.by import By
from bba_playlist.Artist import Artist


class LetterPage(RocksmithPage):
    def __init__(self, letter, driver):
        url = f"https://www.ubisoft.com/en-us/game/rocksmith/plus/song-library/search/artists/{letter}/1"
        super().__init__(url, driver)
        self.artist_page = None
        self.urls = []

    def get_urls(self):
        return self.urls

    def get_artists(self):
        return self.data

    def fetch_data(self):
        target = self.get_target()

        if not self.element_exists(target, 10):
            return []

        urls = self.query_selector_all('a.d-block.text.text-decoration-none')
        elements = self.driver.find_elements(By.CSS_SELECTOR, target)
        for index, element in enumerate(elements):
            self.insert_data(element.text)
            self.urls.append(urls[index].get_attribute('href'))

    def insert_songs_to_artist(self, artist, songs):
        for song in songs:
            artist.add_song(song.strip())

        return artist

    def fetch_artists_songs(self):
        artists = []
        for index, url in enumerate(self.urls):
            artist_page = ArtistPage(url, self.driver)

            next_page = True
            while next_page:
                artist_page.fetch_data()
                next_page = artist_page.next_page()

            artist = Artist(self.data[index])
            self.insert_songs_to_artist(artist, artist_page.get_data())

            artists.append(artist)

        return artists
