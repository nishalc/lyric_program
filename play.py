import urllib.request
from bs4 import BeautifulSoup
import nltk.data
from nltk.tokenize import wordpunct_tokenize

import re
test_url = 'https://www.azlyrics.com/lyrics/queen/bohemianrhapsody.html'
base = "C:/Lyric data"



thepage = urllib.request.urlopen(test_url)
soup = BeautifulSoup(thepage,"html.parser")
#lyrics_html = (soup.find ('div', class_=''))
album = soup.find('div', class_='songinalbum_title').get_text()
album = re.findall(r'"(.*?)"', album)[0] # take album name out of the quotes

#print(soup)
print(album)