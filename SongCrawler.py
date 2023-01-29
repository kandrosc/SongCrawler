import re
import requests
import urllib.request
import os, sys
import json
from multiprocessing import Process
from bs4 import BeautifulSoup
from pytube import YouTube
FILEPATH = os.path.dirname(os.path.abspath(__file__)) + "/"
with open(FILEPATH+"config.json","r") as f: config=json.loads(f.read())

helpString = '''

Arguments:
0 - Write example html files
1 - Download individual song with url as input
2 - Download selected albums with artist name / numeric input

'''
# Downloads two html files that have examples of the two types of containers that contain albums / songs
def writeExamples():
        for i, artist in enumerate(['imagine dragons', 'july talk']):
            r = requests.get("https://www.google.com/search?q={}+albums".format(artist.replace(" ","+")))
            with open(FILEPATH+"example-%s%s.html" % ("no-"*i,"image"),"w") as f: f.write(r.text)

# Downloads a song using the provided url, name (optional), convert it to .mp3, and move it to the music directory
def downloadSong(url, name=""):
    yt = YouTube(url)
    streams = yt.streams.filter(only_audio=True)
    # sort streams by abr
    streams = sorted(streams, key=lambda x: int(x.abr.split("kbps")[0]))[::-1]
    f = streams[0].download()
    filename = (name if name else os.path.basename(f)[:-5]) + '.mp3'
    os.system('ffmpeg -i "%s" -vn -ab 128k -ar 44100 -y "%s"' % (f,config['music_dir'] + '\\' + filename))
    os.remove(f)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(helpString)
    else:
        try:
            arg = int(sys.argv[1])
            if arg not in [0,1,2]:
                print(helpString)
            else:
                if arg == 0:
                    writeExamples()
                elif arg == 1:
                    url = input("Enter the url of the song you would like to download: ")
                    name = input("Enter the name you would like the file to be renamed to (optional): ")
                    downloadSong(url, name)
                else:
                    print(2) 
        except ValueError:
            print(helpString)
    '''
    
    artist = input("Enter the name of the artist you would like to download music from: ")
    r = requests.get("https://www.google.com/search?q={}+albums".format(artist.replace(" ","+")))
    with open(FILEPATH+"test.html","w") as f: f.write(r.text)
    '''