#!/usr/bin/python
from __future__ import unicode_literals
import sys, os, urllib, json
from datetime import datetime
from bs4 import BeautifulSoup
from zipfile import ZipFile
from natsort import *

GALLERIES = {
    "S1M1":"46463019"
}

GALLERY_ROOT = "/var/projects/pmdu.org/assets/data/galleries/"
ARTIST_ROOT = "/var/projects/pmdu.org/assets/data/artists/"
CBR_ROOT = "/var/projects/pmdu.org/assets/data/cbrs/"

def main():
    choices = GALLERIES.keys()
    print ", ".join(choices)
    input = raw_input("Select Mission: ")
    if input not in GALLERIES.keys():
        input = "S1M1"
    mission = input
    
    # Use existing artist names
    if os.path.isfile(ARTIST_ROOT + mission + ".json"):
        json_file = open(ARTIST_ROOT + mission + ".json")
        comics = json.loads(json_file.read())
        json_file.close()
    else:
        # Download relevant data
        files = download_gallery(mission)
        comics = parse_gallery(files)
        
        # Save it for next time
        json_comics = json.dumps(comics, sort_keys=True)
        json_file = open(ARTIST_ROOT + mission + ".json", "w")
        json_file.write(json_comics)
        json_file.close()
    
    
    looping = True
    while looping:
        # List Artists
        for key in sorted(comics.keys()):
            print key,
        input = raw_input("\nUser to download: ")
        if not comics.get(input):
            if input == "":
                sys.exit()
            print "User not found"
            continue
        
        # Download
        download(input, mission, comics)
    return

def download_gallery(mission):
    start = datetime.now()
    
    gallery = GALLERIES[mission]
    url = "http://pmdunity.deviantart.com/gallery/?set="+gallery+"&offset="
    offset = 0
    files = []
    while True:
        filename = mission + "_" + str(offset)
        if os.path.isfile(GALLERY_ROOT + "/" + filename):
            print "Found " + filename
            offset += 24
            files.append(filename)
            continue
        else: # Pull from DA
            try:
                page = urllib.urlopen(url + str(offset)).read()
                if "This section has no deviations yet!" in page:
                    break
            except:
                print "Error reading page for "+mission+":\n" + url + str(offset)
                sys.exit()
            scraped = open(GALLERY_ROOT+"/"+filename, "w")
            scraped.write(page)
            scraped.close()
            print "Saved gallery page.", offset / 24 + 1
            offset += 24
            files.append(filename)
    return files

def parse_gallery(files):
    comics = {}
    blocked = {}
    progress = 0
    for file in files:
        page = open(GALLERY_ROOT+"/"+file, "r").read()
        soup = BeautifulSoup(page)
        submissions = soup.find_all("span", {"class":"details"})
        image_data = soup.find_all("a", {"class":"thumb"})
        x = 0
        for submission in submissions:
            if x >= len(image_data):
               continue
            link = image_data[x].get("data-super-full-img")
            if not link:
                link = image_data[x].get("data-super-img")
            
            title = submission.find_all("a")[0].get("title")
            username = submission.find_all("a")[0].get("href")
            username = username[7:]
            username = username[:username.find(".deviantart")]
            
            if not link: # Skip this one for now
                if not blocked.get(username):
                    blocked[username] = True
                    print "NO LINK FOR", username, "-\n", title
                x += 1
                continue
            
            if comics.get(username):
                comics[username].append({"link":link, "title":title})
            else:
                comics[username] = [{"link":link, "title":title}]
            x += 1
        progress += 1
        print str(progress) + " / " + str(len(files) )
    
    print blocked.keys()
    print comics.keys()
    for block in blocked.keys():
        if comics.get(block):
            del comics[block]
        
    return comics
    
def download(artist, mission, comics):
    data = comics.get(artist)
    data = sorted(data, key=lambda pagesort: pagesort["title"])
    files = []
    for page in data:
        filename = page["link"].split("/")[-1]
        (fname, headers) = urllib.urlretrieve(page["link"], filename)
        files.append(fname)
        
    # Sort pages (I hope)
    natsort(files, natcasecmp)
    
    zip = ZipFile(CBR_ROOT + 'PMDU-'+mission+'- ' + artist + '.cbr', 'w')
    count = 1
    for file in files:
        ext = file.split(".")[-1]
        pagecount = ("000"+str(count))[-3:]
        zip.write(file, pagecount + "." + ext)
        print "Wrote " + pagecount + "("+file+")"
        os.remove(file)
        count += 1
    zip.close()
    print "DOWNLOADED."
if __name__ == "__main__": main()