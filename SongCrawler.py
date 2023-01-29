import re
import requests
import urllib.request
import os, sys
import json
from multiprocessing import Process
from bs4 import BeautifulSoup
FILEPATH = os.path.dirname(os.path.abspath(__file__)) + "/"

helpString = '''

Arguments:
0 - Write example html files
1 - Download individual song with url as input
2 - Download selected albums with artist name / numeric input

'''

def writeExamples():
        for i, artist in enumerate(['imagine dragons', 'july talk']):
            r = requests.get("https://www.google.com/search?q={}+albums".format(artist.replace(" ","+")))
            with open(FILEPATH+"example-%s%s.html" % ("no-"*i,"image"),"w") as f: f.write(r.text)


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
                    print(1)
                else:
                    print(2) 
        except ValueError:
            print(helpString)
    '''
    with open(FILEPATH+"config.json","r") as f: config=json.loads(f.read())
    artist = input("Enter the name of the artist you would like to download music from: ")
    r = requests.get("https://www.google.com/search?q={}+albums".format(artist.replace(" ","+")))
    with open(FILEPATH+"test.html","w") as f: f.write(r.text)
    '''