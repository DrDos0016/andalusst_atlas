import urllib, json
from datetime import datetime
from time import strptime
from bs4 import BeautifulSoup
#apt-get install python-lxml

class Gallery(object):
    def __init__(self, account, id):
        self.page_size = 24
        
        self.id = id
        self.account = account
        self.pages = []
        self.submissions = []
        #print "Working w/ "+account+" gallery "+id
        
    def download(self, start=1, end=32767):
        #print "Downloading pages", start, "through", end
        offset = (start-1) * self.page_size
        end = (end-1) * self.page_size
        while (offset <= end):
            url = "http://"+self.account+".deviantart.com/gallery/?set="+self.id+"&offset="+str(offset)
            print url
            text = urllib.urlopen(url).read()
            
            if "This section has no deviations yet!" in text:
                break
            page = Page(text, start)
            self.pages.append(page)
            offset += self.page_size
            start += 1
        
    def soupify(self):
        for page in self.pages:
            page.soupify()
            
    def parse(self):
        for page in self.pages:
            info = page.parse()
            self.submissions += info
        
class Page(object):
    def __init__(self, text, page_num, truncate=True):
        self.truncate = truncate
        if truncate:
            self.raw = text[text.find("<div class=\"zones-container\""):text.find("<div id=\"depths\"")]
        else:
            self.raw = text
        self.page_num = page_num
        self.soup = None
        
    def save(self, file):
        return True
        
    def soupify(self):
        self.soup = BeautifulSoup(self.raw, "lxml")
        return True
        
    def parse(self):
        if self.soup == None:
            print "Can't parse Page", self.page_num, "until it's been soupified!"
            return False
            
        info = []
        submissions = self.soup.find_all("span", {"class":"tt-w"})
        print "PARSING", self.page_num
        for submission in submissions:
            links = submission.find_all("a")
            
            try:
                url     = links[1].get("href")
                title   = links[1].span.string
                author  = links[2].string
                date    = strptime(links[1].get("title")[-12:].strip(), "%b %d, %Y")
                date    = str(date.tm_year)+"-"+str(date.tm_mon).zfill(2)+"-"+str(date.tm_mday).zfill(2)
                
                if author == None and url: # This handles banned users
                    author = url.split(".deviantart.com")[0].replace("http://", "")
                    if not author:
                        author = "UNKNOWN AUTHOR"
                info.append({"author":author, "url":url, "title":title, "date":date})
            except:
                info.append({"author":"zzzError", "url":"#", "title":"Error parsing: Probably submission in storage (page #"+str(self.page_num)+").", "date":""})
        
        return info