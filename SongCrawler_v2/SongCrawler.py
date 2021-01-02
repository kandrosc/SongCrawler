import re
import requests
import urllib.request
import os
import json
import time
from tkinter import *
from multiprocessing import Process, Queue
from bs4 import BeautifulSoup
FILEPATH = os.path.dirname(os.path.abspath(__file__)) + "/"
Q = Queue()

# Returns a tuple formatted like this: (artist name (in case the artist is mispelled) and album dict)
def getAlbums(artist,config):
    r = requests.get("https://www.google.com/search?q={}+albums".format(artist.replace(" ","+")))
    with open(FILEPATH+"test.html","w") as f: f.write(r.text)
    soup = BeautifulSoup(r.text,"html.parser")
    containers = soup.findAll("div",{"class":config["album"]["container_class"]})
    for c in containers:
        if artist.lower()+"albums" in c.text.lower(): 
            album_container = c
            break
    # Links to album page
    try: album_links = album_container.findAll("a")
    except UnboundLocalError: # misspelled artist
        error_msg = soup.find(id="scc")
        if error_msg:
            error_txt = error_msg.text
            new_artist = re.findall("(?<=Showing results for )(.*?)(?= albums)",error_txt)[0]
            getAlbums(new_artist,config)
            return 0
        else:
            Q.put(0)
            return 0

    album_links = ["https://www.google.com"+a["href"] for a in album_links]

    albums = {}
    for link in album_links:
        # Get songs for each album
        r = requests.get(link)
        soup = BeautifulSoup(r.text,"html.parser")
        containers = soup.findAll("div",{"class":config["album"]["container_class"]})
        for c in containers:
            if "album by "+artist.lower() in c.text.lower(): 
                album_container = c
                album_name = c.text[:c.text.lower().index("album by "+artist.lower())]
                break
            
        with open(FILEPATH+"test2.html","w") as f: f.write(r.text)
        try: song_container = album_container.findAll("div",{"class":config["song"]["container_class"]})[0] # Should only be one of this class!
        except IndexError: continue
        songs = []
        song_links = song_container.findAll("div",{"class":config["song"]["name_class"]})
        for song in song_links: songs.append(BeautifulSoup(song.text,"html.parser").text)
        albums[album_name] = songs
    Q.put((artist,albums))


def displayAlbums(window,artist,loading,config):
    p = Process(target=getAlbums,args=(artist,config))
    template, n, i = "Loading...", len("Loading..."), 3
    p.start()
    while p.is_alive():
        i=i%4
        loading.config(text=template[:n-i])
        window.update()
        i-=1
        time.sleep(1)
    response = Q.get()
    print(response)
    if not response:
        loading.config(text="Could not find albums for: "+artist)
        window.update()
        return 0
    artist, albums = response[0], response[1]
    loading.config(text="Found albums for artist: "+artist)
    window.update()

if __name__ == "__main__":
    with open(FILEPATH+"config.json","r") as f: config=json.loads(f.read())

    window = Tk()
    window.title("SongCrawler")
    window.geometry("1000x600")

    Label(window,text="Enter the name of the artist you would like music from:",fg="black").grid(row=0,column=0,sticky=W)
    artist = Entry(window,width=40,bg="white")
    artist.grid(row=0,column=1,sticky=W)
    loading = Label(window,text="",fg="black")
    loading.grid(row=1,column=0,sticky=W)

    Button(window,text="TEST",width=4,command=lambda:displayAlbums(window,artist.get(),loading,config)).grid(row=0,column=2,stick=W)


    window.mainloop()

    '''
    artist = input("Enter the name of the artist you would like to download music from: ")
    with open(FILEPATH+"config.json","r") as f: config=json.loads(f.read())
    r = requests.get("https://www.google.com/search?q={}+albums".format(artist.replace(" ","+")))
    with open(FILEPATH+"test.html","w") as f: f.write(r.text)
    print(config["html_start"])
    print(config["html_end"])
    for i in re.findall("(?<={0})(.*)(?={1})".format(config["html_start"],config["html_end"]),r.text): print(i)
    '''