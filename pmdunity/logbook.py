# -*- coding: utf-8 -*-
from common import *

def logbook_arrange(request, id):
    data = {"session":request.session}
    team = get_team(id, request.session)
    if not team:
        return redirect("/")
    data["team"] = team
    if team.user.id == request.session.get("userID") or request.session.get("admin"):
        data["yours"] = True
    else:
        return redirect("/")
    
    # Add entry
    if request.POST.get("action") == "arrange":
        logbook_ids = request.POST.getlist("logbook_id")
        for x in xrange(0, len(logbook_ids)):
            entry = Logbook.objects.get(pk=logbook_ids[x])
            entry.order = x
            entry.save()
        return redirect("/logbook/view/"+str(data["team"].id)+"/")
    
    data["logbook"] = Logbook.objects.filter(team__id=id).order_by("order")
    events = Event.objects.exclude(id__in=data["logbook"].values_list("event__id", flat=True))
    
    data["events"] = []
    for event in events:
        if event.key == "ORIG":
            continue
        elif team.guild == "Explorers" and "E" in event.guilds:
            data["events"].append(event)
        elif team.guild == "Hunters" and "H" in event.guilds:
            data["events"].append(event)
        elif team.guild == "Researchers" and "R" in event.guilds:
            data["events"].append(event)
        #else:
        #    print "Skipping ", event.key
        
    data["icons"] = form_select_pokemon("Ditto")
    return render_to_response("logbook/logbook_arrange.html", data, context_instance=RequestContext(request))

def logbook_bookmarks(request):
    data = {"session":request.session}
    if not request.session.get("userID") or not request.session.get("beta"):
        return redirect("/logbook/browse")
        
    data["sort"] = request.GET.get("sort", "-id")
    teams = Bookmark.objects.filter(user_id=request.session.get("userID")).values_list('team_id', flat=True)
    data["logbooks"] = Logbook.objects.filter(team__id__in=teams).order_by("-event__id", "team__name").exclude(event__key="APP")[:100]
    
    return render_to_response("logbook/logbook_bookmarks.html", data)

def logbook_browse(request, key=None):
    data = {"session":request.session}
    results_size = request.session.get("results", RESULTS)
    data["key"] = request.GET.get("key", key) # Backwards compat with old GET param
    if not data["key"]:
        data["events"] = Event.objects.filter(pk__gte=2)
    else:
        if re.match(r"S[0-9+]D[0-9]+", data["key"]):
            data["dungeon"] = True
            data["dungeon_id"] = 2 # TODO Make this not hard coded.
        data["url"] = "/logbook/browse/"+data["key"]
        data["guild"] = request.GET.get("guild", "")
        if data["guild"]:
            data["url"] += "&guild="+request.GET["guild"]
        data["url"] +="&page="
        data["url"] = data["url"].replace("&","?",1)
        data["event"] = Event.objects.get(key=data["key"])
        data["page"] = request.GET.get("page", 1)
        data["next"]            = int(data["page"]) + 1
        data["prev"]            = max(int(data["page"]) - 1, 1)
        
        results = Logbook.objects.filter(event__key=data["key"])
        if request.GET.get("guild"):
            results = results.filter(team__guild=request.GET["guild"])
        
        results = results.order_by("-id")
        results = results[(int(data["page"])-1)*results_size:int(data["page"])*results_size]
        data["results"] = results
    return render_to_response("logbook/logbook_browse.html", data)

def logbook_create(request, id):
    data = {"session":request.session}
    team = get_team(id, request.session)
    if not team:
        return redirect("/")
    data["team"] = team
    if team.user.id == request.session.get("userID") or request.session.get("admin"):
        data["yours"] = True
    else:
        return redirect("/")
    
    # Add entry
    if request.POST.get("action") == "create":
        event = Event.objects.get(pk=request.POST.get("event"))
        logbook = Logbook(team=data["team"], event=event, url=request.POST.get("url"))
        if request.POST.get("event") == "-1":
            logbook.custom_name = request.POST.get("custom_name", "Personal Story")
            logbook.custom_icon = request.POST.get("custom_icon", "-2")
            
        if request.POST.get("dungeon_map") != "":
            logbook.dungeon_map = request.POST.get("dungeon_map")
            json_resources = {}
            total = 0
            resource_ids = request.POST.getlist("resource_id")
            resource_qtys = request.POST.getlist("resource_qty")
            for x in xrange(0, len(resource_qtys)): # Sigh
                if resource_qtys[x] == "":
                    resource_qtys[x] = 0
            
            for x in xrange(0, len(resource_ids)):
                json_resources[resource_ids[x]] = int(resource_qtys[x])
                total += int(resource_qtys[x])
            json_resources = json.dumps(json_resources)
            #print json_resources
            #print total
            # Hardcoded to 3 for now
            if total > 3:
                return redirect("/error/resource-error")
            logbook.resources = json_resources
            
        
        #if event.auto_accept: # Automatic approvals
            """
            today = str(datetime.now())[:10]
            logbook.approved_on = today
            logbook.rewarded = 1
            logbook.rewarded_on = today
            handled_by = "ATLAS"
            note = ""
            
            # Merits/Strikes
            
            # Give the reward
            """
            
        
        logbook.save()
        return redirect("/logbook/view/"+str(data["team"].id)+"/")
    
    data["logbook"] = Logbook.objects.filter(team__id=id)
    events = Event.objects.exclude(id__in=data["logbook"].values_list("event__id", flat=True))
    
    data["events"] = []
    for event in events:
        if event.key == "ORIG":
            continue
        elif team.guild == "Explorers" and "E" in event.guilds:
            data["events"].append(event)
        elif team.guild == "Hunters" and "H" in event.guilds:
            data["events"].append(event)
        elif team.guild == "Researchers" and "R" in event.guilds:
            data["events"].append(event)
        #else:
        #    print "Skipping ", event.key
        
    data["icons"] = form_select_pokemon("Ditto")
    return render_to_response("logbook/logbook_create.html", data, context_instance=RequestContext(request))
    
def logbook_delete(request, id):
    data = {"session":request.session}
    delete = get_object_or_404(Logbook, pk=id)
    if delete.team.user.id == request.session.get("userID"):
        valid = True
    elif request.session.get("admin"):
        valid = True
    else:
        return redirect("/")
        
    if valid:
        delete.delete()
    return redirect("/logbook/view/"+str(delete.team.id)+"/")
    
def logbook_view(request, id):
    data = {"session":request.session}
    team = get_team(id, request.session, PUBLIC)
    if not team:
        raise Http404
    data["team"] = team
    if team.user.id == request.session.get("userID") or request.session.get("admin"):
        data["yours"] = True
    else:
        data["yours"] = False
    
    if request.POST.get("action") == "add_bookmark" and request.session.get("userID"):
        bookmark = Bookmark(team_id=team.id, user_id=request.session.get("userID"))
        bookmark.save()
    elif request.POST.get("action") == "del_bookmark" and request.session.get("userID"):
        Bookmark.objects.filter(team_id=team.id, user_id=request.session.get("userID")).delete()
    
    data["logbook"] = Logbook.objects.filter(team__id=id).order_by("order", "event")
    if data["logbook"] and request.session.get("userID"):
        data["bookmarked"] = Bookmark.objects.filter(team_id=team.id, user_id=request.session.get("userID")).count()
        
    return render_to_response("logbook/logbook_view.html", data, context_instance=RequestContext(request))   