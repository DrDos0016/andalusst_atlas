# -*- coding: utf-8 -*-
from common import *
from pmdunity.admin import *
from pmdunity.shop import *
from pmdunity.logbook import *
from pmdunity.approval import *
from pmdunity.action import *
from pmdunity.stats import *
from pmdunity.dungeon import *

def account_manage(request):
    if not request.session.get("userID"):
        return redirect("/login")
    data = {"session":request.session}
    
    data["user"] = User.objects.get(pk=request.session["userID"])
    data["teams"] = Team.objects.filter(user=data["user"]).order_by("name")
    
    # Save changes
    if request.POST.get("action") == "save":
        # Default Team
        team_id = int(request.POST.get("default_team"))
        for team in data["teams"]:
            if team.id == team_id:
                data["user"].default_team = team_id
                break
                
        # Results
        request.session["results"] = min(int(request.POST.get("results", 25)), 50)
        data["session"] = request.session
        data["user"].results = request.session["results"]
        
        data["user"].save()
        data["msg"] = "Settings applied!"
    
    return render_to_response("account_manage.html", data, context_instance=RequestContext(request))

def contributors(request):
    data = {"session":request.session}
    data["users"] = User.objects.all().order_by("username")
    data["count"] = len(data["users"])
    return render_to_response("misc/contributors.html", data)

def credits(request):
    data = {"session":request.session}
    return render_to_response("misc/credits.html", data)

def error(request, type="Unknown"):
    errors = {"purchase-error":"Something went wrong when attempting to purchase an item.",
    "invalid-team":"Team not found!",
    "team-full":"Your team appears to be full already!",
    "invalid-pokemon":"Pokémon not found!",
    "team-edit":"Could not edit team!",
    "customization-error":"You can't customize that!",
    "insufficient-funds":"You can't afford that!",
    "team-create":"Could not create team!<br>Make sure you are using a <b>fav.me</b> link for you team's application. This is required to submit a team.",
    "oauth-error":"Failed to retrieve data from DeviantArt! You may be unable to login until DA fixes the issue.",
    "resource-error":"You provided invalid values for dungeon resources! The total must be no more than 3 per floor of the dungeon",
    "too-many-teammates":"Your team already has four members!"
    }

    data = {"session":request.session}
    data["error"] = type.replace("-", " ")
    data["error_message"] = errors.get(type, "An unknown error occurred!")
    return render_to_response("error/error.html", data)

def error500(request):
    return render_to_response("500.html")

def generic(request, template):
    data = {"session":request.session}
    return render_to_response(template, data)

def index(request):
    if request.session.get("teamID"):
        info = get_starcoins(request.session["teamID"])
        if info:
            request.session["team_stars"] = info["starcoins"]
            request.session["merits"] = info["merits"]
            request.session["strikes"] = info["strikes"]
    data = {"session":request.session}
    
    # Load data for frontpage modules
    
    return render_to_response("index.html", data) 

def login(request):
    if request.GET.get("error") == "access_denied":
        return render_to_response("misc/deny_auth.html")

    uri = LOGIN_REDIRECT
    if not request.GET.get("code"):
        return redirect("https://www.deviantart.com/oauth2/draft15/authorize?response_type=code&client_id="+CLIENT_ID+"&redirect_uri="+uri)
    
    code = request.GET["code"]
    try:
        url = "https://www.deviantart.com/oauth2/draft15/token?client_id="+CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&grant_type=authorization_code&code="+request.GET["code"]+"&redirect_uri="+uri
        if ENV == "DEV" or True:
            # Standard
            response = urllib2.urlopen(url)
            data = json.load(response)
            #print data
            token = data["access_token"]
            response = urllib2.urlopen("https://www.deviantart.com/api/v1/oauth2/user/whoami?access_token="+token)
            data = json.load(response)
        else: # This is thankfully deprecated, but I'll let it linger for a bit.
            # Ext script
            os.system("/usr/local/bin/python2.7.10 /var/projects/pmdu.org/pmdunity/login.py " + request.META.get("REMOTE_ADDR").replace(".", "") + " \"" + url + "\"")
            # Read file
            file_data = open("/var/projects/pmdu.org/assets/data/logins/"+request.META.get("REMOTE_ADDR").replace(".", "")+".json").read()
            data = json.loads(file_data)
            if data:
                os.remove("/var/projects/pmdu.org/assets/data/logins/"+request.META.get("REMOTE_ADDR").replace(".", "")+".json")
            print data
        
        username = data["username"]
        if data.get("usericonurl"):
            icon = data["usericonurl"]
        elif data.get("usericon"):
            icon = data["usericon"]
        else:
            icon = ""

        # Get / Add user
        user, created = User.objects.get_or_create(username=username)
        user.ip = request.META["REMOTE_ADDR"]
        user.icon = icon
        if username in ADMINS:
            user.admin = 1
        user.save()
        
        request.session["userID"] = user.id
        request.session["admin"] = user.admin
        request.session["beta"] = user.beta
        request.session["username"] = user.username
        request.session["icon"] = user.icon
        request.session["teamID"] = 0
        request.session["team_owner"] = ""
        request.session["team_name"] = ""
        request.session["team_stars"] = 0
        request.session["merits"] = 0
        request.session["strikes"] = 0
        request.session["team_pkmn1"] = ""
        request.session["team_pkmn2"] = ""
        request.session["team_pkmn3"] = ""
        request.session["team_pkmn4"] = ""
        request.session.set_expiry(0)
        
        # Default team
        if user.default_team != 0:
            if Team.objects.filter(pk=user.default_team).count():
                return redirect("/team/set/"+str(user.default_team))
        
        #if created:
        #    return render_to_response("misc/new_user_guide.html")
        #else:
        return redirect("/team/manage")
    except:
        return redirect("/error/oauth-error")

def logout(request):
    request.session["userID"] = ""
    request.session["admin"] = 0
    request.session["username"] = ""
    request.session["icon"] = ""
    
    if request.session.get("teamID"):
        clear_session(request)
    return redirect("/")
    
def misc(request):
    data = {"session":request.session}
    return render_to_response("misc/misc.html", data)

def pokemon_delete(request):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")

    active = delete_pokemon(request.GET.get("pokemon_id"), request.session)
    if active:
        return redirect("/team/set/"+str(active))
    return redirect("/team/manage?success=1")

def search(request):
    data = {"session":request.session}
    results_size = request.session.get("results", RESULTS)
    
    # Form Settings
    data["name"]            = request.GET.get("name", "")
    data["da_name"]         = request.GET.get("da_name", "")
    data["pokemon_select"]  = form_select_pokemon(request.GET.get("pokemon", 0))
    data["pokemon"]         = request.GET.get("pokemon")
    data["related"]         = request.GET.get("related")
    data["cameos"]          = request.GET.get("cameos")
    data["tumblr"]          = request.GET.get("tumblr")
    data["min"]             = request.GET.get("min", "1")
    data["max"]             = request.GET.get("max", "4")
    data["guild"]           = request.GET.get("guild")
    data["type"]            = request.GET.get("type", "")
    data["active"]          = request.GET.get("active")
    data["sort"]            = request.GET.get("sort", "newest")
    data["page"]            = request.GET.get("page", "1")
    data["next"]            = int(data["page"]) + 1
    data["prev"]            = max(int(data["page"]) - 1, 1)
    data["counts"]          = Team.objects.values('guild').annotate(guild_count=Count('guild')).order_by("guild")
    data["total"]           = Team.objects.count()
    
    if data["pokemon"] == "Any":
        data["pokemon"] = ""
    
    # Results
    results = Team.objects.all()
    if len(request.GET) == 0:
        results = results.filter(pkmn1__isnull=False).order_by("-id")
    else:
        if data["name"]:
            results = results.filter(name__icontains=data["name"])
        if data["da_name"]:
            results = results.filter(user__username__icontains=data["da_name"])
        if data["pokemon"] and not data["related"]:
            results = results.filter(pokemon__species=int(data["pokemon"]))
        elif data["pokemon"] and data["related"]:
            origin = int(data["pokemon"])
            chain = PKMN_TO_CHAIN[origin]
            related = CHAIN_TO_PKMN[chain]
            results = results.filter(pokemon__species__in=related)
        if data["cameos"]:
            results = results.filter(cameos=data["cameos"])
        if data["tumblr"] == "y":
            results = results.filter(teamooc__tumblr__gt="")
        elif data["tumblr"] == "n":
            results = results.filter(Q(teamooc__tumblr="") | Q(teamooc__tumblr__isnull=True))
        if data["min"] == "2":
            results = results.filter(pkmn2__isnull=False)
        elif data["min"] == "3":
            results = results.filter(pkmn3__isnull=False)
        elif data["min"] == "4":
            results = results.filter(pkmn4__isnull=False)
        if data["max"] == "1":
            results = results.filter(pkmn2__isnull=True)
        elif data["max"] == "2":
            results = results.filter(pkmn3__isnull=True)
        elif data["max"] == "3":
            results = results.filter(pkmn4__isnull=True)
        
        if data["guild"]:
            results = results.filter(guild=data["guild"])
        if data["type"] != "":
            results = results.filter(teamooc__type=data["type"])
        if data["active"]:
            print "Filtering by active"
            results = results.filter(active=True)
        if data["sort"] == "newest":
            results = results.order_by("-id")
        elif data["sort"] == "name":
            results = results.order_by("name")
        elif data["sort"] == "owner":
            results = results.order_by("user__username", "name")
        elif data["sort"] == "random":
            results = results.order_by("?")
            data["page"] = 1
            data["next"] = 1
            data["prev"] = 1
    
    results = results.distinct()[(int(data["page"])-1)*results_size:int(data["page"])*results_size]
    
    for result in results:
        result.get_urlname()
        
    data["results"] = results
    
    # ?name=a&da_name=s&pokemon=491&cameos=Non-speaking&min=1&max=4&guild=Explorers&sort=name&page=1
    data["url"] = "?"
    data["url"] += "name="+data["name"]+"&" if data["name"] else ""
    data["url"] += "da_name="+data["da_name"]+"&" if data["da_name"] else ""
    data["url"] += "pokemon="+data["pokemon"]+"&" if data["pokemon"] else ""
    data["url"] += "type="+data["type"]+"&" if data["type"] else ""
    data["url"] += "active="+data["active"]+"&" if data["active"] else ""
    data["url"] += "cameos="+data["cameos"]+"&" if data["cameos"] else ""
    data["url"] += "tumblr="+data["tumblr"]+"&" if data["tumblr"] else ""
    data["url"] += "min="+data["min"]+"&" if data["min"] else ""
    data["url"] += "max="+data["max"]+"&" if data["max"] else ""
    data["url"] += "guild="+data["guild"]+"&" if data["guild"] else ""
    data["url"] += "sort="+data["sort"]+"&" if data["sort"] else ""
    data["url"] += "page="
    return render_to_response("search.html", data)

def stats(request):
    data = {"session":request.session}
    
    species = Pokemon.objects.values('species').annotate(species_count=Count('species')).order_by("-species_count", "species")
    data["species"] = []
    for s in species:
        data["species"].append({"name":NUMBERS[s["species"]], "count":s["species_count"], "dex":s["species"]})
        
    data["species"] = sorted(data["species"], key=lambda k: (-1 * k["count"], k["name"].lower()))
    return render_to_response("stats/pokemon_population.html", data)

def storehouse(request):
    data = {"session":request.session}
    data["food"] = 0
    data["spool"] = 0
    
    if request.GET.get("mode") == "tentative":
        data["verified"] = False
        resources = Logbook.objects.filter(event_id=19)
        for resource in resources:
            try:
                r = json.loads(resource.resources)
                for key in r.keys():
                    if key in ["8", "16"]:
                        data["food"] += r[key]
                    elif key == "7":
                        data["spool"] += r[key]
            except:
                continue
    else:
        data["verified"] = True
        resources = Resource.objects.all()
        for resource in resources:
            if resource.entity in [8,16]:
                data["food"] += resource.quantity
            elif resource.entity == 7:
                data["spool"] += resource.quantity
    return render_to_response("misc/storehouse.html", data)

def team(request, team_id=0, read_only=False):
    if not request.session.get("userID") and not read_only:
        return redirect("/login")
    data = {"session":request.session}
    data["now"] = datetime.now()
    data["natures"] = NATURES
    data["traits"] = TRAITS
    data["years"] = range(2013, int(data["now"].year)+1)
    
    lock_temp = datetime.now() + timedelta(days=1)
    action = request.POST.get("action")
    
    # POST
    if action == "create" or action == "edit":
        #print request.POST
        valid_team = True
        valid_pokemon = True
        has_ooc = False
        
        # Load Team
        if team_id == 0:
            team = Team(lock_time=lock_temp)
            team.user_id        = request.session.get("userID")
        else:
            team = get_object_or_404(Team, pk=team_id)
        
        if (team.lock_time and team.lock_time > data["now"]):
            #print "Unlocked team"
            team.application    = request.POST.get("app")
            team.alt_app        = request.POST.get("alt_app", "")
            team.name           = request.POST.get("team_name", "").strip()
            team.guild          = request.POST.get("guild", "Explorers")
            team.joined         = request.POST.get("year") + "-" + request.POST.get("month") + "-" + request.POST.get("day")
            team.cameos         = request.POST.get("cameos", "Ask")
            team.lock_time      = lock_temp
            team.pkmn1          = None
            team.pkmn2          = None
            team.pkmn3          = None
            team.pkmn4          = None
            try:
                team.full_clean(exclude=["alt_app", "pkmn1", "pkmn2", "pkmn3", "pkmn4"])
            except ValidationError as e:
                print "============== TEAM ERRORS"
                print e
                valid_team = False
                
        else: # Only non-lockable fields
            if request.POST.get("alt_app"):
                team.alt_app = request.POST.get("alt_app")
            team.cameos         = request.POST.get("cameos", "Ask")    
            
        # Create Team OOC
        if team_id == 0:
            ooc = TeamOOC()
        else:
            ooc = TeamOOC.objects.get_or_create(team_id=team_id)[0]
        has_ooc = True
        ooc.tumblr  = request.POST.get("tumblr", "")
        ooc.type    = request.POST.get("type")
        try:
            ooc.full_clean(exclude=["team", "tumblr"])
        except ValidationError as e:
            print "============== TEAM OOC ERRORS"
            print e
            valid_team = False
            
        # Load Pokemon
        all_pokemon = []
        for i in xrange(0, len(request.POST.getlist("species"))):
            poke = Pokemon.objects.filter(pk=request.POST.getlist("pokemon_id", [])[i])
            if len(poke) == 1:
                poke = poke[0]
            else:
                poke = Pokemon(species=0, lock_time=lock_temp)
            if request.POST.getlist("species")[i] == "0":
                continue
            
            if (poke.lock_time and poke.lock_time > data["now"]):
                poke.name           = request.POST.getlist("pokemon_name")[i].strip()
                poke.species        = request.POST.getlist("species")[i]
                poke.shiny          = request.POST.getlist("shiny")[i]
                poke.gender         = request.POST.getlist("gender")[i]
                poke.ability        = request.POST.getlist("ability")[i]
                poke.nature         = request.POST.getlist("nature")[i]
                poke.trait          = request.POST.getlist("trait")[i]
                poke.move1          = request.POST.getlist("move1")[i]
                poke.move2          = request.POST.getlist("move2")[i]
                poke.move3          = request.POST.getlist("move3")[i]
                poke.move4          = request.POST.getlist("move4")[i]
                poke.lock_time      = lock_temp
                
                # Stats
                stats = request.POST.getlist("stat")
                poke.strength           = stats[0+(i*8)]
                poke.intelligence       = stats[2+(i*8)]
                poke.agility            = stats[4+(i*8)]
                poke.charisma           = stats[6+(i*8)]
                poke.bonus_strength     = stats[1+(i*8)]
                poke.bonus_intelligence = stats[3+(i*8)]
                poke.bonus_agility      = stats[5+(i*8)]
                poke.bonus_charisma     = stats[7+(i*8)]
            else: # Only non-lockable fields
                poke.name           = request.POST.getlist("pokemon_name")[i].strip()
                poke.gender         = request.POST.getlist("gender")[i]
                poke.nature         = request.POST.getlist("nature")[i]
                poke.trait          = request.POST.getlist("trait")[i]
                """
                if request.POST.getlist("move1")[i] != "N/A":
                    poke.move1          = request.POST.getlist("move1")[i]
                if request.POST.getlist("move2")[i] != "N/A":
                    poke.move2          = request.POST.getlist("move2")[i]
                if request.POST.getlist("move3")[i] != "N/A":
                    poke.move3          = request.POST.getlist("move3")[i]
                if request.POST.getlist("move4")[i] != "N/A":
                    poke.move4          = request.POST.getlist("move4")[i]
                """
            
            """
            # Clean up move dashes
            if poke.move1 != "-" and poke.move1[0] == "-":
                poke.move1 = poke.move1[1:]
            if poke.move2 != "-" and poke.move2[0] == "-":
                poke.move2 = poke.move2[1:]
            if poke.move3 != "-" and poke.move3[0] == "-":
                poke.move3 = poke.move3[1:]
            if poke.move4 != "-" and poke.move4[0] == "-":
                poke.move4 = poke.move4[1:]
            """
            
            if poke.gender == "":
                poke.gender = "Not specified"
            
            try:
                poke.full_clean(exclude=["comments", "team"])
                all_pokemon.append(poke)
            except ValidationError as e:
                print "============== POKEMON "+str(i)+" ERRORS"
                print e
                valid_pokemon = False
            
        # Save
        if valid_team and valid_pokemon and len(all_pokemon) > 0:
            team.save()
            team.pkmn1 = None
            team.pkmn2 = None
            team.pkmn3 = None
            team.pkmn4 = None
            if has_ooc:
                ooc.team = team
                ooc.save()
            for poke in all_pokemon:
                poke.team = team
                poke.save()
                
                if team.pkmn1 == None or team.pkmn1.id == poke.id:  
                    team.pkmn1 = poke
                elif team.pkmn2 == None or team.pkmn2.id == poke.id:
                    team.pkmn2 = poke
                elif team.pkmn3 == None or team.pkmn3.id == poke.id:
                    team.pkmn3 = poke
                elif team.pkmn4 == None or team.pkmn4.id == poke.id:
                    team.pkmn4 = poke
            if all_pokemon:
                team.save()
            #print "SAVED ALL"
            
            # Submit app to logbook
            if action == "create":
                logbook = Logbook(team=team, event=Event.objects.get(pk=1), url=team.application)
                logbook.save()
            
            if team.id == request.session.get("teamID"):
                return redirect("/team/set/"+str(team.id))
            return redirect("/team/manage?success=1")
    
    if action == "lock_edit" and request.session.get("admin"):
        times = request.POST.getlist("lock_time")
        pk_ids = request.POST.getlist("pokemon_id")
        team = Team.objects.get(pk=team_id)
        team.lock_time = times[0]
        team.save()
        times = times[1:]
        x = 0
        for pk_id in pk_ids:
            poke = Pokemon.objects.get(pk=pk_id)
            poke.lock_time = times[x]
            poke.save()
            x += 1
        data["lock_msg"] = " - Updated!"
        
    
    # Set up forms
    if (team_id):
        data["action"] = "edit"
        data["team"] = get_object_or_404(Team, pk=team_id)
        data["year"] = str(data["team"].joined)[:4]
        data["month"] = str(data["team"].joined)[5:7]
        data["day"] = str(data["team"].joined)[8:10]
        data["pokemon"] = Pokemon.objects.filter(team_id=team_id)
        
        for poke in data["pokemon"]:
            poke.species_name = NUMBERS[poke.species]
            poke.select_list = form_select_pokemon(NUMBERS[poke.species], "pmdu_starters")
            if poke.species not in PMDU_STARTERS:
                poke.evolved = poke.species
            else:
                poke.evolved = False
        
        if not read_only and (data["team"].user_id == request.session.get("userID") or request.session.get("admin")):
            data["yours"] = True
        else:
            data["yours"] = False
            
        if (data["team"].user_id == request.session.get("userID") or request.session.get("admin")):
            data["extra_nav"] = True
        else:
            data["extra_nav"] = False
        
        if data["yours"] and len(data["pokemon"]) <= 1: # Add a second slot for solo-teams
            data["pokemon"] = data["pokemon"][:20]
            temp_poke = Pokemon(species=0, lock_time=lock_temp)
            temp_poke.select_list = form_select_pokemon("", "pmdu_starters")
            data["pokemon"].append(temp_poke)
            if len(data["pokemon"]) == 1: # Repeat for empty teams
                data["pokemon"].append(temp_poke)
    
        
    else:
        data["action"] = "create"
        data["team"] = Team(guild="Explorers", lock_time=lock_temp)
        temp_poke = Pokemon(species=0, lock_time=lock_temp)
        temp_poke.select_list = form_select_pokemon("", "pmdu_starters")
        data["pokemon"] = [temp_poke, temp_poke]
        data["yours"] = True
    
    return render_to_response("team/team.html", data, context_instance=RequestContext(request))

def team_actions(request, team_id):
    if not request.session.get("userID"):
        return redirect("/login")
    
    data = {"session":request.session}    
    team = get_object_or_404(Team, pk=team_id)
    if team.user_id == request.session.get("userID") or request.session.get("admin"):
        data["yours"] = True
    else:
        return redirect("/")
        
    data["actions"] = {}
    
    # Check if you have Pokemon with unset stats
    no_stats = Pokemon.objects.filter(team_id=team.id, strength=0, intelligence=0, agility=0, charisma=0, bonus_strength=0, bonus_intelligence=0, bonus_agility=0, bonus_charisma=0).order_by("name")
    if no_stats:
        data["actions"]["set_stats"] = True
        data["no_stats"] = no_stats
    
    data["team"] = team
    data["pokemon"] = Pokemon.objects.filter(team_id=team.id)
    
    return render_to_response("team/team_actions.html", data)

def team_delete(request):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
        
    #team = get_object_or_404(Team, pk=)
    delete_team(int(request.GET.get("team_id")), request.session)
    if int(request.session["teamID"]) == int(request.GET.get("team_id")):
        clear_session(request)
    return redirect("/team/manage?success=1")

def team_inventory(request, id):
    data = {"session":request.session}
    team = get_team(id, request.session, PUBLIC)
    data["team"] = team
    data["yours"] = False
    if request.session.get("userID"):
        if team.user.id == request.session["userID"] or request.session["admin"]:
            data["yours"] = True
    
    if request.session.get("admin") and request.POST.get("admin-del"):
        Inventory.objects.filter(pk=request.POST.get("admin-del")).delete()
    
    data["inventory"] = Inventory.objects.filter(team_id=team).order_by("item__name")
    data["blank"] = range(0, INV_PAGE - len(data["inventory"]))
    return render_to_response("team/team_inventory.html", data, context_instance=RequestContext(request))

def team_manage(request):
    if not request.session.get("userID"):
        return redirect("/login")
    if request.session.get("teamID"):
        info = get_starcoins(request.session["teamID"])
        if info:
            request.session["team_stars"] = info["starcoins"]
            request.session["merits"] = info["merits"]
            request.session["strikes"] = info["strikes"]
    data = {"session":request.session}
    if request.GET.get("success"):
        data["success"] = "Your changes have been made."
    
    teams = Team.objects.filter(user_id=request.session.get("userID")).order_by("name")
    for team in teams:
        team.get_urlname()
        if team.pkmn1:
            team.pkmn1.get_urlname()
        if team.pkmn2:
            team.pkmn2.get_urlname()
        if team.pkmn3:
            team.pkmn3.get_urlname()
        if team.pkmn4:
            team.pkmn4.get_urlname()
    data["teams"] = teams
    
    return render_to_response("team/team_manage.html", data)
    
def team_set(request, id):
    if not request.session.get("userID"):
        return redirect("/login")
        
    # Get team
    team = Team.objects.filter(pk=id)
    if len(team) != 1:
        return redirect("/error/team-not-found")
    team = team[0]
    
    request.session["teamID"] = team.id
    request.session["team_guild"] = team.guild
    request.session["team_owner"] = team.user.id
    request.session["team_name"] = team.name
    request.session["team_stars"] = team.stars
    request.session["merits"] = team.merits
    request.session["strikes"] = team.strikes
    request.session["team_pkmn1"] = "blank"
    request.session["team_pkmn2"] = "blank"
    request.session["team_pkmn3"] = "blank"
    request.session["team_pkmn4"] = "blank"
    if team.pkmn1:
        request.session["team_pkmn1"] = team.pkmn1.species
    if team.pkmn2:
        request.session["team_pkmn2"] = team.pkmn2.species
    if team.pkmn3:
        request.session["team_pkmn3"] = team.pkmn3.species
    if team.pkmn4:
        request.session["team_pkmn4"] = team.pkmn4.species
    
    return redirect("/team/manage")
    
def team_view(request, id):
    data = {"session":request.session}
    team = get_team(id, request.session, True)
    if not team:
        return redirect("/error/invalid-team")
    team.get_urlname()
    data["team"] = team
    data["pokemon"] = []
    if request.session.get("teamID"):
        info = get_starcoins(request.session["teamID"])
        if info:
            request.session["team_stars"] = info["starcoins"]
            request.session["merits"] = info["merits"]
            request.session["strikes"] = info["strikes"]
    
    if team.pkmn1:
        team.pkmn1.get_urlname()
        team.pkmn1.species_name = NUMBERS[team.pkmn1.species]
        data["pokemon"].append(team.pkmn1)
    if team.pkmn2:
        team.pkmn2.get_urlname()
        team.pkmn2.species_name = NUMBERS[team.pkmn2.species]
        data["pokemon"].append(team.pkmn2)
    if team.pkmn3:
        team.pkmn3.get_urlname()
        team.pkmn3.species_name = NUMBERS[team.pkmn3.species]
        data["pokemon"].append(team.pkmn3)
    if team.pkmn4:
        team.pkmn4.get_urlname()
        team.pkmn4.species_name = NUMBERS[team.pkmn4.species]
        data["pokemon"].append(team.pkmn4)
    
    return render_to_response("team/team_view.html", data)

def test(request):
    data = {"session":request.session, "version":VERSION}
    now = str(datetime.now())[:10]

    # Latest Logbooks
    l1 = Logbook.objects.exclude(event__id=1).filter(team__guild="Explorers").order_by("-id")[0]
    l2 = Logbook.objects.exclude(event__id=1).filter(team__guild="Hunters").order_by("-id")[0]
    l3 = Logbook.objects.exclude(event__id=1).filter(team__guild="Researchers").order_by("-id")[0]
    data["latest"] = [l1,l2,l3]
    
    # Recently Joined
    r1 = Logbook.objects.filter(event__id=1, team__guild="Explorers").order_by("-id")[0]
    r2 = Logbook.objects.filter(event__id=1, team__guild="Hunters").order_by("-id")[0]
    r3 = Logbook.objects.filter(event__id=1, team__guild="Researchers").order_by("-id")[0]
    data["recruits"] = [r1,r2,r3]
    
    # Spotlight
    spotlight = Spotlight.objects.filter(appears__lte=now).order_by("-id")
    if len(spotlight):
        data["spotlight"] = spotlight[0]
        
        # Logbooks
        data["submissions"] = Logbook.objects.filter(team_id=data["spotlight"].team_id).order_by("order")
        
        # Other Teams
        data["other_teams"] = Team.objects.filter(user=data["spotlight"].team.user).exclude(id=data["spotlight"].team_id).order_by("guild", "name")
    
    return render_to_response("test.html", data)