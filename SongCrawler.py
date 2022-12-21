import re
import requests
import urllib.request
import os
import json
from multiprocessing import Process
from bs4 import BeautifulSoup
FILEPATH = os.path.dirname(os.path.abspath(__file__)) + "/"

if __name__ == "__main__":
    with open(FILEPATH+"config.json","r") as f: config=json.loads(f.read())

    artist = input("Enter the name of the artist you would like to download music from: ")
    r = requests.get("https://www.google.com/search?q={}+albums".format(artist.replace(" ","+")))
    with open(FILEPATH+"test.html","w") as f: f.write(r.text)