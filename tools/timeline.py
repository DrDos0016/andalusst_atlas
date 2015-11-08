#!/usr/bin/python
from __future__ import unicode_literals
import sys, os, json
from datetime import datetime
from datools import *

GALLERY_IDS = {"S1M1-D":"46463019", "S1M1-W":"46463028", "S1M1-L":"47624508", "CONTEST-ART":"51220734"}

def main():
    gallery_key = sys.argv[1]
    print "Main Start: " + str(datetime.now())
    gallery = Gallery("pmdunity", GALLERY_IDS[gallery_key])
    gallery.download(1)
    gallery.soupify()
    gallery.parse()
    
    submissions = gallery.submissions
    del gallery
    
    artists = {}
    output = []
    
    # Group by artist
    for s in submissions:
        if s["author"] in artists:
            artists[s["author"]].append({"date":s["date"], "title":s["title"], "url":s["url"]})
        else:
            artists[s["author"]] = [{"date":s["date"], "title":s["title"], "url":s["url"]}]
    
    # Sort the artists' submissions
    #for artist in artists:
    #    artist = sorted(artist, key=lambda k: (k['date'], k['title'].lower()))
        
    artist_names = sorted(artists, key=lambda k: k[0].lower())
    for artist in artist_names:
        subs = []
        for sub in reversed(artists[artist]):
            subs.append({"date":sub["date"], "title":sub["title"], "url":sub["url"]})
        
        output.append({"artist":artist, "submissions":subs})
    
    output = json.dumps(output, sort_keys=True, indent=4)
    data = open("/var/projects/pmdu.org/assets/data/timeline/"+gallery_key+".json", "w")
    data.write(output)
    data.close()
    
    print "Main End  : " + str(datetime.now())
    return
    
if __name__ == "__main__":main()