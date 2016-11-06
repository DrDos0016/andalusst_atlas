# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


from django.db import models
import re
import json
from datetime import datetime

class User(models.Model):
    username    = models.CharField(max_length=20, db_index=True)        # The user's DeviantArt username
    icon        = models.CharField(max_length=70, default="")           # The user's DeviantArt avatar url
    default_team= models.IntegerField(default=0)                        # Team to auto-select, 0 for none.
    results     = models.IntegerField(default=25)                       # Results per page, max 50
    # Misc
    ip          = models.GenericIPAddressField(default="")              # The IP address that last logged with this information
    admin       = models.BooleanField(default=False)                    # Is this account an admin? Yes/No
    beta        = models.BooleanField(default=False)                    # Allow beta features?
    last_login  = models.DateTimeField(auto_now=True, null=True)        # The last time this user logged in        

class Pokemon(models.Model):
    team        = models.ForeignKey("Team")                     # The teamID of the pokemon
    name        = models.CharField(max_length=80, db_index=True)# The name of the pokemon
    species     = models.IntegerField(default=0, db_index=True) # The name of the pokemon's species
    shiny       = models.BooleanField(default=False)            # Is the pokemon shiny?
    gender      = models.CharField(max_length=20)               # The pokemon's gender
    ability     = models.CharField(max_length=30)               # The pokemon's ability
    nature      = models.CharField(max_length=8)                # The pokemon's nature
    trait       = models.CharField(max_length=30)               # The pokemon's trait
    move1       = models.CharField(max_length=40, default="-")  # The name of move #1 if any
    move2       = models.CharField(max_length=40, default="-")  # The name of move #2 if any
    move3       = models.CharField(max_length=40, default="-")  # The name of move #3 if any
    move4       = models.CharField(max_length=40, default="-")  # The name of move #4 if any
    strength    = models.IntegerField(default=0)                # Strength stat
    intelligence= models.IntegerField(default=0)                # Intelligence stat
    agility     = models.IntegerField(default=0)                # Agility stat
    charisma    = models.IntegerField(default=0)                # Charisma stat
    bonus_strength = models.IntegerField(default=0)             # Bonus STR
    bonus_intelligence = models.IntegerField(default=0)         # Bonus INT
    bonus_agility = models.IntegerField(default=0)              # Bonus AGI
    bonus_charisma = models.IntegerField(default=0)             # Bonus CHR
    #equipment   = models.CharField(max_length=20, default="")   # CSV of inventory ids
    
    
    comments    = models.CharField(max_length=500)              # Any notes on the pokemon
    lock_time  = models.DateTimeField(null=True)                # When the Pokemon will no longer be editable
    
    def get_urlname(self): # This is redundant and should the templating slugify function should be used
        self.urlname     = re.sub('[^0-9a-zA-Z_]+', '-', self.name.replace(" ", "-").lower())

class Team(models.Model):
    user        = models.ForeignKey(User)                               # The user who created this team
    name        = models.CharField(max_length=80, db_index=True)        # The name of the team
    application = models.CharField(max_length=150)                      # The URL of the team's application
    alt_app     = models.URLField(default="", null=True)                # Alt app for hybrid teams
    guild       = models.CharField(max_length=12, db_index=True)        # The team's guild affilition
    joined      = models.DateTimeField()                                # The date the team joined the guild
    stars       = models.IntegerField(default=0)                        # The number of starcoins the team currently has
    merits      = models.IntegerField(default=0)                        # Team's merits
    strikes     = models.IntegerField(default=0)                        # Team's strikes
    pkmn1       = models.ForeignKey(Pokemon, related_name='poke1', null=True, on_delete=models.SET_NULL) # The pokemonID of the first team member
    pkmn2       = models.ForeignKey(Pokemon, related_name='poke2', null=True, on_delete=models.SET_NULL) # The pokemonID of the second team member
    pkmn3       = models.ForeignKey(Pokemon, related_name='poke3', null=True, on_delete=models.SET_NULL) # The pokemonID of the third team member
    pkmn4       = models.ForeignKey(Pokemon, related_name='poke4', null=True, on_delete=models.SET_NULL) # The pokemonID of the fourth team member
    lock_time   = models.DateTimeField(null=True)                       # When the Team will no longer be editable
    active      = models.BooleanField(default=True, db_index=True)      # If the team has submitted a logbook in the past 120 days    
    
    # Misc
    cameos      = models.CharField(max_length=12, default="Ask", db_index=True)    # Is this team welcome to be cameoed? No/Ask/Non-speaking/Yes
    
    def __init__(self, *args, **kwargs):
        super(Team, self).__init__(*args, **kwargs)
        guild_icons = {"Explorers":"map-pin.png", "Hunters":"sealing-wax.png", "Researchers":"flask.png"}
        self.guild_icon = guild_icons.get(self.guild, "")
    
    def get_urlname(self): # This is redundant and should the templating slugify function should be used
        self.urlname     = re.sub('[^0-9a-zA-Z_]+', '-', self.name.replace(" ", "-").lower())
    
class TeamOOC(models.Model):
    team        = models.OneToOneField("Team", primary_key=True)        # TeamID
    tumblr      = models.URLField(default="")                           # Tumblr URL for team
    type        = models.CharField(max_length=10, default="Drawn")      # Drawn, Written, or Hybrid
    
class Item(models.Model):
    name        = models.CharField(max_length=80)           # The name of the item
    cost        = models.IntegerField(default=0)            # The cost of the item. (0 is free, -1 is not for sale)
    image       = models.CharField(max_length=40)           # The image filename of the item.
    description = models.TextField()                        # An in-universe description of the item
    explanation = models.TextField()                        # An OOC explanation of how the item works
    appears     = models.DateTimeField()                    # When the item becomes available for purchase
    disappears  = models.DateTimeField(null=True)           # When the item stops being available for purchase (for special events)
    attributes  = models.TextField(null=True)

class Inventory(models.Model):
    team        = models.ForeignKey(Team)                   # The teamID that owns an item.
    item        = models.ForeignKey(Item)                   # The itemID of what the team now has.
    details     = models.TextField(null=True)
    #equipped    = models.ForeignKey("Pokemon", null=True, default=None) # This field does not want to be deleted in the database. Whatever~
    approval    = models.ForeignKey("Approval", null=True, default=None)
    
    def customize(self, url, name, desc, alterations):
        if self.details:
            details = json.loads(self.details)
        else:
            details = {"is_customized":True, "history":[]}
            
        if desc == "":
            desc = "A customized " + self.item.name
        
        details["is_customized"] = True
        details["history"].append({"action":"customization", "url":url, "name":name, "desc":desc, "time":str(datetime.now()), "alterations":alterations})
        
        self.details = json.dumps(details)
    
class Transaction(models.Model):
    team        = models.ForeignKey(Team)                   # The team that made the purchase
    change      = models.IntegerField(default=0)            # The increase/decrease in stars
    username    = models.CharField(max_length=20)           # The user that created the transaction
    description = models.TextField()                        # An explanation of the transaction
    timestamp   = models.DateTimeField(auto_now_add=True)   # When the transaction happened
    
class Log(models.Model):
    username    = models.CharField(max_length=20)           # The user that caused the event
    ip          = models.GenericIPAddressField()            # The user's IP
    timestamp   = models.DateTimeField(auto_now_add=True)   # When the event happened
    action      = models.TextField()                        # What the user did

class Event(models.Model):
    key         = models.CharField(max_length=8, unique=True) # The event key ("S1M01, S1APP", etc)
    name        = models.CharField(max_length=40)           # The name of the event "A Gigantic Problem"
    image       = models.CharField(max_length=10, default="blank.png") # Pokemon image associated w/ event
    opens       = models.DateField()                        # The date the event begins
    closes      = models.DateField(null=True)               # The date the event ends. Anything on or after this date is late.
    guilds      = models.CharField(max_length=8, default="EHR") # The guilds which can participate in the event.
    rewards     = models.TextField(default="{}")            # The rewards to be given for completing the event. JSON format to be determined later.
    #auto_accept = models.BooleanField(default=True)         # Automatically accept and reward logbooks for this event.
    order       = models.IntegerField(default=999)          # Used for ordering of events

class Logbook(models.Model):
    team        = models.ForeignKey(Team)                   # The teamID for the logbook event
    event       = models.ForeignKey(Event)                  # The event participated in
    url         = models.URLField()                         # The first page of the submission that shows completion of this event            
    custom_name = models.CharField(max_length=40, default="")        # Name for peronsal story
    custom_icon = models.IntegerField(default=0)            # Name for personal story
    approved    = models.NullBooleanField(default=None)     # Has an admin approved the submission? Yes/No/Not Yet (True/False/Null)
    approved_on = models.DateField(null=True, default=None) # The date approval was given
    rewarded    = models.BooleanField(default=False)        # Was the team given their reward yet?
    rewarded_on = models.DateField(null=True, default=None) # The date the team was rewarded
    reputation  = models.IntegerField(default=0)            # Merits/Strikes for this event
    handled_by  = models.CharField(max_length=20, null=True, default=None)# The admin account that handled this
    user_note   = models.CharField(max_length=400, default="") # A note from an admin only the user/admins can see
    admin_note  = models.CharField(max_length=400, default="") # A note from an admin only admins can see
    order       = models.IntegerField(default=1000)            # Order for custom sorting
    submitted   = models.DateField(auto_now_add=True)       # Date submitted
    dungeon_map = models.IntegerField(default=0)            # Map ID for dungeon submissions
    resources   = models.CharField(max_length=100, default="{}") # Resource:Qty collected for dungeon submissions

class Timer(models.Model):
    end_time    = models.IntegerField(default=0)            # Unix time from DA.
    what        = models.CharField(max_length=20)           # What ends

class Approval(models.Model):
    user        = models.ForeignKey(User)
    team        = models.ForeignKey(Team, null=True)        # The teamID the approval is for
    pokemon     = models.ForeignKey(Pokemon, null=True)     # The pokemon the approval is for
    type        = models.CharField(max_length=40, db_index=True)
    url         = models.URLField()
    submitted   = models.DateField(auto_now_add=True)
    approved    = models.NullBooleanField(default=None, db_index=True)     # Date of admin approval
    approved_on = models.DateField(null=True, default=None) # The date approval was given
    handled_by  = models.CharField(max_length=20, null=True, default=None)# The admin account that handled this
    user_note   = models.CharField(max_length=400, default="") # A note from an admin only the user/admins can see
    admin_note  = models.CharField(max_length=400, default="") # A note from an admin only admins can see
    data        = models.TextField(default="{}")

class Bookmark(models.Model):
    user        = models.ForeignKey(User, db_index=True)    # This user
    team        = models.ForeignKey(Team)                   # Is watching this team

class Resource(models.Model):  # This table got made early and probably needs to be dropped
    team         = models.ForeignKey(Team)               # The team that acquired the resource
    logbook      = models.ForeignKey(Logbook)            # The logbook where the resource was acquired    
    entity       = models.IntegerField()                 # The resource itself
    quantity     = models.IntegerField(default=1)        # The amount collected

class Dungeon_List(models.Model):
    key             = models.CharField(max_length=20, db_index=True)       # Dungeon identifier
    name            = models.CharField(max_length=60)       # Dungeon's Name
    tileset         = models.CharField(max_length=30)       # GFX Tileset
    floors          = models.IntegerField(default=1)        # Floors of dungeon
    public          = models.BooleanField(default=False)    # Show up on the list of dungeons
    
class Blueprint(models.Model):
    key             = models.ForeignKey("Dungeon_List", db_index=True)     # The dungeon identifier
    floor           = models.IntegerField(default=1)        # Rules are for this floor
    style           = models.CharField(max_length=20)       # Dungeon Generation Style            
    min_rooms       = models.IntegerField(default=5)        # Min. # of rooms to try to make
    max_rooms       = models.IntegerField(default=5)        # Max. # of rooms to try to make
    min_room_size   = models.IntegerField(default=5)        # Min dimensions of a room
    max_room_size   = models.IntegerField(default=5)        # Max dimensions of a room
    door_chance     = models.IntegerField(default=75)       # Chance of a door in a doorway
    min_danger_level= models.IntegerField(default=1)        # Lower limit of item/enemy pool
    max_danger_level= models.IntegerField(default=1)        # Upper limit of item/enemy pool
    trap_ratio      = models.DecimalField(max_digits=3, decimal_places=2, default=0) # Traps/room
    resource_ratio  = models.DecimalField(max_digits=3, decimal_places=2, default=0) # Resources/room
    enemy_ratio     = models.DecimalField(max_digits=3, decimal_places=2, default=0) # Enemies/room
    
class Entity(models.Model):
    type            = models.CharField(default="", max_length=10, db_index=True)   # Type of entity trap/resource/enemy/door
    tile            = models.CharField(default="", max_length=20)   # Tile to use on dungeon map
    image           = models.CharField(default="", max_length=20)   # Image to use for details
    name            = models.CharField(default="", max_length=40)   # Name of entity
    danger_level    = models.IntegerField(default=1, db_index=True) # Level where this entity may spawn
    desc            = models.CharField(default="", max_length=250)  # Description of entity
    data            = models.TextField(default="{}")                # JSON Data (if needed?)
    collectible     = models.BooleanField(default=False)            # Can this resource be taken from the dungeon?
    
class Team_Dungeon(models.Model):
    team            = models.ForeignKey(Team, db_index=True)                               # The team who has this dungeon
    key             = models.ForeignKey("Dungeon_List", db_index=True)      # The dungeon identifier
    floor           = models.IntegerField(default=1)                        # Dungeon Floor
    dive            = models.IntegerField(default=1)                        # What trip into the dungeon this is
    seed            = models.CharField(max_length=32)                       # The seed used that generated the dungeon
    data            = models.TextField(default="")                          # The actual dungeon (pickled!)
    completed       = models.BooleanField(default=False)                    # Has this dungeon's logbook been submitted and approved?
    timestamp       = models.DateTimeField(auto_now_add=True)               # When the Dungeon was saved
    
class Spotlight(models.Model):
    team            = models.ForeignKey(Team)                       # Team to be featured
    image           = models.URLField(null=True)                    # Thumbnail image to display. Pull from DA API to get the url for this.
    text            = models.TextField(null=True)                   # Text to display if the team has no drawn portion
    summary         = models.TextField()                            # The text to accompany the team
    appears         = models.DateField()                            # The date this team will be shown in the spotlight
#
# Site related Classes
#

class Customization(object):
    def __init__(self, team_id, inv_id):
        inv_id = int(inv_id)
        self.inv = Inventory.objects.get(pk=inv_id, team_id=team_id)
        self.team = Team.objects.get(pk=team_id)
        
    def can_customize(self, method, cost, voucher_id=None):
        self.method = ""
        self.can_customize = False
        self.cost = int(cost)
        if "can_customize" in self.inv.item.attributes:
            if method == "starcoins":
                self.method = "starcoins"
                self.balance = self.team.stars
                self.after = self.balance - self.cost
                self.can_customize = (self.after >= 0)
                if not self.can_customize:
                    self.error = "insufficient-funds"
                    self.msg = "You don't have enough starcoins to purchase that!"
                return self.can_customize
            elif method == "voucher" and voucher_id:
                self.method = "voucher"
                self.voucher_id = voucher_id
                self.can_customize = True
                return True
        self.error = "customization-error"
        self.msg = "Tried to customize an invalid inventory item"
        return False
        
    def customize_item(self, url, name, desc, alterations):
        if self.method == "starcoins" and self.can_customize:
            try:
                self.team.stars -= self.cost
                self.inv.customize(url, name, desc, alterations)
                self.inv.save()
                self.team.save()
                return True
            except:
                self.error = "customization-error"
                self.msg = "Couldn't save customization properly!"
                return False
        elif self.method == "voucher" and self.can_customize:
            try:
                self.inv.customize(url, name, desc, alterations)
                self.inv.save()
                v = Inventory.objects.get(pk=self.voucher_id)
                v.delete()
                return True
            except:
                self.error = "customization-error"
                self.msg = "Couldn't save customization properly!"
                return False

class Sale(object):
    def __init__(self, id, type="item"):
        if type == "item":
            id = int(id)
            self.item = Item.objects.get(pk=id, cost__gte=0)
            self.cost = self.item.cost
            
    def can_afford(self, team_id):
        self.team = Team.objects.get(pk=team_id)
        
        # Starcoins
        self.balance = self.team.stars
        self.after = self.balance - self.cost
        self.can_afford = (self.after >= 0)
        
        # Vouchers
        vouchers = Inventory.objects.filter(team_id=self.team.id, item__name__icontains="Voucher")
        seen_vouchers = []
        valid_vouchers = []
        self.valid_voucher_ids = []
        for v in vouchers:
            if v.item.id in seen_vouchers:
                continue
            seen_vouchers.append(v.item.id)
            attr = json.loads(v.item.attributes)
            if attr.get("valid_items") and (self.item.id in attr["valid_items"]):
                valid_vouchers.append(v)
                self.valid_voucher_ids.append(v.id)
        if len(valid_vouchers) >= 1:
            self.can_vouch = True
            valid_vouchers.sort()
            self.valid_vouchers = valid_vouchers
        else:
            self.can_vouch = False
            self.valid_vouchers = None
        
    def purchase(self, method, voucher_id=None):
        if method == "starcoins" and self.can_afford:
            
            # Reduce starcoins
            self.team.stars -= self.cost
            
            # Give Item
            try:
                purchase = Inventory(team_id=self.team.id, item_id=self.item.id)
                purchase.save()
                self.team.save()
            except:
                self.error = "purchase-error"
                self.msg = "A purchase error (with starcoins) occurred!"
                return False
                
            self.msg = "Purchased " + self.item.name + " for " + str(self.item.cost)
            return True
        elif method == "voucher" and self.can_vouch and voucher_id:
            voucher_id = int(voucher_id)
            
            # Remove voucher
            if voucher_id in self.valid_voucher_ids:
                for v in self.valid_vouchers:
                    if voucher_id == v.id:
                        v.delete()
            else:
                self.error = "purchase-error"
                self.msg = "Invalid voucher ID: "+ str(voucher_id) + " to purchase " + self.item.name
                return False
                
            # Give Item
            try:
                purchase = Inventory(team_id=self.team.id, item_id=self.item.id)
                purchase.save()
                self.team.save()
            except:
                self.error = "purchase-error"
                self.msg = "A purchase error (with starcoins) occurred!"
                return False
            
            self.msg = "Purchased " + self.item.name + "w/ a voucher: "  + v.item.name
            return True
        else:
            self.error = "purchase-error"
            self.msg = "Unknown payment type: " + str(method)
        return False
