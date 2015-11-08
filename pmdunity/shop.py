# -*- coding: utf-8 -*-
from common import *

def buy(request, item_id):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/")
    if not request.session.get("teamID"):
        return redirect("/team/manage")
    
    if request.session.get("teamID"):
        info = get_starcoins(request.session["teamID"])
        if info:
            request.session["team_stars"] = info["starcoins"]
            request.session["merits"] = info["merits"]
            request.session["strikes"] = info["strikes"]
    log_post(request)
    
    # Store info
    data["store"] = "Wear and Flair Accessories"
    
    # Set up the potential sale
    sale = Sale(item_id)
    sale.can_afford(request.session["teamID"])
    sale.purchase(request.POST.get("payment"))
    
    # Template variables related to sale
    data["item"] = sale.item
    data["after"] = sale.after
    data["can_vouch"] = sale.can_vouch
    data["can_cash"] = sale.can_afford
    data["vouchers"] = sale.valid_vouchers
    
    # Are you trying to buy it right now?
    payment = None
    if request.POST.get("starcoins"):
        payment = "starcoins"
    elif request.POST.get("voucher"):
        payment = "voucher"
    if payment:
        success = sale.purchase(payment, request.POST.get("voucher_id"))
        if success:
            log(request, sale.msg)
            transaction(sale.team.id, -1 * sale.item.cost, request.session["username"], sale.msg)
            return redirect("/shop?purchase="+str(sale.item.id))
        else:
            log(request, sale.msg)
            return redirect("/error/"+sale.error)   
    return render_to_response("shop/buy.html", data, context_instance=RequestContext(request))

def customization(request, store_id="wear_and_flair"):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
    if not request.session.get("teamID"):
        return redirect("/team/manage")
    if request.session.get("teamID"):
        info = get_starcoins(request.session["teamID"])
        if info:
            request.session["team_stars"] = info["starcoins"]
            request.session["merits"] = info["merits"]
            request.session["strikes"] = info["strikes"]
    
    # Get item list that can be customized
    data["inventory"] = get_inventory(request.session.get("teamID"), "can_customize")
    
    # Figure out if you have a valid voucher
    voucher = Inventory.objects.filter(team_id=request.session.get("teamID"), item__name="Accesory Customization Voucher")
    if len(voucher) > 0:
        data["can_vouch"] = True
        data["voucher_id"] = voucher[0].id
    else:
        data["can_vouch"] = False
        data["voucher_id"] = 0
    
    # Are you trying to customize an item right now?
    if request.POST.get("action") == "customization" and request.POST.get("payment"):
        payment = request.POST["payment"]
        cost = int(request.POST.get("cost"))
        custom = Customization(request.session.get("teamID"), request.POST["item"])
        if custom.can_customize(payment, cost, data["voucher_id"]):
            success = custom.customize_item(request.POST["customization_url"], request.POST["name"], request.POST["desc"], int(request.POST["alterations"]))
            if success:
                # Add the approval request
                data = json.dumps({"inventory_id":custom.inv.id, "cost":cost, "payment":request.POST["payment"]})
                approval = Approval(user_id=request.session.get("userID"), team_id=request.session.get("teamID"), type="Customization", url=request.POST["customization_url"], data=data)
                approval.save()
                custom.inv.approval = approval
                custom.inv.save()
                
                msg = "Purchased accessory customization ["+request.POST["customization_url"]+"] for " + str(cost) + " via " + payment
                log(request, msg)
                transaction(custom.team.id, -1 * cost, request.session["username"], msg)
                return redirect("/shop?purchase=customization")
            else:
                log(request, custom.msg)
                return redirect("/error/"+custom.error)
        else:
            log(request, custom.msg)
            return redirect("/error/"+custom.error)
            

    
    return render_to_response("shop/customization.html", data, context_instance=RequestContext(request))

def shop(request, store_id="wear_and_flair"):
    data = {"session":request.session}
    if not request.session.get("userID"):
        #print "No userID for shop"
        return redirect("/login")
    if not request.session.get("teamID"):
        #print "No teamID for shop"
        return redirect("/team/manage")
    if request.session.get("teamID"):
        info = get_starcoins(request.session["teamID"])
        if info:
            request.session["team_stars"] = info["starcoins"]
            request.session["merits"] = info["merits"]
            request.session["strikes"] = info["strikes"]
    
    # Get items for sale
    now = str(datetime.now())
    store = Item.objects.filter(cost__gte=0, appears__range=["2014-01-01", now]).order_by("name")
    data["store"] = store
    
    # Get purchase message
    if request.GET.get("purchase"):
        data["purchase"] = request.GET["purchase"]
    # Pre select item
    if request.GET.get("select"):
        data["select"] = request.GET["select"]
    
    return render_to_response("shop/shop.html", data)