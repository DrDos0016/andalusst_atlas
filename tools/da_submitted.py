#!/usr/bin/python
import urllib
import os, sys
sys.path.append("/var/projects/pmdu.org")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pmdu.settings")
from pmdunity.models import *
from bs4 import BeautifulSoup

def main():
    teams = []
    logs = Logbook.objects.exclude(event_id=-1).order_by("team", "-id")
    
    for log in logs:
        if log.team_id in teams:
            continue
        
        teams.append(log.team)
        url = log.url
        text = urllib.urlopen(url).read()
        soup = BeautifulSoup(text, "lxml")
        
        #start = text.find("<span offset=\"-1\"") + 17
        #submitted = text[start:start+100]
        print log.team.name
        

if __name__ == "__main__": main()