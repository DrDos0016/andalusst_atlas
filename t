diff --git a/pmdu/urls.py b/pmdu/urls.py
index a895095..aa6be75 100755
--- a/pmdu/urls.py
+++ b/pmdu/urls.py
@@ -63,6 +63,7 @@ urlpatterns = patterns('',
     url(r'^ability/(?P<inv_id>[0-9]+)$', 'pmdunity.views.ability'),
     url(r'^evolve/(?P<inv_id>[0-9]+)$', 'pmdunity.views.evolve'),
     url(r'^open/(?P<inv_id>[0-9]+)$', 'pmdunity.views.open_item'),
+    url(r'^recruit/(?P<inv_id>[0-9]+)$', 'pmdunity.views.recruit_teammate'),
     url(r'^set_stats/(?P<pokemon_id>[0-9]+)/(.*)$', 'pmdunity.views.set_stats'),
     url(r'^tm/(?P<inv_id>[0-9]+)$', 'pmdunity.views.tm'),
     
diff --git a/pmdunity/action.py b/pmdunity/action.py
index fa60742..7d844c6 100755
--- a/pmdunity/action.py
+++ b/pmdunity/action.py
@@ -198,6 +198,51 @@ def open_item(request, inv_id):
             return redirect("/")
         return redirect("/team/inventory/"+str(team_id)+"/")
         
+def recruit_teammate(request, inv_id):
+    data = {"session":request.session}
+    if not request.session.get("userID"):
+        return redirect("/login")
+        
+    # Get the item
+    item = get_object_or_404(Inventory, pk=inv_id)
+    
+    # Confirm it's yours
+    if (item.team.user_id != request.session.get("userID")):
+        return redirect("/")
+        
+    # Confirm it's a recruitment slip
+    if (item.item.id != 53):
+        return redirect("/")
+    
+    # Confirm you have no more than 4 teammates already
+    if (item.team.pkmn1_id and item.team.pkmn2_id and item.team.pkmn3_id and item.team.pkmn4_id):
+        return redirect("/error/too-many-teammates")
+    
+    # Create a blank teammate
+    team_id = item.team.id
+    tomorrow = datetime.now() + timedelta(days=1)
+    recruit = Pokemon(team=item.team, species=-1, lock_time=tomorrow)
+    recruit.save()
+    
+    if not item.team.pkmn1_id:
+        item.team.pkmn1 = recruit
+    elif not item.team.pkmn2_id:
+        item.team.pkmn2 = recruit
+    elif not item.team.pkmn3_id:
+        item.team.pkmn3 = recruit
+    elif not item.team.pkmn4_id:
+        item.team.pkmn4 = recruit
+        
+    # Remove the item
+    try:
+        item.team.save()
+        item.delete()
+        log(request, "[NEW RECRUIT] PKMN ID: " + str(recruit.id) + " ON TEAM ID: " + str(recruit.team.id))
+        return redirect("/team/"+str(recruit.team.id))
+    except:
+        log(request, "[NEW RECRUIT] FAILURE FOR TEAM " + str(team_id))
+        raise Http404
+
 def set_stats(request, pokemon_id):
     data = {"session":request.session}
     if not request.session.get("userID"):
diff --git a/pmdunity/views.py b/pmdunity/views.py
index 8c5be1a..2d055e4 100755
--- a/pmdunity/views.py
+++ b/pmdunity/views.py
@@ -55,7 +55,8 @@ def error(request, type="Unknown"):
     "insufficient-funds":"You can't afford that!",
     "team-create":"Could not create team!<br>Make sure you are using a <b>fav.me</b> link for you team's application. This is required to submit a team.",
     "oauth-error":"Failed to retrieve data from DeviantArt! You may be unable to login until DA fixes the issue.",
-    "resource-error":"You provided invalid values for dungeon resources! The total must be no more than 3 per floor of the dungeon"
+    "resource-error":"You provided invalid values for dungeon resources! The total must be no more than 3 per floor of the dungeon",
+    "too-many-teammates":"Your team already has four members!"
     }
 
     data = {"session":request.session}
diff --git a/templates/team/team_inventory.html b/templates/team/team_inventory.html
index eaaff46..934be41 100755
--- a/templates/team/team_inventory.html
+++ b/templates/team/team_inventory.html
@@ -133,10 +133,8 @@ $(document).ready(function (){
                 var type = $("#type-"+id).val();
                 if (type == 15)
                     $("#action").html("<h3>Action:</h3><a href='/evolve/"+$("#id-"+id).val()+"' class='bigbutton'>Evolve Teammate</a>");
-                else if (type == 47)
-                    $("#action").html("<h3>Action:</h3><a href='/ability/"+$("#id-"+id).val()+"' class='bigbutton'>Change Ability</a>");
-                else if (type == 48 || type == 49)
-                    $("#action").html("<h3>Action:</h3><a href='/tm/"+$("#id-"+id).val()+"' class='bigbutton'>Change Moveset</a>");
+                else if (type == 53)
+                    $("#action").html("<h3>Action:</h3><a href='/recruit/"+$("#id-"+id).val()+"' class='bigbutton'>Recruit Teammate</a>");
             }
         }
         
