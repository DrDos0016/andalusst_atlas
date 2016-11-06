# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


from .common import *

def admin(request):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    return render(request, "admin/admin.html", data)

def account_transfer(request):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    
    if request.POST.get("action") == "transfer":
        old_name = request.POST.get("from")
        new_name = request.POST.get("to")
        
        success = False
        data["result"] = "An error occurred! Check the new name doesn't have any teams"
        # Confirm the old name exists
        try:
            user_info = User.objects.get(username=old_name)
            success = True
        except:
            data["result"] = "Original DA name not found! " + old_name
            
        if success:
            # Delete the new name if there is one
            User.objects.filter(username=new_name).delete()
            user_info.username = new_name
            user_info.save()
            data["result"] = "Changes saved!"
            
            
    return render(request, "admin/account_transfer.html", data)

def add_event(request):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    
    data["pokemon_list"] = form_select_pokemon("", "all")
    data["reward_size"] = range(0, REWARD_ITEMS)
    data["items"] = Item.objects.all().order_by("name")
    
    if request.POST.get("name"):
        # Add event
        #try:
        event = Event(key=request.POST.get("key"), name=request.POST.get("name"), image=request.POST.get("image")+".png", opens=request.POST.get("opens"), closes=request.POST.get("closes"))
        guilds = "".join(request.POST.getlist("guild", []))
        event.guilds = guilds
        
        if request.POST.get("reward_template") == "basic_errand":
            event.rewards = '{"Explorers":[{"name":"1 Starcoin","contents":[{"item":-1,"quantity":1}]}],"Hunters":[{"name":"1 Starcoin","contents":[{"item":-1,"quantity":1}]}],"Researchers":[{"name":"1 Starcoin","contents":[{"item":-1,"quantity":1}]}],"Bonus":[]}'
        elif request.POST.get("reward_template") == "custom":
            event.rewards = request.POST.get("custom_reward")
        else:
            event.rewards = ""
        
        event.save()
        data["msg"] = "Event added successfully!"
        #except:
            #data["msg"] = "An error occurred! Event not added!"
    
    return render(request, "admin/add_event.html", data)
    
def approvals(request):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    
    status = request.GET.get("status", "undecided")
    data["status"] = status
    status_nums = {"approved":1, "rejected":0, "undecided":None}
    approvals = Approval.objects.filter(type=request.GET.get("type", "Customization")).filter(approved=status_nums[status]).order_by("team__guild", "team__name")
    data["approvals"] = approvals
    types = Approval.objects.values("type").distinct()
    data["types"] = types
    data["type"] = request.GET.get("type", "Customization")

    return render(request, "admin/approvals.html", data)
    
def dungeons(request):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    
    return render(request, "admin/dungeons/dungeons.html", data)

def dungeon_design(request):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    
    saved = False
    if request.POST.get("action") == "save_dungeon":
        if request.POST.get("id") == "0":
            dungeon = Dungeon_List()
        else:
            dungeon = Dungeon_List.objects.get(pk=request.GET["dungeon"])
            
        dungeon.name = request.POST.get("name")
        dungeon.key = request.POST.get("key")
        dungeon.tileset = request.POST.get("tileset")
        dungeon.floors = request.POST.get("floors")
        dungeon.public = request.POST.get("public", False)
        
        try:
            dungeon.full_clean()
            dungeon.save()
            data["msg"] = "Saved Dungeon!"
            saved = True
        except ValidationError as e:
            data["msg"] = "Entity failure!<br>" + str(e)
       
    if request.POST.get("action") == "save_floor":
        # If the blueprint already exists load it
        if request.POST.get("id"):
            id = int(request.POST["id"])
        else:
            id = -9999
        blueprint = Blueprint.objects.filter(id=id)
        if len(blueprint) == 1:
            blueprint = blueprint[0]
        else:
            blueprint = Blueprint()
            blueprint.floor = request.POST.get("floor")
            blueprint.key = Dungeon_List.objects.get(pk=request.GET["dungeon"])
            
        blueprint.style             = request.POST.get("style")
        blueprint.min_rooms         = request.POST.get("min_rooms")
        blueprint.max_rooms         = request.POST.get("max_rooms")
        blueprint.min_room_size     = request.POST.get("min_room_size")
        blueprint.max_room_size     = request.POST.get("max_room_size")
        blueprint.door_chance       = request.POST.get("door_percent")
        blueprint.min_danger_level  = request.POST.get("min_danger_level")
        blueprint.max_danger_level  = request.POST.get("max_danger_level")
        blueprint.trap_ratio        = request.POST.get("trap_ratio")
        blueprint.resource_ratio    = request.POST.get("resource_ratio")
        blueprint.enemy_ratio       = request.POST.get("enemy_ratio")
        
        try:
            blueprint.full_clean()
            blueprint.save()
            data["msg2"] = "Saved Blueprint F"+str(blueprint.floor)+"!"
        except ValidationError as e:
            data["msg2"] = "Blueprint failure!<br>" + str(e)
 
    data["tilesets"] = glob(os.path.join(SITE_ROOT, "assets", "images", "dungeons", "*"))
    data["dungeons"] = Dungeon_List.objects.all()
    data["blueprints"] = []
    #entities = Entities.objects.all().order_by("")
    
    if saved:
        data["wip"] = dungeon
        data["floors"] = dungeon.floors
        # Add floor blueprints
        data["blueprints"] = list(Blueprint.objects.filter(key_id=dungeon.id))
        while len(data["blueprints"]) != data["wip"].floors:
            data["blueprints"].append(Blueprint(floor=len(data["blueprints"])+1))
    elif int(request.GET.get("dungeon", -1)) >= 0 and request.GET.get("dungeon", -1) != -1:
        data["wip"] = Dungeon_List.objects.get(pk=request.GET["dungeon"])
        # Add floor blueprints
        data["blueprints"] = list(Blueprint.objects.filter(key_id=request.GET["dungeon"]))
        while len(data["blueprints"]) != data["wip"].floors:
            data["blueprints"].append(Blueprint(floor=len(data["blueprints"])+1))
    
    
    return render(request, "admin/dungeons/design.html", data)

def dungeon_entity(request):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    
    if request.POST.get("action") == "save":
        if request.POST.get("id") == "0":
            entity = Entity()
        else:
            entity = Entity.objects.get(pk=request.GET["entity"])
            
        entity.type = request.POST.get("type")
        entity.tile = request.POST.get("tile")
        entity.image = request.POST.get("image")
        entity.name = request.POST.get("name")
        entity.danger_level = request.POST.get("danger_level")
        entity.desc = request.POST.get("desc")
        entity.collectible = int(request.POST.get("collectible", 0))
        
        try:
            entity.full_clean()
            entity.save()
            data["msg"] = "Saved Entity!"
        except ValidationError as e:
            data["msg"] = "Entity failure!<br>" + str(e)
    
    data["entities"] = Entity.objects.all().order_by("type","name")
    if request.GET.get("entity") and request.GET.get("entity") != "0":
        data["wip"] = Entity.objects.get(pk=request.GET["entity"])
    
    return render(request, "admin/dungeons/entity.html", data)
    
def manage_items(request, item_id=None):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    
    if request.POST.get("name"):
        item = Item()
        item.name = request.POST.get("name", "No Name")
        item.cost = int(request.POST.get("cost", -1))
        
        if request.FILES.get("file"):
            with open(os.path.join(SITE_ROOT, "assets", "images", "items", request.FILES["file"].name), 'wb+') as destination:
                for chunk in request.FILES["file"].chunks():
                    destination.write(chunk)
                item.image = request.FILES["file"].name
        else:
            item.image = request.POST.get("image", "")
        
        item.description = request.POST.get("desc", "-").replace("\n", "<br>")
        item.explanation = request.POST.get("exp", "-").replace("\n", "<br>")
        item.appears = request.POST.get("appears")
        item.disappears = request.POST.get("disappears")
        if item.appears == "":
            item.appears = "2050-12-31"
        if item.disappears == "":
            item.disappears = None
        if request.POST.get("id"):
            item.id = int(request.POST.get("id"))
            
        # Attributes
        attributes = []
        for attrib in request.POST.getlist("attribute"):
            attributes.append({attrib:True})
        item.attributes = json.dumps(attributes, sort_keys=True)
        
        item.save()
        item_id = None
    
    if item_id == "-1":
        data["mode"] = "new"
    elif item_id == None:
            data["mode"] = "list"
            items = Item.objects.all().order_by("name")
            data["items"] = items
    else:
        data["mode"] = "edit"
        item = Item.objects.get(pk=int(item_id))
        data["id"] = item.id
        data["name"] = item.name
        data["cost"] = item.cost
        data["image"] = item.image
        data["image_full"] = os.path.join(SITE_ROOT, "assets", "images", "items", item.image)
        data["desc"] = item.description.replace("<br>", "\n")
        data["exp"] = item.explanation.replace("<br>", "\n")
        data["appears"] = item.appears
        data["disappears"] = item.disappears
        
    data["images"] = glob(os.path.join(SITE_ROOT, "assets", "images", "items", "*"))
    data["images"].sort()
    
    data["appears"] = str(datetime.now())
    
    return render(request, "admin/manage_items.html", data)

def manage_inventory(request, team_id=None):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    return render(request, "admin/manage_inventory.html", data)

def manage_merits_strikes(request):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    data["message"] = ""
    if not request.GET.get("team_id"):
        offset = int(request.GET.get("offset", 0))
        data["offset"] = offset
        data["prev"] = max(offset-100, 0)
        data["next"] = offset + 100
        teams = Team.objects.all().order_by("name")[offset:100+offset]
        data["teams"] = teams
    else:
        data["team"] = Team.objects.get(pk=int(request.GET.get("team_id")))
        
    if request.POST.get("action") == "edit":
        merits = request.POST.get("merits", 0)
        strikes = request.POST.get("strikes", 0)
        data["team"].merits = merits
        data["team"].strikes = strikes
        data["team"].save()
        log(request, "Manually adjusted Merits/Strikes for: ("+request.GET.get("team_id")+") " + data["team"].name + " (M:"+str(merits)+" S:"+str(strikes)+")")
        data["message"] = "Merits/Strikes have been adjusted successfully"
    
    return render(request, "admin/manage_merits_strikes.html", data)

def manage_star_coins(request, team=None):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    data["message"] = ""
    data["team"] = team
    
    if not data["team"]:
        offset = int(request.GET.get("offset", 0))
        data["offset"] = offset
        data["prev"] = max(offset-100, 0)
        data["next"] = offset + 100
        teams = Team.objects.all().order_by("name")[offset:100+offset]
        data["teams"] = teams
    else:
        data["team"] = Team.objects.filter(pk=team)[0]
        
    if request.POST.get("action") == "edit":
        coins = request.POST.get("starcoins", 0)
        # Update team coins
        data["team"].stars = coins
        data["team"].save()
        transaction(data["team"].id, -1, request.session["username"], "Manually set Starcoins to "+coins+" (from "+request.POST.get("original_starcoins", "unknown")+")")
        log(request, "Manually adjusted Starcoins for: ("+unicode(data["team"].id)+") " + data["team"].name)
        data["message"] = "Starcoins have been adjusted successfully"

    return render(request, "admin/manage_star_coins.html", data)

def powerless(request):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    request.session["admin"] = False
    return redirect("/")
    
def reward_teams(request):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    page = int(request.GET.get("page", 1))
    data["prev_page"] = max(page, 1)
    data["next_page"] = page + 1
    data["message"] = ""
    
    if request.POST.get("action") == "reward_teams":
    
        teams = map(int, request.POST.getlist("teams"))
        team_objs = Team.objects.filter(id__in=teams)
        for key in request.POST.keys():
            if key == "item-0" and request.POST.get("item-0") != "": # Give Starcoins 
                team_objs.update(stars=F('stars')+request.POST.get("item-0"))
                for team in teams:
                    transaction(team, int(request.POST.get("item-0")), request.session["username"], "Given as a reward.")
            elif key.startswith("item-") and request.POST.get(key) != "" : # Give Items
                item_id = int(key.replace("item-", ""))
                objs = []
                for team in team_objs:
                    for x in range(0,int(request.POST.get(key))):
                        objs.append(Inventory(item_id=item_id, team=team))
                Inventory.objects.bulk_create(objs)
        log(request)
        data["message"] = "Items have been given successfully."
    
    teams = Team.objects.all().order_by("name")[(page-1)*100:page*100]
    items = Item.objects.all().order_by("name")
    
    data["teams"] = teams
    data["items"] = items
    if request.POST.get("log"):
        data["log"] = "Gave" + request.POST["log"][4:]
    return render(request, "admin/reward_teams.html", data)
    
def site_log(request):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    offset = int(request.GET.get("offset", 0))
    
    data["next"] = offset + 30
    data["username"] = request.GET.get("username", "")
    data["action"] = request.GET.get("action", "")
    data["ip"] = request.GET.get("ip", "")
    data["time"] = request.GET.get("time", "")
    
    site_log = Log.objects.all().order_by("-id")
    if data["username"]:
        site_log = site_log.filter(username__icontains=data["username"])
    if data["ip"]:
        site_log = site_log.filter(ip=data["ip"])
    if data["action"]:
        site_log = site_log.filter(action__icontains=data["action"])
    if data["time"]:
        site_log = site_log.filter(timestamp__range=[data["time"], "2025-12-31"])
    
    site_log = site_log[offset:30+offset]
    data["logs"] = site_log
    return render(request, "admin/site_log.html", data)

def timeline(request):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    
    data["event"] = request.GET.get("event")
    
    if data["event"] == None:
        events = glob(os.path.join(SITE_ROOT, "assets", "data", "timeline", "*.json"))
        sorted(events)
        data["events"] = []
        for e in events:
            key = os.path.basename(e)[:-5]
            data["events"].append({"key":key, "name":EVENTS[key]})
        return render(request, "admin/timeline.html", data)

    # Load the submission data
    data["info"] = json.loads(open(os.path.join(SITE_ROOT, "assets", "data", "timeline", data["event"]+".json")).read())
    
    # Get the existing accounts for those who contributed
    users = User.objects.all().order_by("username")
    data["usernames"] = []
    for user in users:
        data["usernames"].append(user.username)
        
    # Get the teams for those who contributed
    teams = Team.objects.all().order_by("user__username")
    #for row in data["info"]:

    return render(request, "admin/timeline.html", data)

def transaction_log(request):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    offset = int(request.GET.get("offset", 0))
    
    data["next"] = offset + 30
    data["name"] = request.GET.get("name", "")
    data["performer"] = request.GET.get("performer", "")
    data["desc"] = request.GET.get("desc", "")
    data["time"] = request.GET.get("time", ""   )
    
    t_log = Transaction.objects.all().order_by("-id")
    if data["name"]:
        t_log = t_log.filter(team__name__icontains=data["name"])
    if data["performer"]:
        t_log = t_log.filter(username=data["performer"])
    if data["desc"]:
        t_log = t_log.filter(description__icontains=data["desc"])
    if data["time"]:
        t_log = t_log.filter(timestamp__range=[data["time"], "2025-12-31"])
    
    t_log = t_log[offset:30+offset]
    data["transactions"] = t_log
    return render(request, "admin/transaction_log.html", data)

def verify_logbooks(request):
    data = {"session":request.session}
    is_admin(request.session.get("admin"))
    
    logbooks = Logbook.objects.filter(event__key=request.GET.get("key", "APP")).filter(approved__isnull=True).order_by("team__guild", "id")
    data["logbooks"] = logbooks
    events = Event.objects.filter(id__gte=1)
    if request.GET.get("key", "APP") != "APP":
        data["valid_apps"] = Logbook.objects.values_list("team_id", flat=True).filter(event__key="APP").filter(approved=True)
    data["events"] = events
    data["event"] = events.filter(key=request.GET.get("key", "APP"))[0]

    return render(request, "admin/verify_logbooks.html", data)
