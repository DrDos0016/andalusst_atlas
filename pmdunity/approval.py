# -*- coding: utf-8 -*-
from common import *

def resubmit(request):
    id = request.GET.get("id")
    try:
        approval = Approval.objects.get(pk=int(id))
        if not (request.session.get("userID") == approval.user_id or request.session.get("admin")):
            return redirect("/")
          
        if approval.type == "Customization":
            approval.approved = None
            approval.approved_on = None
            approval.handled_by = ""
            approval.user_note = ""
            approval.admin_note = ""
            location = "/team/inventory/"+str(approval.team_id)+"/"
            note = request.session.get("username") + " resubmitted approval request #"+str(approval.id)
        
        log(request, note)
        approval.save()
        return redirect(location)
    except:
        return redirect("/")
    return redirect("/")
    
def undo(request):
    id = request.GET.get("id")
    #try:
    approval = Approval.objects.get(pk=int(id))
    if not (request.session.get("userID") == approval.user_id or request.session.get("admin")):
        return redirect("/")
    
    if approval.type == "Customization":
        location = "/team/inventory/"+str(approval.team_id)+"/"
        data = json.loads(approval.data)
        
        inv_id = int(data["inventory_id"])
        
        # Strip the customization
        item = Inventory.objects.get(pk=inv_id)
        details = json.loads(item.details)
        deleted = False
        is_customized = False
        for x in reversed(range(0,len(details["history"]))):
            if details["history"][x]["action"] == "customization" and not deleted:
                print "Deleting history :O"
                del details["history"][x]
                deleted = True
            elif details["history"][x]["action"] == "customization" and deleted:
                is_customized = True
                break
                
        if not is_customized:
            details["is_customized"] = False
            
        if len(details["history"]) == 0:
            new_details = None
        else:
            new_details = json.dumps(details)
            
        item.details = new_details
        
        # Give a new voucher
        if data["payment"] == "voucher":
            voucher = Inventory(team_id=item.team.id, item_id=11)
        else: # Give coins
            refund = data["cost"]
            item.team.stars += refund
        
        # Save and return
        item.approval = None
        item.save()
        if data["payment"] == "voucher":
            voucher.save()
        else:
            item.team.save()
        
        approval.delete() # Delete approval request
        if is_customized: # Set to old approval request
            old_approval = Approval.objects.filter(type="Customization", approved=1, data__icontains=str(inv_id)).order_by("-id")[0]
            item.approval = old_approval
            item.save()
            
        
        note = request.session.get("username") + " undid approval request #"+str(id)
        log(request, note)
        return redirect(location)
            
    #except:
    #    return redirect("/")
    return redirect("/")