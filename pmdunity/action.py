# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from .common import *

def ability(request, inv_id):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
        
    # Get the item
    item = get_object_or_404(Inventory, pk=inv_id)
    
    # Confirm it's yours
    if (item.team.user_id != request.session.get("userID")):
        return redirect("/")
    
    # Update ability
    if request.POST.get("action") == "ability":
        pokemon_id = request.POST.get("pokemon_id")
        ability = request.POST.get("ability")
        
        # Verify you own the pokemon
        target = get_object_or_404(Pokemon, pk=pokemon_id, team__user__id=request.session.get("userID"))
        
        try:
            target.ability = ability
            target.save()
            
            # Remove the item
            item.delete()
            log(request, "[ABILITY CHANGE] " + target.name + "("+str(target.id)+") changed abilities to - " + target.ability)
            return redirect("/team/view/"+str(target.team.id))
        except:
            log(request, "[ABILITY CHANGE] FAILURE - " + target.name + "("+str(target.id)+") DID NOT change abilities to - "+ target.ability +"\n" + str(e))
            raise Http404
    
    team_id = item.team.id
    data["item"] = item
    data["pokemon"] = Pokemon.objects.filter(team_id=team_id).order_by("name")
    return render(request, "action/ability.html", data)

def equip(request, team_id):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
        
    team = Team.objects.get(pk=team_id)
    if request.session.get("userID"):
        if team.user.id == request.session["userID"] or request.session["admin"]:
            data["yours"] = True
            
    if not data["yours"]:
        return redirect("/")
        
    # Get team
    data["pokemon"] = Pokemon.objects.filter(team_id=team_id)
    # Get inventory
    data["inventory"] = Inventory.objects.filter(team_id=team_id)
        
    return render(request, "action/equip.html", data)

def evolve(request, inv_id):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
        
    # Get the item
    item = get_object_or_404(Inventory, pk=inv_id)
    
    # Confirm it's yours
    if (item.team.user_id != request.session.get("userID")):
        return redirect("/")
    
    # Check if you're evolving
    if request.POST.get("action") == "evolve":
        # Load the pokemon
        stats = request.POST.getlist("stat")
        
        target = get_object_or_404(Pokemon, pk=request.POST.get("pokemon_id"), team__user__id=request.session.get("userID"))
        target.ability              = request.POST.get("ability")
        target.species              = request.POST.get("to_species")
        target.strength             = stats[0]
        target.intelligence         = stats[2]
        target.agility              = stats[4]
        target.charisma             = stats[6]
        target.bonus_strength       = stats[1]
        target.bonus_intelligence   = stats[3]
        target.bonus_agility        = stats[5]
        target.bonus_charisma       = stats[7]
        
        target.move1          = request.POST.get("move1", "-")
        target.move2          = request.POST.get("move2", "-")
        target.move3          = request.POST.get("move3", "-")
        target.move4          = request.POST.get("move4", "-")
        
        if target.move1 == "":
            target.move1 = "-"
        if target.move2 == "":
            target.move2 = "-"
        if target.move3 == "":
            target.move3 = "-"
        if target.move4 == "":
            target.move4 = "-"
        
        # Clean up move dashes
        if target.move1 != "-" and target.move1[0] == "-":
            target.move1 = target.move1[1:]
        if target.move2 != "-" and target.move2[0] == "-":
            target.move2 = target.move2[1:]
        if target.move3 != "-" and target.move3[0] == "-":
            target.move3 = target.move3[1:]
        if target.move4 != "-" and target.move4[0] == "-":
            target.move4 = target.move4[1:]
        
        try:
            target.full_clean(exclude=["comments"])
            target.save()
            item.delete()
            log(request, "[EVOLUTION] " + target.name + "("+str(target.id)+") evolved from " + request.POST.get("from_species") + " to " + request.POST.get("to_species"))
            return redirect("/team/view/"+str(target.team.id))
        except ValidationError as e:
            log(request, "[EVOLUTION] FAILURE - " + target.name + "("+str(target.id)+") DID NOT evolve from " + request.POST.get("from_species") + " to " + request.POST.get("to_species") + "\n" + str(e))
            raise Http404
    
    team_id = item.team.id
    team_name = item.team.name
    data["item"] = item
    data["evolutions"] = EVOLUTIONS
    data["pokemon"] = Pokemon.objects.filter(team_id=team_id, species__in=data["evolutions"].keys()).order_by("name")
    #data["names"] = POKEMON
    return render(request, "action/evolve.html", data)

def open_item(request, inv_id):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
        
    # Get the item
    item = get_object_or_404(Inventory, pk=inv_id)
    
    # Confirm it's yours
    if (item.team.user_id != request.session.get("userID")):
        return redirect("/")
    
    team_id = item.team.id
    team_name = item.team.name
    data["item"] = item
    
    # Determine possible rewards
    rewards = {
        37:[{"item":15, "qty":1}, {"item":11, "qty":2}, {"item":16, "qty":1}], 
        38:[{"item":35, "qty":1}, {"item":36, "qty":1}], 
        39:[{"item":17, "qty":1}, {"item":18, "qty":1}],
        40:[{"item":19, "qty":1}, {"item":20, "qty":1}], 
        41:[{"item":23, "qty":1}, {"item":24, "qty":1}], 
        42:[{"item":25, "qty":1}, {"item":26, "qty":1}], 
        43:[{"item":27, "qty":1}, {"item":28, "qty":1}], 
        44:[{"item":29, "qty":1}, {"item":30, "qty":1}], 
        45:[{"item":31, "qty":1}, {"item":32, "qty":1}],
        66:[{"item":62, "qty":1}, {"item":63, "qty":1}],
        65:[{"item":56, "qty":1}, {"item":54, "qty":3}, {"item":55, "qty":1}]
    }
    
    choices = rewards[item.item.id]
    del rewards
    
    if (request.POST.get("action") != "open"):
        # Parse possible rewards
        for choice in choices:
            if (choice != -1):
                choice["item"] = Item.objects.get(pk=choice["item"])
            else:
                # Handle starcoin reward here
                None
        data["choices"] = choices
        #print choices
        # Render
        return render(request, "action/open.html", data)
    else:
        try:
            choice = int(request.POST.get("choice"))
            reward = choices[choice]
            # Give the new item
            for _ in range(0, reward["qty"]):
                inv = Inventory(team_id=team_id, item_id=reward["item"])
                # Save
                inv.save()
                
            package = Inventory.objects.get(pk=inv_id)
            
            
            # Remove the old item
            package.delete()
            
            
            log(request, "[OPEN] " + team_name + " chose reward #"+str(choice)+" from their " + package.item.name)
        except:
            return redirect("/")
        return redirect("/team/inventory/"+str(team_id)+"/")
        
def recruit_teammate(request, inv_id):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
        
    # Get the item
    item = get_object_or_404(Inventory, pk=inv_id)
    
    # Confirm it's yours
    if (item.team.user_id != request.session.get("userID")):
        return redirect("/")
        
    # Confirm it's a recruitment slip
    if (item.item.id != 53):
        return redirect("/")
    
    # Confirm you have no more than 4 teammates already
    if (item.team.pkmn1_id and item.team.pkmn2_id and item.team.pkmn3_id and item.team.pkmn4_id):
        return redirect("/error/too-many-teammates")
    
    # Create a blank teammate
    team_id = item.team.id
    tomorrow = datetime.now() + timedelta(days=1)
    recruit = Pokemon(team=item.team, species=-1, lock_time=tomorrow)
    recruit.save()
    
    if not item.team.pkmn1_id:
        item.team.pkmn1 = recruit
    elif not item.team.pkmn2_id:
        item.team.pkmn2 = recruit
    elif not item.team.pkmn3_id:
        item.team.pkmn3 = recruit
    elif not item.team.pkmn4_id:
        item.team.pkmn4 = recruit
        
    # Give a voucher
    guild = item.team.guild
    if guild == "Explorers":
        item_id = 12
    elif guild == "Hunters":
        item_id = 13
    elif guild == "Researchers":
        item_id = 14
    
    voucher = Inventory(team_id=item.team_id, item_id=item_id)
    voucher.save()
        
    # Remove the item
    try:
        item.team.save()
        item.delete()
        log(request, "[NEW RECRUIT] PKMN ID: " + str(recruit.id) + " ON TEAM ID: " + str(recruit.team.id))
        return redirect("/team/"+str(recruit.team.id))
    except:
        log(request, "[NEW RECRUIT] FAILURE FOR TEAM " + str(team_id))
        raise Http404

def set_stats(request, pokemon_id):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
        
    # Get the pokemon
    target = get_object_or_404(Pokemon, pk=pokemon_id, team__user__id=request.session.get("userID"))
    
    # Check if you're evolving
    if request.POST.get("action") == "set_stats":
        # Set the pokemon info
        stats = request.POST.getlist("stat")
        
        target.strength             = stats[0]
        target.intelligence         = stats[2]
        target.agility              = stats[4]
        target.charisma             = stats[6]
        target.bonus_strength       = stats[1]
        target.bonus_intelligence   = stats[3]
        target.bonus_agility        = stats[5]
        target.bonus_charisma       = stats[7]
        
        try:
            target.full_clean(exclude=["comments", "lock_time"])
            target.save()
            log(request, "[SET_STATS] " + target.name + "("+str(target.id)+") has set their stats.")
            return redirect("/team/view/"+str(target.team.id))
        except ValidationError as e:
            print(e)
            log(request, "[SET_STATS] FAILURE - " + target.name + "("+str(target.id)+") DID NOT properly set their stats.\n" + str(e))
            raise Http404
    
    data["pokemon"] = target
    #data["names"] = POKEMON
    return render(request, "action/set_stats.html", data)
    
def tm(request):
    return HttpResponse("TM")
