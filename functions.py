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

def soup_to_lyric_file(soup, base, artist_name=''):
    lyrics_html = (soup.find ('div', class_=''))

    #processing the lyric data
    lyrics_raw = (lyrics_html).get_text().lower().replace("'",'') # get rid of apostroches

    #lyrics_raw = re.sub("[\(\[].*?[\)\]]", "", lyrics_raw) # gets rid of anything in brackets, WHY?
    lyrics = wordpunct_tokenize(lyrics_raw) # this is a list of all the words and punctuation as separate strings

    artist_title_html = soup.find_all('b')
    if artist_name == '':
        artist = artist_title_html[0].get_text().replace(' Lyrics','') #problematic
    else:
        artist = artist_name
    title = artist_title_html[1].get_text().replace('"','')

    try: # find the album title if there is one
        album_raw = soup.find('div', class_='songinalbum_title').get_text()
        title = re.findall(r'"(.*?)"', album_raw)[0]
        year = re.findall('\(.*?\)', album_raw)[0][1:-1]
        album = title + '---' + 'year'
    except AttributeError:
        album = 'No album'

    directory = base + '/' + artist + '/' + album
    filename = artist + '---' + title
    Path(directory).mkdir(parents=True, exist_ok=True)
    full_path = directory + '/' + filename + '.txt'

    with open(full_path, "wb") as fp:  # dump data in text file
        pickle.dump(lyrics, fp)

    return True

def get_artist_links(artist_url):
    soup = url_to_soup(artist_url)
    artist = soup.find_all('h1')[0].get_text().replace(' Lyrics', '')
    links_html_raw = soup.find_all(id="listAlbum")
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
    links.sort()
    return links, artist

def scrape_artist(artist_url, base):
    # take the artist url and download all of their songs
    links, artist = get_artist_links(artist_url)
    length = len(links)
    for i, x in enumerate(links[:5]):
        print(f'Attempting {x}')
        while True:
            try:
                soup_to_lyric_file(url_to_soup(x), base, artist)
                break
            except TimeoutError:
                print('Timeout error, waiting...')
                time.sleep(10)
            except urllib.error.URLError as e:
                ResponseData = e.reason
                print(f'URL error: {ResponseData}, waiting...')
                time.sleep(10)

        print(f'Done {i+1} of {length} and waiting')

        with open(os.path.join(base, 'current_progress.txt'), 'w') as f:
            f.write(str(i))
            f.close()

        time.sleep((random.randint(0,20)))

    return 0

# takes the directory of an artist folder and returns a
def album_song_lists(artist_dir):
    albums = [os.path.basename(f) for f in os.scandir(artist_dir) if f.is_dir()]
    files = []
    for album in os.listdir(artist_dir):
        album_path = os.path.join(artist_dir,album)
        for r, d, f in os.walk(album_path):
            files.append([os.path.join(album_path, song) for song in f])
    return albums, files

test_song = 'https://www.azlyrics.com//lyrics/kanyewest/breatheinbreatheout.html'
test_artist = 'https://www.azlyrics.com/w/west.html'
base = "C:/Lyric data"

#soup = url_to_soup(test_song)
#bin = soup_to_lyric_file(soup, base)

#with open(full_path, 'rb') as f:
 #   data = pickle.load(f)

soup_to_lyric_file(url_to_soup(test_song), base)


