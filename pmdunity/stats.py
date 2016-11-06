# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


from .common import *

def logbooks(request):
    data = {"session":request.session}
    
    #form = Pokemon_Form()
    #data["form"] = form
    
    #data["counts"]          = Team.objects.values('guild').annotate(guild_count=Count('guild')).order_by("guild")
    raw_stats = Logbook.objects.values("approved", "event__key", "event__name", "event__image").annotate(entry_count=Count("event__key")).order_by("event__id")
    data["stats"] = []
    last_key = ""
    for stat in raw_stats:
        if last_key != stat["event__key"]:
            if last_key != "":
                wip["percent"] = int((1.0 * wip["handled"] / max(wip["total"],1)) * 100)
                data["stats"].append(wip)
            wip = {}
            wip["handled"] = 0
            wip["total"] = 0
            wip["key"] = stat["event__key"]
            wip["name"] = stat["event__name"]
            wip["image"] = stat["event__image"]
            last_key = wip["key"]
        if (stat["approved"] == True) or (stat["approved"] == False) :
            wip["handled"] += stat["entry_count"]
        wip["total"] += stat["entry_count"]
        
    # Write the last one
    wip["percent"] = int((1.0 * wip["handled"] / max(wip["total"],1)) * 100)
    data["stats"].append(wip)
    
    return render(request, "stats/logbook_stats.html", data)

def population(request):
    data = {"session":request.session}
    
    species = Pokemon.objects.values('species').annotate(species_count=Count('species')).order_by("-species_count", "species")
    active = Pokemon.objects.filter(team__active=True).annotate(active_count=Count('species')).order_by("-active_count", "species")
    
    active_dict = {}
    data["species"] = []
    
    for a in active:
        if active_dict.get(a.species):
            active_dict[a.species] += 1
        else:
            active_dict[a.species] = 1
            
    for s in species:
        data["species"].append({"name":NUMBERS[s["species"]], "count":s["species_count"], "active":active_dict.get(s["species"], 0), "dex":s["species"]})
        
    if request.GET.get("sort") == "species":
        data["species"] = sorted(data["species"], key=lambda k: (k["name"].lower()))
    elif request.GET.get("sort") == "active":
        data["species"] = sorted(data["species"], key=lambda k: (-1 * k["active"], k["name"].lower()))
    else:
        data["species"] = sorted(data["species"], key=lambda k: (-1 * k["count"], k["name"].lower()))
    return render(request, "stats/pokemon_population.html", data)
