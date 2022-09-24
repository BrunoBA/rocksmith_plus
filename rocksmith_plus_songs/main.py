from urllib.request import urlopen

url = "https://www.ubisoft.com/en-us/game/rocksmith/plus/song-library/search/artists/a/1"

response = urlopen(url)
html = response.read()

print(html)

#soup = BeautifulSoup(html, 'html.parser')

#print(soup.find('p').get_text())