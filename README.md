# lyric_program

This project was intiated with the following question:

*Given two music artists, what is the longest phrase in common between every song in their respective discographies?* 

The rather messy and incoherent code here managed to achieve this feat by doing the following:
1. Scraping every song by an artist from AZlyrics, removing punctuation and saving to .txt files.
2. Compare one artists folder of songs to another, at a somewhat slow pace
3. Output a text file with the longest phrases in common between the artists.

There are a few issues which I ran into:
* AZlyrics didn't like me scraping lots of webpages at the same time. I tried to look for a way to implement an IP changing VPN in python but didn't have any luck.
* The comparison is quite slow, possible due to not being very efficient. 
* Processing of text was fairly basic, given the lack of experience in NLP.

There is however some potential for this project, ideas include:
1. Looking at the statistics of an artists lyrics overall, which word/phrase is most common, how many times do they say x word per song?
2. Using an artists discography with AI to generate a new song

Unfortunately due to time constraints this project has been left to rot slightly, but may be returned to in the future.
