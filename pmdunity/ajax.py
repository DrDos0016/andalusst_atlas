# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


from .common import *
from django.views.decorators.csrf import csrf_exempt
from cgi import escape

# Incomplete
def get_item(request):
    if not request.POST.get("inventory_id"):
        return HttpResponse("{}")
    inv = Inventory.objects.get(pk=request.POST.get("inventory_id"))
    
    output = {
        "inventory_id": inv.id,
        "item_id": inv.item.id,
        "team_id": inv.team.id,
        "details": inv.details,
        "item_name": inv.item.name,
        "item_image": inv.item.image,
        "item_desc": inv.item.description,
        "item_exp": inv.item.explanation,
        "item_attr": inv.item.attributes
    }
    
    output = json.dumps(output)
    
    return HttpResponse(output)

def get_resources(request, map_id):
    output = {"success":False, "entities":[], "owner_id":-1, "owner":""}
    try:
        dungeon_storage = Team_Dungeon.objects.get(pk=map_id)
        dungeon = cPickle.loads(str(dungeon_storage.data))
        entities = Entity.objects.filter(pk__in=dungeon.entity_ids)
        for entity in entities:
            if entity.type == "resource" and entity.collectible:
                output["entities"].append({"id":entity.id, "name":entity.name})
        output["success"] = True
        output["owner_id"] = dungeon_storage.team.id
        output["owner"] = dungeon_storage.team.name
    except:
        None
    output = json.dumps(output)
    return HttpResponse(output)


def get_species(request, species_id):
    pokemon = Pokemon.objects.filter(species=species_id)
    output = []
    for pkmn in pokemon:
        output.append({"name":escape(pkmn.name), "shiny":pkmn.shiny, "gender":escape(pkmn.gender), "team_id":pkmn.team.id, "team_name":escape(pkmn.team.name), "guild":pkmn.team.guild})
        
    output = json.dumps(output)
    return HttpResponse(output)

def get_team_map(request, team_id, key_id):
    output = {"success":False}
    try:
        # Find the dungeon list ID of the dungeon with the provided key:
        temp = Dungeon_List.objects.get(key=key_id).id
        # Find the dungeon id
        team_dungeon = Team_Dungeon.objects.get(team_id=team_id, key_id=temp, floor=1)
        output["key"] = team_dungeon.id
        output["success"] = True
    except:
        None
    output = json.dumps(output)
    return HttpResponse(output)

def submit_approval(request):
    data = json.loads(request.POST["data"])
    today = str(datetime.now())[:10]
    #{"entry":"14","key":"S1M01","status":"1","reward":"full","u_note":"N/A","s_note":"N/A","size":"2"}

    if not request.session.get("admin"):
        return HttpResponse("FAILURE")
    
    try:
        # Get the approval entry
        approval = Approval.objects.get(pk=int(data["entry"]))
        approval_statuses = {"approved":1, "rejected":0, "undecided":None}
        approval.approved = approval_statuses[data["status"]]
        if data["status"] == "approved":
            approval.approved_on = today
            approval.handled_by = request.session.get("username")
        elif data["status"] == "undecided":
            approval.approved_on = None
            approval.handled_by = None
        elif data["status"] == "rejected":
            approval.approved_on = None
            approval.handled_by = request.session.get("username")
        approval.user_note = data["u_note"]
        approval.admin_note = data["s_note"]
        approval.save()
        note = "Set status for "+approval.type+" approval #"+str(approval.id) + " to " + data["status"] + ". By " + request.session.get("username")
        ret = "SUCCESS"
    except:
        note = "Approval Submission Failure!\nData: " + request.POST["data"]
        ret = "FAILURE"
        
    log(request, note)
    return HttpResponse(ret)

@csrf_exempt
def validate_logbook(request):
    """
        This requires a regular reward set to be chosen to be able to get a bonus reward!
        Let's hope this doesn't change.
    """
    data = json.loads(request.POST["data"])
    today = str(datetime.now())[:10]
    #{"entry":"14","key":"S1M01","status":"1","reward":"full","u_note":"N/A","s_note":"N/A","size":"2"}                                                                                                                                                        :"N/A","size":"2"}
    #print request.POST["data"]
    if not request.session.get("admin"):
        return HttpResponse("FAILURE")
    
    note = ""
    try:
        logbook = Logbook.objects.get(pk=int(data["entry"]))
        
        logbook.approved = int(data["status"])
        logbook.approved_on = today
        logbook.handled_by = request.session.get("username")
        ret = "SUCCESS"
        
        # Rewarding
        if logbook.approved == 1:
            note += "["+data["key"]+"] - APPROVED team #"+str(logbook.team.id) + " ("+logbook.team.name+").\n"
            if data["reputation"] != 0:
                logbook.reputation = data["reputation"]
                note += "Reputation change: " + str(data["reputation"])
                logbook.team.merits += abs((data["reputation"] > 0) * data["reputation"])
                logbook.team.strikes += abs((data["reputation"] < 0) * data["reputation"])
                logbook.team.save()
            logbook.rewarded = 1
            logbook.rewarded_on = today
            
            if data["reward"] == "None": # Nothing to do
                note += "No reward given."
            else:
                event = Event.objects.get(key=data["key"])
                all_rewards = json.loads(event.rewards)
                possible_rewards = all_rewards[logbook.team.guild]
                reward_set = None
                for rewards in possible_rewards:
                    if rewards.get("name") == data["reward"]:
                        reward_set = rewards["contents"]
                        break
                if not reward_set:
                    print("Reward set: " + data.get("reward") + " not found!")
                    ret = "FAILURE"
                else:
                    note += "Giving reward set: " + data.get("reward") + "\n"
                    
                    # Give the reward
                    for prize in reward_set:
                        if prize["item"] == -1:
                            logbook.team.stars += prize["quantity"]
                            logbook.team.save()
                            note += str(prize["quantity"]) + " star coins, "
                        else:
                            for _ in range(0,prize["quantity"]):
                                if not prize.get("per"):
                                    inv = Inventory(team_id=logbook.team.id, item_id=prize["item"])
                                    note += inv.item.name + ", "
                                    inv.save()
                                elif prize.get("per") == "member":
                                    for x in range(0, int(data["size"])):
                                        inv = Inventory(team_id=logbook.team.id, item_id=prize["item"])
                                        note += inv.item.name + ", "
                                        inv.save()
                    note += "\n"
                
                    # Give the BONUS if applicable
                    if data["bonus"] == 1 and len(all_rewards.get("Bonus", [])) != 0:
                        note += "Giving Bonus rewards:\n"
                        reward_set = all_rewards["Bonus"][0]["contents"]
                        for prize in reward_set:
                            if prize["item"] == -1:
                                logbook.team.stars += prize["quantity"]
                                logbook.team.save()
                                note += str(prize["quantity"]) + " star coins, "
                            else:
                                for _ in range(0,prize["quantity"]):
                                    if not prize.get("per"):
                                        inv = Inventory(team_id=logbook.team.id, item_id=prize["item"])
                                        note += inv.item.name + ", "
                                        inv.save()
                                    elif prize.get("per") == "member":
                                        for x in range(0, int(data["size"])):
                                            inv = Inventory(team_id=logbook.team.id, item_id=prize["item"])
                                            note += inv.item.name + ", "
                                            inv.save()
                        note += "\n"
        else:
            logbook.user_note = data["u_note"]
            logbook.admin_note = data["s_note"]
            note += "["+data["key"]+"] - REJECTED team #"+str(logbook.team.id) + " ("+logbook.team.name+").\n"
            
            
        # Resource collection
        collected = []
        if logbook.approved and logbook.resources != "" and logbook.resources != "{}":
            resources = json.loads(logbook.resources)
            res_note = "[RESOURCE] - Team #"+str(logbook.team.id) + " collected:\n"
            for resource in resources:
                res = Resource(team=logbook.team, logbook=logbook, entity=int(resource), quantity=int(resources[resource]))
                res_note += str(resources[resource]) + " of resource # " + resource + "\n"
                collected.append(res)
            
            
        log(request, note)
        logbook.save()
        log(request, res_note)
        for res in collected:
            res.save()
    except:
        log(request, "VERIFICATION ERROR\n" + note)
        ret = "FAILURE"
    return HttpResponse(ret)
