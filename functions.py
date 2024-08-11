import urllib.request
from bs4 import BeautifulSoup
import nltk.data
from nltk.tokenize import wordpunct_tokenize
import re
import pickle
import os
from pathlib import Path
import random
import time

def url_to_soup(url, headers):
    req = urllib.request.Request(url, headers=headers)
    thepage = urllib.request.urlopen(req)
    soup = BeautifulSoup(thepage, 'html.parser')
    return soup

def soup_to_lyrics(soup):
    lyrics_html = (soup.find_all('div', class_=''))
    lyrics_raw = lyrics_html[4].get_text().lower()
    # gets rid of anything in brackets, because they are markers that say who is singing
    lyrics_raw = re.sub("[\(\[].*?[\)\]]", "", lyrics_raw) 
    return lyrics_raw

def remove_punctuation(s):
    return s.translate(str.maketrans('', '', '"#$%&\'()*+-/:;<=>@[]^_`{|}~?!,'))

def lyrics_raw_to_tokens(lyrics_raw):
    lyrics_nopunc = remove_punctuation(lyrics_raw) # get rid of apostroches
    lyrics_tokens = wordpunct_tokenize(lyrics_nopunc)
    return lyrics_tokens

def soup_to_metadata(soup):
    artist_title_html = soup.find_all('b')
    artist = artist_title_html[0].get_text().replace(' Lyrics','') #problematic
    title = soup.find_all('b')[1].get_text().replace('"',"").lower()

    try: # find the album title if there is one
        album_raw = soup.find('div', class_='songinalbum_title').get_text()
        album_title = re.findall(r'"(.*?)"', album_raw)[0]
        year = re.findall('\(.*?\)', album_raw)[0][1:-1]
        album = f"{album_title}---{year}"
    except AttributeError:
        album = 'No album'
    return artist, album, title

# given a soup file and a base directory, will extract the lyrics
# and save a text file with raw text to in the base directory with structure ARTIST/ALBUM/SONG
def soup_to_lyric_file(soup, base_dir):
    lyrics_raw = soup_to_lyrics(soup)
    artist, album, title = soup_to_metadata(soup)
    
    directory = Path(base_dir) / artist / album
    filename = artist + '---' + title + '.txt'
    directory.mkdir(parents=True, exist_ok=True)

    with open(directory / filename, "w") as lyrics_file:  # dump data in text file
        lyrics_file.write(lyrics_raw)
    return True

def artist_name_to_artist_link(artist_name):
    artist_name_nospace = remove_punctuation(artist_name.lower().replace(" ", ""))
    if artist_name_nospace[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        url = 'https://www.azlyrics.com/19/' + artist_name_nospace + '.html'
    elif artist_name_nospace[:3] == 'the':
        url = 'https://www.azlyrics.com/' + artist_name_nospace[3] + '/' + artist_name_nospace[3::] + '.html'
    else:
        url = 'https://www.azlyrics.com/' + artist_name_nospace[0] + '/' + artist_name_nospace + '.html'
    return url

# given the URL for an artist, will generate all song URL's
def get_artist_links(artist_url):
    soup = url_to_soup(artist_url)
    links_html_raw = soup.find_all(id="listAlbum")
    links_html = links_html_raw[0].find_all('a', href=True)
    links = ['https://www.azlyrics.com/' + i.get('href')[1:] for i in links_html]
    return links

def scrape_artist(artist_url, base_dir, start_indice=0):
    # take the artist url and download all of their songs
    links = get_artist_links(artist_url)
    length = len(links)
    for i, x in enumerate(links[start_indice:]):
        print(f'Attempting {x}')
        while True:
            try:
                soup_to_lyric_file(url_to_soup(x), base_dir)
                sleep_time = 1#random.randint(1,30)
                time.sleep(sleep_time)
                break
            except TimeoutError:
                print('Timeout error, waiting...')
                time.sleep(5)
            except urllib.error.URLError as e:
                ResponseData = e.reason
                print(f'URL error: {ResponseData}, waiting...')
                time.sleep(5)

        print(f'Scraped {i+1} of {length} and waiting')

        with open(os.path.join(base_dir, 'current_progress.txt'), 'w') as f:
            f.write(str(i))
            f.close()
    return True

# takes the directory of an artist folder and returns a
def album_song_lists(artist_dir):
    albums = [os.path.basename(f) for f in os.scandir(artist_dir) if f.is_dir()]
    files = []
    for album in os.listdir(artist_dir):
        album_path = os.path.join(artist_dir,album)
        for r, d, f in os.walk(album_path):
            files.append([os.path.join(album_path, song) for song in f])
    return albums, files



