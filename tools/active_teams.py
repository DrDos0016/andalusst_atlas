#!/usr/bin/python
import os, sys
sys.path.append("/var/projects/pmdu.org")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pmdu.settings")
from django.db.models import Count
from pmdunity.models import *
from datetime import date, timedelta

def main():
    # Get a list of teams that submitted logbooks in the past 90 days
    today = date.today()
    cutoff = today - timedelta(days=90)
    logs = Logbook.objects.filter(submitted__gte=cutoff).annotate(Count("id")).order_by("submitted")
    active = []
    for log in logs:
        active.append(log.team.id)
        
    # Get a list of teams that joined in the past 90 days too
    teams = Team.objects.filter(joined__gte=cutoff).annotate(Count("id"))
    for team in teams:
        active.append(team.id)
        
    # Mark all active teams not in the list as inactive
    Team.objects.filter(active=True).exclude(id__in=active).update(active=False)
    # Mark all teams in the list as active
    Team.objects.filter(id__in=active).update(active=True)
    return True
if __name__ == "__main__": main()