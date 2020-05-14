#Loading Libraries
import urllib
import urllib.request
import time
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import os
import webbrowser
from bs4 import BeautifulSoup
from random import shuffle

#takes the url to a lyric file and writes a text file with the lyrics to the specified path
def url_to_lyric_file(url, path):
    try:
        thepage = urllib.request.urlopen(url)
    except ConnectionError:
        print ('Connection failed, you got kicked off')
        answer = input('Enter anything and hit enter to continue:')
        thepage = urllib.request.urlopen(url)
    soup = BeautifulSoup(thepage,"html.parser")
    lyrics_html = (soup.find_all('div', class_=''))
    lyrics_raw = ((lyrics_html[1]).get_text()).lower()
    lyrics = remove_punctuation(lyrics_raw, 0, 0).split()
    artist_title_html = soup.find_all('b')
    artist = artist_name_fixer(artist_title_html[0].get_text())
    title = title_name_fixer(artist_title_html[1].get_text())
    title = remove_punctuation(title, 0, 0)
    filename = "/" + artist + '---' + title + '.txt'
    text_file = open((path + filename), 'w+')
    for i in lyrics:
        try:
            text_file.write(i + '\n')
        except UnicodeEncodeError:
            text_file.write('' + '\n')
    return True

#open a text file at path and make it a list of words
def open_file(path):
    reading_file = open(path, 'r')
    return reading_file.read().split()

#this artist fixer is used when parsing links from the site
def artist_name_fixer(artist):
    fixed = (((artist[::-1])[7::])[::-1]).lower()
    return fixed

def artist_name_fixer2(artist):
    artist = (artist.lower()).replace(' ', '')
    artist_fixed = remove_punctuation(artist, 0, 0)
    return artist_fixed

def title_name_fixer(title):
    fixed = ((((title[1::])[::-1])[1::])[::-1]).lower()
    return fixed

#gets rid of the punctuation in the lyrics
def remove_punctuation(lyrics, remove_spaces, lower_case):
    lyrics = lyrics.replace(',', '')
    lyrics = lyrics.replace('.', '')
    lyrics = lyrics.replace('-', '')
    lyrics = lyrics.replace('"', '')
    lyrics = lyrics.replace('(', '')
    lyrics = lyrics.replace(')', '')
    lyrics = lyrics.replace('?', '')
    lyrics = lyrics.replace('!', '')
    lyrics = lyrics.replace('*', '')
    lyrics = lyrics.replace('/', '')
    lyrics = lyrics.replace('>', '')
    lyrics = lyrics.replace('<', '')
    if remove_spaces == 1:
        lyrics =lyrics.replace(' ', '')
    if lower_case == 1:
        lyrics = lyrics.lower()
    return lyrics

#takes the url to an artists page and returns a list of links for all of the songs.
def get_artist_links(artist_page):
    thepage = urllib.request.urlopen(artist_page)
    soup = BeautifulSoup(thepage, "html.parser")
    links_html_raw = (soup.find_all(id="listAlbum"))
    links_html = links_html_raw[0].find_all('a', href=True)
    shuffle(links_html)
    links = []
    counter = 1
    links_length = len(links_html)
    for i in links_html:
        the_link = i.get('href')[2::]
        if the_link[0] == '/':
            the_link = 'https://www.azlyrics.com/' + the_link
        else:
            the_link = 'https://' + the_link[5::]
        links.append(the_link)
        counter += 1
    print('All %s links parsed' % (links_length))
    return links

#take an ACCURATE name of an artist and return the relevant url to use to access their songs
def artist_name_to_artist_link(artist_name):
    artist_name_nospace = artist_name_fixer2(artist_name)
    if artist_name[0] == '0' or artist_name[0] == '1' or artist_name[0] == '2' or artist_name[0] == '3' or artist_name[0] == '4' or artist_name[0] == '5' or artist_name[0] == '6' or artist_name[0] == '7' or artist_name[0] == '8' or artist_name[0] == '9' or artist_name[0] == '10':
        theurl = 'https://www.azlyrics.com/19/' + artist_name_nospace + '.html'
    elif artist_name[:3] == 'the':
        theurl = 'https://www.azlyrics.com/' + artist_name[3] + '/' + artist_name_nospace[3::] + '.html'
    else:
        theurl = 'https://www.azlyrics.com/' + artist_name[0] + '/' + artist_name_nospace + '.html'
    req = Request(theurl)
    try:
        response = urlopen(req)
    except HTTPError as e:
        status = 0
    except URLError as e:
        status = 0
    else:
        status = 1
    url_dict = {'url':theurl, 'status':status, 'artist':artist_name_nospace}
    return url_dict
    

#Take artist name, and make a folder with their name at the folder path, then scrape all their songs into lyric files there.
def artist_name_to_lyrics_folder(artist_name, folder_path):
    artist_link_dict = artist_name_to_artist_link(artist_name)
    newfolder = folder_path + '/' + artist_link_dict['artist']
    print(artist_link_dict)
    if artist_link_dict['status'] == 1:
        links_list = get_artist_links(artist_link_dict['url'])

        if not os.path.exists(newfolder):
            os.makedirs(newfolder)
            counter = 0
            num_of_links = len(links_list)
            print('Scraping commenced...')
            for i in links_list:
                url_to_lyric_file(i, newfolder)
                counter += 1
                if counter % 5 == 0:
                    print('%s out of %s lyric links scraped' % (counter, num_of_links))
                time.sleep(5)
            print ('finished scraping!')
            return newfolder
        else:
            print ('folder already exists!')
            answer = input('continue anyway? y/n: ')
            if answer == 'y' or answer == 'Y':
                print ('Scraping commenced...')
                counter = 0
                num_of_links = len(links_list)
                for i in links_list:
                    url_to_lyric_file(i, newfolder)
                    counter += 1
                    if counter % 5 == 0:
                        print('%s out of %s lyric links scraped' % (counter, num_of_links))
                    time.sleep(1)
                print('finished scraping!')
                return newfolder
            else:
                return 0
    else:
        print ('there is a problem with: %s' % (artist_name))
        return 0

#class used for comparing two lyric files
class two_song_report():
    def __init__(self, list_report, phrases_dict, longest_phrase, highest_length, longest_phrase_location):
        self.list_report = list_report
        self.phrases_dict = phrases_dict
        self.longest_phrase = longest_phrase
        self.highest_length = highest_length
        self.longest_phrase_location = longest_phrase_location

#compares two lyric text files and returns a results class which contains all the matching phrases, longest phrase, etc (see class)
def compare_two_file(file_1_path, file_2_path):
    file_1 = open_file(file_1_path)
    file_2 = open_file(file_2_path)
    reporting_list = []
    matching_phrases = {}
    best_combo = 0
    longest_phrase_location = []
    for i, iword in enumerate(file_1[:len(file_1):]):
        for j, jword in enumerate(file_2[:(len(file_2)):]):
            current_combo = 0
            current_phrase = ''
            while jword == iword:
                current_phrase += iword
                current_combo += 1
                if (j + current_combo) >= len(file_2) or (i + current_combo) >= len(file_1):
                    break
                else:
                    jword = file_2[(j + current_combo)]
                    iword = file_1[(i + current_combo)]
                    current_phrase += ' '
            if current_combo != 0:
                if current_combo > best_combo:
                    best_combo = current_combo
                    longest_phrase_location = [i+1, len(file_1), j+1, len(file_2)]
                try:
                    reporting_list[((current_combo) - 1)] += 1
                except IndexError:
                    while len(reporting_list) < (current_combo - 1):
                        reporting_list.append(0)
                    reporting_list.append(1)
                try:
                    matching_phrases[str(current_combo)].append(current_phrase)
                except KeyError:
                    matching_phrases[str(current_combo)] = [current_phrase]
            iword = file_1[i]
    try:
        longest_phrase = (matching_phrases[str(len(reporting_list))])[0]
    except KeyError:
        longest_phrase = ''
    return two_song_report(reporting_list, matching_phrases, longest_phrase, len(reporting_list), longest_phrase_location)

#take an artist name as input along with base_folder and return a list of that artists text files
def artist_lyric_text_files(artist_name, base_folder):
    artist_name_fixed = remove_punctuation(artist_name, 1, 1)
    folder_path = base_folder + '/' + artist_name_fixed
    if os.path.exists(folder_path):
        lyric_files = os.listdir(folder_path)
        lyric_file_paths = [folder_path + '/' + i for i in lyric_files]
        return lyric_file_paths
    else:
        print('haven\'t downloaded it m8, but lets do that now')
        folder_path = artist_name_to_lyrics_folder(artist_name, base_folder)
        lyric_files = os.listdir(folder_path)
        lyric_file_paths = [folder_path + '/' + i for i in lyric_files]
        return lyric_file_paths

def lyric_file_to_song_name(text_file_path):
    without_txt_reversed = (text_file_path[:text_file_path.find('.txt'):])[::-1]
    artist_song = (without_txt_reversed[:without_txt_reversed.find('/'):])[::-1]
    return artist_song

#takes two artist names, have to be correct spelling (though it will lower case and despace them), and the base folder they will be located. Returns a report which includes all
def artist_compare(artist_1, artist_2, basefolder, min_phrase_length):
    artist_1_files = artist_lyric_text_files(artist_1, basefolder)
    artist_2_files = artist_lyric_text_files(artist_2, basefolder)
    artist_1_files_length = len(artist_1_files)
    artist_2_files_length = len(artist_2_files)
    total = artist_1_files_length * artist_2_files_length
    comparison_report_name = artist_1 + ' vs ' + artist_2 + '.txt'
    comparison_report = open((basefolder + '/' + comparison_report_name), 'w+')
    best_match = 0
    counter = 0
    for i in artist_1_files:
        for j in artist_2_files:
            if counter % 250 == 0:
                print ('Completed %s out of %s' %(str(counter), str(total)))
            ij_results = compare_two_file(i, j)
            if ij_results.highest_length >= int(min_phrase_length):
                if ij_results.highest_length > best_match:
                    best_match = ij_results.highest_length
                    best_match_phrase = ij_results.longest_phrase
                iname = lyric_file_to_song_name(i)
                jname = lyric_file_to_song_name(j)
                report_line = iname + ' and ' + jname + '\n' + str(ij_results.highest_length) + '\n' + str(
                    ij_results.longest_phrase) + ', at ' + str(ij_results.longest_phrase_location) + '\n' + str(ij_results.list_report) + '\n' + str(
                    ij_results.phrases_dict) + '\n\n'
                comparison_report.write(report_line)
            counter += 1
    webbrowser.open(basefolder + '/' + comparison_report_name)
    return two_song_report([], {}, best_match_phrase, best_match, [])

def list_folders(base_folder):
    directory_list = list()
    for root, dirs, files in os.walk(base_folder, topdown=False):
        for name in dirs:
            directory_list.append(os.path.join(name))
            print (name)
    return directory_list

def compare_all_artists(basefolder, tolerance):
    artist_list = list_folders(basefolder)
    print (artist_list)
    for i in artist_list:
        print ('Setting artist 1 to %s' % (i))
        for j in artist_list:
            if i != j:
                artist_compare(i, j, basefolder, tolerance)
    return 0

def file_word_histogram(text_file_path):
    pass