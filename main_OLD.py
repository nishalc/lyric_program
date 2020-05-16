from functions import *

basefolder = "C:/Lyric data/"

print('Welcome to the amazing lyric matcher scraper 2000\n')
print('Current base folder = ' + basefolder)
while True:
    print ('1 - Download an artists lyrics to an artist folder')
    print ('2 - Compare Artists')
    print ('3 - Compare ALL Artists (will take hella long!')
    print ('4 - Artist common words histogram')
    answer = input('Please select from the above options: ')
    if answer == '1':
        artist_name = input('Please enter the artist name (accurate spelling a must!): ')
        artist_name_to_lyrics_folder(artist_name, basefolder)
        print ('%s successfully added to artist database' % (artist_name))
    elif answer == '2':
        artist_1_name = input('Select artist 1: ')
        artist_2_name = input('Select artist 2: ')
        min_phrase_length = int(input('Please select the minimum number of words in a phrase to report: '))
        artist_comparison = artist_compare(artist_1_name, artist_2_name, basefolder, min_phrase_length)
        print ('Great success! The longest match between the artists was \"%s\" ' % (artist_comparison.longest_phrase))
        break
    elif answer == '3':
        min_phrase_length = int(input('Please select the minimum number of words in a phrase to report: '))
        compare_all_artists(basefolder, min_phrase_length)
    elif answer == '4':
        print ('noooop dooop')
    else:
        print ('that isn\'t one of the options!')
