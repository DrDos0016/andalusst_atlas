# -*- coding: utf-8 -*-
from common import *
from datetime import datetime

ROOT = SITE_ROOT

# Tile ID
VOID        = -1
WALL        = 0
FLOOR       = 1
ENTRANCE    = 2
EXIT        = 3
STAIRS_UP   = 4
STAIRS_DOWN = 5

# Description List
DESCRIPTIONS = [
    "Wow! The ceiling in this room is dizzyingly high. There seems to be something up there, though...",
    "The room smells like fresh roses! But from what?",
    "For some reason, the floor is wet in this room. How odd.",
    "The room is pitch black. One could hardly see their feet. Hopefully there's something around that can help...",
    "This room is sweltering hot! What could be causing this heat?",
    "The ceiling in this room is really low at points. So much for headroom! ",
    "Laughter can be heard echoing throughout the room. Where is it coming from?",
    "Looking to the far side of the room, something could be seen in the shadows...",
    "There is an eerie silence in this room. It's quiet. TOO quiet...",
    "Examining the walls, there seem to be a strange set of disturbances embedded in them. Just what are they? ",
    "There seem to be shards of some material all over the floor in this room. Huh.",
    "In the middle of the room stands a strange obelisk. What could it be?",
    "Neat (Neat!) There seems to be an echo in this room (echo in this room).",
    "There seems to be an alarmingly loud commotion in this room. This deserves some attention!",
    "Ack! A brilliant light flashes from somewhere in the room. Where did THAT come from?",
    "You can hear music playing in the wind. How pleasant! But who, or what, is playing?",
    "The only thing extraordinary about this room is just how ordinary it is. Look over there! Wait, no, it's still ordinary.",
    "The delectable aroma of food wafts gently throughout this room. Maybe ONE bite wouldn't hurt...",
    "It seems like someone has shed quite a bit in this room. Here's to hoping they're still not around...",
    "While it doesn't appear so at first glance, it seems like someone has made a makeshift shelter in this room. But where is its resident?",
    "There is a small stream running through this room.",
    "Most of this room appears to be underwater, with dry patches scattered about. Get set to get wet!",
    "Thick, strong vines have taken residence all over this room. Where is this overgrown undergrowth coming from?",
    "For whatever reason, there are somewhat deep trenches dug out in the formation of a maze into the floor in this room. They're shallow enough to climb out of with some effort, if need be.",
    "A rusted, old piece of machinery lies discarded on the floor. Its design is very primitive, but some parts still are capable of motion.",
    "There are large, sudden, and steep shifts of elevation all throughout the room. Navigation may prove difficult.",
    "Everything in this room, for whatever reason, seems to be slightly tilted; even the floor and ceiling!",
    "A peculiar, but very deliberate, pattern is inscribed onto the floor all over this room. Is this natural?",
    "The floor dips down in a slope towards the center, giving the floor a bowl-like shape. Hopefully it's safe...",
    "Large chunks of the floor are missing from this room. They appear to have been dug out by some force...",
    "Scattered around this room are several posts brandishing some sort of banner or flag. They seem to be freshly planted.",
    "A powerful, sustained gust of wind blows through the room. Is there any way to overcome it?",
    "This room is almost completely vertical; its exit is several stories above the floor. Maybe there's something in the dungeon to assist in scaling this height...",
    "Is that another you?... No, this room just happens to be perfectly reflective!",
    "A chill wind whips past you in this room. Just where is this breeze coming from?",
    "A small red glow catches your eye in the corner of this dark room, what is its source?",
    "A soft, inaudible whisper comes from your left. Was it just you, or is there something in the room with you?",
    "Small beams of sunlight come from tiny holes in the roof of this room, it's nice to see natural light again.",
    "Water cascades down from one of the walls in this room to a small pond, it's got a refreshing feel to it!",
    "The walls of this room are shiny and freezing... ice?",
    "This room is filled with snow, enough to make a snowmon!",
    "This room is overgrown with flowers! Though you need to keep moving, this room would make for a very pretty painting.",
    "The air hangs heavy in this room, you almost begin to feel tired from it.",
    "Large, wooden planks are placed in a winding path atop pillar in this room. You can't see where the drop ends if you fell off of them, tread lightly...",
    "A shadow flies overhead and disappears behind a corner! Should you follow it or not?",
    "You hear laughter coming from behind you, it sounds distant. Should you quicken your pace or hide to see who's there?",
    "A constant stream of bubbles pop on the surface in the small pond in this room, how odd...",
    "Broken twigs and stones litter this room. What happened here?",
    "The room begins to rumble and shake, an earthquake!?",
    "Are you seeing things or is a shadow coming out of the wall over there!?",
    "You spot cut rope and bits of cloth in this room, were other adventurers here recently?",
    "You spot a small wooden chest in the corner. Treasure!?",
    "Why do the walls in this room feel fuzzy?",
    "The floor seems to have been splattered with a mix of color!",
    "Large chains rest in the corner of this room, how odd...",
    "There's something white sticking out of the ground...",
    "A shiver travels down your spine as you enter the room. Ominous...",
    "Something's hanging from the ceiling.",
    "This room smells rancid... Do you dare investigate?",
    "There are strange marks on the floor here. What could have made them?",
    "You see something move out of the corner of your eye. What was that?",
    "It's so cold in here, you can see your breath. What could be the source of the chill?",
    "The floor here feels oddly abrasive.",
    "Small scraps of material are strewn across the floor here.",
    "You hear a strange scraping sound in the distance...",
    "You feel a strange presence nearby...",
    "The floor here is quite smooth.",
    "This room has an old, musty sort of smell.",
    "The walls in this room are green. What could have caused this?",
    "You see a flicker of light from the far end of the room. What could it be?",
    "The room appears to get darker as you move further in...",
    "You feel a strange jerk as you enter this room. Your imagination, or something more sinister...?",
    "The faint echo of strange chanting resonates through this room...",
    "The scent of wet earth hangs in the air.",
    "Something shiny is poking up out of the ground here. Could it be... treasure?",
    "Thorny plants appear to have taken over this room. Don't get poked!",
    "The ground here is warm, almost uncomfortably so. The heat appears to be coming from beneath...",
    "Ancient stalagmites and stalactites create a mazelike path through this room.",
    "A strange crash is heard from above. Hopefully the ceiling won't give way to something unpleasant...",
    "There's a strange pressure in the air here. It makes it difficult to breathe.",
    "There's a rudimentary weapon stuck in the ground in the middle of the room. What could have happened here?",
    "Sound seems amplified in this room. Better keep your voice down.",
    "A thick cloud of some sort has filled this room. Hope it's not toxic...",
    "This room has signs of a battle...",
    "Part of this room contains a few healthy-looking plants. Someone's garden?",
    "There's an odd rock formation here.",
    "There's some kind of strange goo bubbling in the corner.",
    "A wild howl echoes in the distance...",
    "This room is covered in scorch marks.",
    "The floor here is covered in a thick layer of mud.",
    "The walls are covered in strange scratches. Could they mean something?",
    "Aww, how nice! There's a rainbow in this room!",
    "Walking in here kicks up a lot of dust.",
    "You feel inexplicably happy as you enter this room.",
    "Small crystals are dotted along the walls here.",
    "There's some sort of dais here. Could it be important? WHAT'S A DAIS",
    "Some sections of the walls in this room are jutting out a bit. Perhaps they could be climbed?",
    "Shards of wood litter the floor here.",
    "The floor is littered with footprints. Has someone already come and gone?",
    "Entering this room gives you an inexplicable sense of unease...",
    "There appears to be some sort of mirage in this room.",
    "This room is full of sand.",
    "This room is... a room. What did you expect?",
    "A small river runs upwards along a groove in the wall of this room, defying gravity.",
    "Beautiful crystals decorate the walls of this room, emitting a soothing tinkling sound.",
    "Tiny blue lights float through the air here, illuminating the walls and casting shadows.",
    "Basalt platforms create formations that invoke the image of tables and chairs. Spooky? Or convenient?",
    "There's a surprising amount of foliage in this room. Tiny trees grow from cracks in the floor and walls.",
    "You see a face in the stone wall staring back at you. Turn away, and it moves somewhere else.",
    "Your shadow behaves oddly in this room, and simply stands projected from a dim light, as if watching you.",
    "A small natural basin of water decorates the center of this room. It glows with an unearthly, yet calming blue light from below.",
    "The rocks in this room feel kind of spongy."
]

class Dungeon(object):
    def __init__(self, name="Test Dungeon", floors=1, seed="TEST", floor=1, variation="0001", tileset="forest", style="dungeon", min_rooms=1, max_rooms=1, min_room_size=5, max_room_size=5, door_chance=75, min_danger_level=1, max_danger_level=1, trap_ratio=1, resource_ratio=1, enemy_ratio=1):
        self.name = name
        self.floors = floors
        self.raw_seed = seed
        self.floor = str(floor)
        self.variation = variation
        self.seed = seed + "-F" + self.floor + "-" + self.variation
        
        self.tileset = tileset
        self.style = style
        self.min_rooms = min_rooms
        self.max_rooms = max_rooms
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
        self.door_chance = door_chance
        self.min_danger_level = min_danger_level
        self.max_danger_level = max_danger_level
        self.trap_ratio = trap_ratio
        self.enemy_ratio = enemy_ratio
        self.resource_ratio = resource_ratio
        
        random.seed(self.seed)
        self.room_count = 0
        self.rooms = []
        self.doors = []
        self.doorways = []
        self.ghost_doorways = []
        self.entrance = None
        self.exit = None
        self.entities = []
        self.occupied = [] # Room tiles which have entities on top already
        self.last_dir = None
        self.room_goal = 0
        self.map = [
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        ]
        self.x_offset = 0;
        self.y_offset = 0;
        
        self.empty_row = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        fails = 0
        door_fails = 0
        
        self.room_goal = random.randint(self.min_rooms, self.max_rooms)
        while self.room_count < self.room_goal:
            plotted = self.plot_room()
            if plotted and self.room_count < self.room_goal:
                #print "DOORWAY===================================", self.room_count
                while True:
                    success = self.plot_doorway()
                    if success:
                       break 
                fails = 0
            else:
                fails += 1
            if fails and fails % 10 == 0: # Retry the doorway
                doorway = self.doorways[-1]
                #print "DOORWAY ERASE", doorway
                #self.map[doorway[1]][doorway[0]] = 0
                self.doorways = self.doorways[:-1]
                self.ghost_doorways.append(doorway)
                
                door_fails = 0
                while True:
                    door = self.plot_doorway()
                    door_fails += 1
                    if door or door_fails > 15:
                        break
                
            if fails > 100: # Completely give up
                break
        
        # Add entrance/exit
        if self.floor == "1":
            self.entrance   = self.plot_endpoint(0, ENTRANCE)
        else:
            self.entrance   = self.plot_endpoint(0, STAIRS_UP)
            
        if int(self.floor) == self.floors:
            self.exit       = self.plot_endpoint(-1, EXIT)
        else:
            self.exit       = self.plot_endpoint(-1, STAIRS_DOWN)
        
        
        # Compile entities
        self.spawns = self.load_entities()
        self.entity_ids = []
        
        
        # Set doorways/doors
        for doorway in self.doorways:
            self.map[doorway[1]][doorway[0]] = FLOOR
            if random.randint(1,100) <= self.door_chance:
                id = self.get_entity("door")
                #print "RANDOM ENTITY IS", id
                if id:
                    self.entities.append({"type":"door", "id":int(id), "coords":[doorway[0], doorway[1]]})
                    if id not in self.entity_ids:
                        self.entity_ids.append(id)
        
        # Set entities
        self.populate_entities("trap")
        self.populate_entities("resource")
        self.populate_entities("enemy")

        # Remove dead doorways
        for ghost_doorway in self.ghost_doorways:
            self.map[ghost_doorway[1]][ghost_doorway[0]] = WALL

        del self.spawns
        # Center the dungeon and entities within
        self.center_map()
        
        # Handle room descriptions
        self.descriptions = []
        for room in self.rooms:
            self.descriptions.append({
                "tl_x":room["origin"][0] + self.x_offset, 
                "tl_y":room["origin"][1] + self.y_offset, 
                "br_x":room["origin"][0] + room["size"][0] + self.x_offset - 1,
                "br_y":room["origin"][1] + room["size"][1] + self.y_offset - 1,
                "description":random.choice(DESCRIPTIONS)}) # I wonder about those -1's but it would only grab wall tiles otherwise so it's nbd.
        
    def plot_room(self):
        room = {}
        edges = {"top":[], "bottom":[], "left":[], "right":[]}
        
        size_x = random.randint(self.min_room_size,self.max_room_size)
        size_y = random.randint(self.min_room_size,self.max_room_size)
        
        if self.room_count == 0:
            origin_x = random.randint(8,16)
            origin_y = random.randint(8,16)
            doorway = None
        else:
            # Grab the latest doorway
            doorway = self.doorways[-1]
            #print doorway
            #print size_x, size_y
            #print self.last_dir
            
            if self.last_dir == "right":
                used_edge = "left"
                origin_x = doorway[0]+1 # Correct
                origin_y = doorway[1]-size_y+random.randint(2,size_y-1) # Adjust
            elif self.last_dir == "left":
                used_edge = "right"
                origin_x = doorway[0]-size_x # Correct
                origin_y = doorway[1]-size_y+random.randint(2,size_y-1) # Adjust
            elif self.last_dir == "top":
                used_edge = "bottom"
                #print "\t\tsize_y", size_y
                origin_x = doorway[0]-size_x+random.randint(2,size_x-1) # Adjust (+2 to +4 for a 5 wide room)
                origin_y = doorway[1]-size_y # Correct
            elif self.last_dir == "bottom":
                used_edge = "top"
                origin_x = doorway[0]-size_x+random.randint(2,size_x-1) # Adjust
                origin_y = doorway[1]+1 # Correct
        
        # Record properties
        room["origin"] = (origin_x, origin_y)
        room["size"] = (size_x, size_y)
        
        # Check for running off the map
        if origin_x <= 0 or origin_y <= 0 or (origin_x+size_x > 23) or (origin_y+size_y > 23): # These 23s might need to be 24s?
            return False
        # Check for overlap
        for y in xrange(0,size_y):
            for x in xrange(0,size_x):
                pt_y = origin_y+y
                pt_x = origin_x+x
                if self.map[pt_y][pt_x] != -1:
                    #print "OVERLAP AT", pt_x, pt_y
                    return False
        
        #print "ROOM ====================================="
        #print "\tLSTDIR:", self.last_dir
        #print "\tORIGIN:", room["origin"]
        #print "\tSIZE  :", room["size"]
        
        # Write the room
        for y in xrange(0,size_y):
            for x in xrange(0,size_x):
                pt_y = origin_y+y
                pt_x = origin_x+x
                self.map[pt_y][pt_x] = 1
                
                if y == 0 and x > 0 and x < (size_x - 1):
                    edges["top"].append((pt_x,pt_y))
                if y == (size_y - 1) and x > 0 and x < (size_x - 1):
                    edges["bottom"].append((pt_x,pt_y))
                if x == 0 and y > 0 and y < (size_y - 1):
                    edges["left"].append((pt_x,pt_y))
                if x == (size_x - 1) and y > 0 and y < (size_y - 1):
                    edges["right"].append((pt_x,pt_y))
                
        room["edges"] = edges
        # Get rid of the edge used to connect to previous room
        if self.room_count > 0:
            del room["edges"][used_edge] 
        # Get rid of any edges on the actual edge of the map
        if (origin_x == 0):
            del room["edges"]["left"]
        elif (origin_x + size_x + 1 >= 23):
            del room["edges"]["right"]
        if (origin_y == 0):
            del room["edges"]["top"]
        elif (origin_y + size_y + 1 >= 23):
            del room["edges"]["bottom"]
        
        
        # Write the walls
        for y in xrange(-1,size_y+1):
            for x in xrange(-1,size_x+1):
                if y == -1 or x == -1 or y == size_y or x == size_x:
                    pt_y = origin_y+y
                    pt_x = origin_x+x
                    if pt_y == -1 or pt_x == -1:
                        continue
                    self.map[pt_y][pt_x] = 0
        
        self.rooms.append(room)
        self.room_count += 1
        return True
        
    def plot_doorway(self):
        #print self.rooms
        
        # Pick a room:
        if self.style == "tunnel":
            room_num = len(self.rooms) - 1
        elif self.style == "dungeon":
            room_num = random.randint(0,len(self.rooms)-1)
        #print "ROOM #", room_num
        
        # Pick a direction
        if self.rooms[room_num]["edges"].keys():
            dir = random.choice(self.rooms[room_num]["edges"].keys())
            #print "\tDIR", dir
        else:
            #print "ROOM DUMP"
            #print self.rooms
            return False
        
        # Pick an edge
        edge = random.choice(self.rooms[room_num]["edges"][dir])
        #print "EDGE", edge
        
        # Plot a doorway
        y = edge[1]+(dir == "bottom")-(dir == "top")
        x = edge[0]+(dir == "right")-(dir == "left")
        #self.map[y][x] = 1
        #print "\tPlotted at", x, y
        
        # Remove it from the list
        del self.rooms[room_num]["edges"][dir]
        
        # Add doorway to the list
        self.doorways.append((x,y))
        self.last_dir = dir
        return True
        
    def plot_endpoint(self, room_num, type):
        # Pick a room
        #while len(self.rooms[room_num]["edges"].keys()) == 0:
        #    room_num += 1 

        while True:
            # Pick a direction
            if self.rooms[room_num]["edges"].keys():
                dir = random.choice(self.rooms[room_num]["edges"].keys())
            else:
                room_num += 1
                continue
                #print "ROOM DUMP"
                #print self.rooms
                #return False
        
            # Pick an edge
            edge = random.choice(self.rooms[room_num]["edges"][dir])
            # Remove it from the list
            del self.rooms[room_num]["edges"][dir]
            
            # Check if plottable
            y = edge[1]+(dir == "bottom")-(dir == "top")
            x = edge[0]+(dir == "right")-(dir == "left")
            if dir == "left" and self.map[y][x-1] > 0: # non void/wall
                if len(self.rooms[room_num]["edges"]) == 0:
                    None
                    #room_num += 1
                continue
            elif dir == "right" and self.map[y][x+1] > 0: # non void/wall
                if len(self.rooms[room_num]["edges"]) == 0:
                    None
                    #room_num += 1
                continue
            elif dir == "top" and self.map[y-1][x] > 0: # non void/wall
                if len(self.rooms[room_num]["edges"]) == 0:
                    None
                    #room_num += 1
                continue
            elif dir == "bottom" and self.map[y+1][x] > 0: # non void/wall
                if len(self.rooms[room_num]["edges"]) == 0:
                    None
                    #room_num += 1
                continue
            
            self.map[y][x] = type
            #print "\t"+str(type)+" Plotted at", x, y
            
            # Surround stairs with walls where there's void.
            """
            if (type == STAIRS_UP or type == STAIRS_DOWN):
                if y-1 > 0 and x-1 > 0:
                    if self.map[y-1][x-1] == VOID:
                        self.map[y-1][x-1] = WALL
                        print "Made wall 1"
                if y-1 > 0:
                    if self.map[y-1][x] == VOID:
                        self.map[y-1][x] = WALL
                        print "Made wall 2"
                if y-1 > 0 and x+1 > 0:
                    if self.map[y-1][x+1] == VOID:
                        self.map[y-1][x+1] = WALL
                        print "Made wall 3"
                        
                if x-1 > 0:
                    if self.map[y][x-1] == VOID:
                        self.map[y][x-1] = WALL
                        print "Made wall 4"
                if x+1 < 24:
                    if self.map[y][x+1] == VOID:
                        self.map[y][x+1] = WALL
                        print "Made wall 5"
                        
                if y+1 < 24 and x-1 > 0:
                    if self.map[y+1][x-1] == VOID:
                        self.map[y+1][x-1] = WALL
                        print "Made wall 6"
                if y+1 < 24:
                    if self.map[y+1][x] == VOID:
                        self.map[y+1][x] = WALL
                        print "Made wall 7"
                if y+1 > 0 and x+1 < 24:
                    if self.map[y+1][x+1] == VOID:
                        self.map[y+1][x+1] = WALL
                        print "Made wall 8"
            """
            break
            
        return (x,y)
    
    def load_entities(self):
        entities = {}
        qs = Entity.objects.filter(danger_level__gte=self.min_danger_level, danger_level__lte=self.max_danger_level).order_by("type", "name")
        for entity in qs:
            if not entities.get(entity.type):
                entities[entity.type] = {}
            
            """ Duplicating this can be done for individual item bias if needed """
            if entities[entity.type].get(entity.danger_level):
                entities[entity.type][entity.danger_level].append(entity.id)
            else:
                entities[entity.type][entity.danger_level] = [entity.id]
        return entities
        
    def get_entity(self, type):
        if not self.spawns.get(type):
            return false
            
        """ This should be baked in some way """
        levels = self.spawns[type].keys()
        levels.sort(reverse=True)
        marbles = []
        bias = [65,20,10,5,1,1,1,1,1,1,1,1,1,1,1]
        for x in xrange(0,len(levels)):
            marbles += [levels[x]]*bias[x]
        #print marbles
        
        danger_level = random.choice(marbles)
        return random.choice(self.spawns[type][danger_level])
        
    def populate_entities(self, type):
        if type == "trap":
            ratio = self.trap_ratio
        elif type == "resource":
            ratio = self.resource_ratio
        elif type == "enemy":
            ratio = self.enemy_ratio
        goal = int(ratio * self.room_goal)
        room_pool = range(0,len(self.rooms))    
        while goal > len(room_pool):
            room_pool += range(0,len(self.rooms))
        rooms = random.sample(room_pool, goal)
        
        for room in rooms:
            id = self.get_entity(type)
            if id:
                while True:
                    x_pos = random.randint(0,self.rooms[room]["size"][0]-1)
                    y_pos = random.randint(0,self.rooms[room]["size"][1]-1)
                    x_pos += self.rooms[room]["origin"][0]
                    y_pos += self.rooms[room]["origin"][1]
                    if ((x_pos,y_pos) not in self.occupied):
                        break
                
                self.entities.append({"type":type, "id":int(id), "coords":[x_pos, y_pos]})
                self.occupied.append((x_pos,y_pos))
                if id not in self.entity_ids:
                    self.entity_ids.append(id)
                    
        return True

    def text_map(self):
        text = ""
        for y in xrange(0,len(self.map)):
            row = ""
            for x in xrange(0,len(self.map[0])):
                if self.map[y][x] == VOID:
                    row += "&nbsp;"
                elif self.map[y][x] == WALL:
                    row += "#"
                elif self.map[y][x] == FLOOR:
                    row += "."
                elif self.map[y][x] == ENTRANCE:
                    row += "/"
                elif self.map[y][x] == EXIT:
                    row += "+"
                elif self.map[y][x] == STAIRS_UP:
                    row += "<"
                elif self.map[y][x] == STAIRS_DOWN:
                    row += ">"
            #print row
            text += row + "\n"
        #print "\n"
        return text
        
    def center_map(self):
        # Vertical centering
        x_offset = 0
        y_offset = 0
        remove = []
        for x in xrange(0, len(self.map)):
            if self.map[x] == self.empty_row:
                y_offset -= 1
                remove.append(x)
            else:
                break
        remove.reverse() # Flip to allow for removing to work properly
        
        for row in remove:
            del self.map[row]
            self.map.append(self.empty_row)
            
        # Now loop until you find an empty row
        dungeon_height = 0
        for x in xrange(0, len(self.map)):
            if self.map[x] != self.empty_row:
                dungeon_height += 1
            else:
                break
        
        
        adjust = ((24 - dungeon_height) / 2)
        y_offset += adjust
        
        for x in xrange(0,adjust):
            self.map.insert(0, self.empty_row)
        
        if adjust != 0:
            self.map = self.map[:(-1 * adjust)]
        
        # Horizontal centering
        has_floors = []
        for x in xrange(0, len(self.map[0])):
            for y in xrange(0, len(self.map)):
                if self.map[y][x] != VOID:
                    if x not in has_floors:
                        has_floors.append(x)
        blank_left = has_floors[0]
        blank_right = 23 - has_floors[-1]
        
        if blank_left > blank_right:
            to_adjust = 0
            while blank_left > blank_right:
                blank_left -= 1
                blank_right += 1
                to_adjust += 1
            
            for x in xrange(0,to_adjust):
                for col in xrange(0, len(self.map)):
                    self.map[col].pop(0)
                    self.map[col].append(VOID)
            x_offset = -1 * to_adjust
        else:
            to_adjust = 0
            while blank_right > blank_left:
                blank_left += 1
                blank_right -= 1
                to_adjust += 1
            
            for x in xrange(0,to_adjust):
                for col in xrange(0, len(self.map)):
                    self.map[col].pop()
                    self.map[col].insert(0,VOID)
            x_offset = to_adjust
        
        # Center entities
        for entity in self.entities:
            entity["coords"][0] += x_offset
            entity["coords"][1] += y_offset
            
        self.x_offset = x_offset
        self.y_offset = y_offset
        
        #print self.x_offset
        #print self.y_offset
        #print self.rooms

    def test_map(self):
        self.map = [
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1, 0, 0, 0, 0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1, 0, 1, 1, 0,-1,-1,-1,-1, 1, 1, 1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1, 0, 0, 0, 0,-1,-1,-1,-1, 1, 0, 1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,-1,-1,-1,-1, 1, 1, 1, 0, 1, 1, 1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1, 0, 0, 0,-1,-1, 1, 0, 0, 0, 0, 0, 1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1, 0, 1, 0,-1,-1, 1, 1, 1, 0, 1, 1, 1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [ 0, 0, 0, 1, 0, 0, 0,-1,-1, 1, 0, 1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [ 0, 1, 1, 1, 1, 1, 0,-1,-1, 1, 1, 1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [ 0, 0, 0, 1, 0, 0, 0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
        [-1,-1, 0, 1, 0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1, 1, 1, 1, 1],
        [-1,-1, 0, 0, 0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1, 0, 0, 0, 1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1, 0,-1, 0, 1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1, 0, 0, 0, 1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1, 1, 1, 1, 1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1, 1, 1, 1, 1,-1, 1, 0, 0, 0, 1],
        [-1,-1,-1,-1,-1,-1,-1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1,-1, 1, 0, 0, 0, 1],
        [-1,-1,-1,-1,-1,-1,-1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1,-1, 1, 0, 0, 0, 1],
        [-1,-1,-1,-1,-1,-1,-1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1, 1],
        [-1, 1, 1, 1,-1,-1,-1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1,-1,-1, 1, 0, 0, 1, 1],
        [-1, 1, 0, 1,-1,-1,-1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,-1,-1, 1, 0, 0, 1, 1],
        [-1, 1, 1, 1,-1,-1,-1,-1, 1, 1, 1, 1, 1, 0, 0, 0, 1,-1,-1, 1, 1, 1, 1, 1],
        [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1, 1, 1, 1, 1, 1,-1,-1,-1,-1,-1,-1,-1]
        ]
        
        self.entities = []

def dungeon_browse(request):
    data = {"session":request.session}
    if not request.session.get("userID"):
        return redirect("/login")
    if not request.session.get("teamID"):
        return redirect("/team/manage")
    
    if request.session.get("admin"):
        data["dungeons"] = Dungeon_List.objects.all().order_by("-id")
    else:
        data["dungeons"] = Dungeon_List.objects.filter(public=True).order_by("-id")
    return render_to_response("dungeons/browse.html", data)

def dungeon_explore(request, dungeon_id, variation="0001"):
    data = {"session":request.session, "version":VERSION}
    dungeon_id = int(dungeon_id)
    team_id = request.session.get("teamID")
    user_id = request.session.get("userID")
    if not team_id or not user_id:
        return redirect("/team/manage")
    
    # If you have an incomplete version of this dungeon, redirect to its map.
    matches = Team_Dungeon.objects.filter(team_id=team_id, key_id=dungeon_id, floor=1, completed=False).order_by("-dive")
    if len(matches):
        return redirect("/dungeon/view/"+str(dungeon_id)+"/"+str(team_id))
        
    # Generate a dungeon
    # Get the floors from the dungeon list
    if request.session.get("admin"):
        basics = get_object_or_404(Dungeon_List, id=dungeon_id)
    else:
        basics = get_object_or_404(Dungeon_List, id=dungeon_id, public=1)
    tileset = basics.tileset
    floors = basics.floors
    name = basics.name
    
    # Load dungeon blueprints
    blueprints = Blueprint.objects.filter(key_id=dungeon_id).order_by("floor")
    if not len(blueprints):
        raise Http404
    
    # Check if you have a completed dive, in which case the dive number needs to increment
    dive_check = Team_Dungeon.objects.filter(team_id=team_id, key_id=dungeon_id, floor=1, completed=True).order_by("-dive")
    if len(dive_check):
        dive = dive_check[0].dive + 1
    else:
        dive = 1

    #print "Generating New Dungeon"
    
    for blueprint in blueprints:
        # TEAM-USER-DKEY-DIVE-FLOR-VARI
        seed                = str(team_id)+"-"+str(user_id)+"-"+str(blueprint.key.id)+"-"+str(dive).zfill(4)
        floor               = blueprint.floor
        style               = blueprint.style
        min_rooms           = blueprint.min_rooms
        max_rooms           = blueprint.max_rooms
        min_room_size       = blueprint.min_room_size
        max_room_size       = blueprint.max_room_size
        door_chance         = blueprint.door_chance
        min_danger_level    = blueprint.min_danger_level
        max_danger_level    = blueprint.max_danger_level
        trap_ratio          = blueprint.trap_ratio
        resource_ratio      = blueprint.resource_ratio
        enemy_ratio         = blueprint.enemy_ratio
    
        dungeon = Dungeon(name, blueprint.key.floors, seed, floor, variation, tileset, style, min_rooms, max_rooms, min_room_size, max_room_size, door_chance, min_danger_level, max_danger_level, trap_ratio, resource_ratio, enemy_ratio)
        storage = Team_Dungeon(team_id=team_id, key_id=dungeon_id, floor=floor, dive=dive, seed=dungeon.seed, data=cPickle.dumps(dungeon))
        if not request.GET.get("nosave"):
            storage.save()
            #print "SAVING DUNGEON"    
    
    return redirect("/dungeon/view/"+str(dungeon_id)+"/"+str(team_id))


def dungeon_view(request, team_id=4, dungeon_id=1, dive=1, map_id=0):
    data = {"session":request.session, "version":VERSION}
    
    # Overrides
    dive = int(dive)
    data["floor"]   = int(request.GET.get("f", 1))
    data["tileset"] = request.GET.get("tileset", "parent")
    data["debug"]   = request.GET.get("debug")
    
    if not data["debug"]:     
        #print team_id, dungeon_id, data["floor"], dive
        
        if not map_id:
            #dungeon_storage = Team_Dungeon.objects.get(team_id=team_id, key_id=dungeon_id, floor=data["floor"], dive=dive)
            dungeon_storage = get_object_or_404(Team_Dungeon, team_id=team_id, key_id=dungeon_id, floor=data["floor"], dive=dive)
        else:
            #dungeon_storage = Team_Dungeon.objects.get(pk=map_id)
            dungeon_storage = get_object_or_404(Team_Dungeon, pk=map_id)
            data["minimal"] = int(request.GET.get("minimal", 0))
        dungeon = cPickle.loads(str(dungeon_storage.data))
        if data["tileset"] == "parent":
            data["tileset"] = dungeon.tileset
        
        data["yours"]       = (dungeon_storage.team.user.id == request.session.get("userID"))
        data["dive"]        = dive
        data["team_id"]     = team_id
        data["team_name"]   = dungeon_storage.team.name
        data["suffix"]      = {1:"st", 2:"nd", 3:"rd"}.get(dive, "xx")
        data["dungeon_id"]  = dungeon_id
        data["map_id"]      = dungeon_storage.id
        data["dungeon"]     = dungeon
        data["images"]      = glob(ROOT+"/assets/images/dungeons/"+data["tileset"]+"/*.png")
        data["seed"]        = dungeon.seed
        data["text_map"]    = dungeon.text_map()
        data["entities"]    = Entity.objects.filter(pk__in=dungeon.entity_ids)
        data["floors"]      = range(1, dungeon_storage.key.floors + 1)
        data["descriptions"]= dungeon.descriptions
    else:
        dungeon = Dungeon("Dungeon Preview", 1, str(request.GET.get("seed")), 1, "1", "caves", request.GET.get("style"), int(request.GET.get("min_rooms")), 
            int(request.GET.get("max_rooms")), int(request.GET.get("min_room_size")), int(request.GET.get("max_room_size")), int(request.GET.get("door_chance")), 
            int(request.GET.get("min_danger_level")), int(request.GET.get("max_danger_level")), 
            float(request.GET.get("trap_ratio")), float(request.GET.get("resource_ratio")), float(request.GET.get("enemy_ratio")))
        #dungeon.test_map()
        data["tileset"]     = dungeon.tileset
        data["yours"]       = False
        data["dive"]        = 1
        #data["team_id"]     = team_id
        #data["team_name"]   = dungeon_storage.team.name
        data["suffix"]      = {1:"st", 2:"nd", 3:"rd"}.get(dive, "xx")
        data["dungeon_id"]  = dungeon_id
        data["dungeon"]     = dungeon
        data["images"]      = glob(ROOT+"/assets/images/dungeons/"+data["tileset"]+"/*.png")
        data["seed"]        = dungeon.seed
        data["text_map"]    = dungeon.text_map()
        data["entities"]    = Entity.objects.filter(pk__in=dungeon.entity_ids)
        data["floors"]      = range(1,1)
        data["descriptions"]= dungeon.descriptions
    
    return render_to_response("dungeons/view.html", data)

def dungeon_reroll(request):
    data = {"session":request.session, "version":VERSION}
    team_id = request.session.get("teamID")
    team = get_object_or_404(Team, pk=team_id)
    
    dungeon = request.GET.get("dungeon")
    floor = request.GET.get("floor")
    #dive = request.GET.get("dive")
    dive = 1
    
    dungeon_storage = Team_Dungeon.objects.get(team_id=team_id, key_id=dungeon, floor=floor, dive=dive)
    
    if request.POST.get("action") == "reroll":
        # Erase the stored floor of the dungeon
        dungeon = cPickle.loads(str(dungeon_storage.data))
        
        reroll_log = open("/var/projects/pmdu.org/assets/data/rerolls.log", "wa")
        reroll_log.write("==== BEGIN REROLL FOR " + str(team_id) + " DUNGEON " + str(request.GET.get("dungeon")) + " FLOOR " + str(floor) + " @ " + str(datetime.now()) + "====\n")
        reroll_log.write(str(dungeon_storage.data) + "\n")
        reroll_log.write("==== END REROLL ====\n")
        reroll_log.close()
        """
        print "-----"*5
        print dungeon.name
        print dungeon.floors
        print dungeon.raw_seed
        print dungeon.floor
        print dungeon.variation
        print dungeon.tileset
        print dungeon.style
        print dungeon.min_rooms
        print dungeon.max_rooms
        print dungeon.min_room_size
        print dungeon.max_room_size
        print dungeon.door_chance
        print dungeon.min_danger_level
        print dungeon.max_danger_level
        print dungeon.trap_ratio
        print dungeon.resource_ratio
        print dungeon.enemy_ratio
        print "-----"*5
        """
        new_variation = str(int(dungeon.variation)+1).zfill(4)
        new_dungeon = Dungeon(dungeon.name, dungeon.floors, dungeon.raw_seed, dungeon.floor, new_variation, dungeon.tileset, dungeon.style, dungeon.min_rooms, dungeon.max_rooms, dungeon.min_room_size, dungeon.max_room_size, dungeon.door_chance, dungeon.min_danger_level, dungeon.max_danger_level, dungeon.trap_ratio, dungeon.resource_ratio, dungeon.enemy_ratio)
        dungeon_storage.data = cPickle.dumps(new_dungeon)
        dungeon_storage.timestamp = datetime.now()
        dungeon_storage.save()
        return redirect("/dungeon/view/"+request.GET.get("dungeon")+"/"+str(team_id)+"/"+str(dungeon_storage.dive))
    
    data["dungeon_id"] = dungeon
    data["dungeon_name"] = dungeon_storage.key.name
    data["floor"] = floor
    
    return render_to_response("dungeons/reroll.html", data, context_instance=RequestContext(request))