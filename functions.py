import urllib.request
from bs4 import BeautifulSoup
import nltk.data
from nltk.tokenize import wordpunct_tokenize
import re
import pickle
import os
from pathlib import Path
import random


def url_to_soup(url):
    req = urllib.request.Request(url, headers={
        'Referer': 'https://www.google.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30'
    })
    thepage = urllib.request.urlopen(req)
    soup = BeautifulSoup(thepage, 'html.parser')
    return soup

def soup_to_lyric_file(soup, base):
    lyrics_html = (soup.find ('div', class_=''))
    lyrics_raw = (lyrics_html).get_text().lower().replace("'",'') # get rid of apostroches cause they suck
    lyrics_raw = re.sub("[\(\[].*?[\)\]]", "", lyrics_raw) # gets rid of anything in brackets
    lyrics = wordpunct_tokenize(lyrics_raw) # this is a list of all the words and punctuation we kept

    artist_title_html = soup.find_all('b')
    artist = artist_title_html[0].get_text().replace(' Lyrics','')
    title = artist_title_html[1].get_text().replace('"','')
    album = soup.find('div', class_='songinalbum_title').get_text()
    album = re.findall(r'"(.*?)"', album)[0]  # take album name out of the quotes

    directory = base + '/' + artist + '/' + album
    filename = artist + '---' + title
    Path(directory).mkdir(parents=True, exist_ok=True)
    full_path = directory + '/' + filename + '.txt'

    with open(full_path, "wb") as fp:  # dump data in text file
        pickle.dump(lyrics, fp)

    return True

def get_artist_links(artist_url):
    thepage = urllib.request.urlopen(artist_url)
    soup = BeautifulSoup(thepage, "html.parser")
    links_html_raw = (soup.find_all(id="listAlbum"))
    links_html = links_html_raw[0].find_all('a', href=True)
    random.shuffle(links_html)
    links = []
    for i in links_html:
        the_link = i.get('href')[2::]
        if the_link[0] == '/':
            the_link = 'https://www.azlyrics.com/' + the_link
        else:
            the_link = 'https://' + the_link[5::]
        links.append(the_link)
    print('All %s links parsed' % (len(links_html)))
    return links

def scape_artist(artist_url):
    # take the artist url and download all of their songs
    pass

test_song = 'https://www.azlyrics.com/lyrics/queen/bohemianrhapsody.html'
test_artist = 'https://www.azlyrics.com/a/aaronlewis.html'
base = "C:/Lyric data"

soup = url_to_soup(test_song)
bin = soup_to_lyric_file(soup, base)
#with open(full_path, 'rb') as f:
 #   data = pickle.load(f)

#print(get_artist_links(test_artist))