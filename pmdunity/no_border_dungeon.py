# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


import random
from datetime import datetime
#random.seed("1-1-S1D01")
#random.seed("1-4-S1D01") # exit right
#random.seed("1-4-S1D07") # exit left
#random.seed("1-4-S1D08") # exit right

# Tile ID
VOID        = -1
WALL        = 0
FLOOR       = 1
ENTRANCE    = 2
EXIT        = 3
UP_STAIRS   = 4
DOWN_STAIRS = 5

class Dungeon(object):
    def __init__(self, name="Test Dungeon", seed="TEST", floor=1, tileset="forest", variation="0001"):
        self.name = name
        self.raw_seed = seed
        self.floor = "F"+str(floor)
        self.variation = variation
        self.seed = seed + "-" + self.floor + "-" + self.variation
        
        self.tileset = "forest"
        self.style = "tunnel"
        self.min_rooms = 5
        self.max_rooms = 5
        self.min_room_size = 5
        self.max_room_size = 5
        
        random.seed(self.seed)
        self.room_count = 0
        self.rooms = []
        self.doorways = []
        self.ghost_doorways = []
        self.entrance = None
        self.exit = None
        self.last_dir = None
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
        
        self.empty_row = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        fails = 0
        door_fails = 0
        
        while self.room_count < 5:
            plotted = self.plot_room()
            if plotted and self.room_count < 5:
                print "DOORWAY===================================", self.room_count
                self.plot_doorway()
                fails = 0
            else:
                fails += 1
            if fails and fails % 10 == 0: # Retry the doorway
                doorway = self.doorways[-1]
                print "DOORWAY ERASE", doorway
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
        print "DEFINE ENTRANCE/EXIT ========================="
        self.plot_doorway(0)
        self.plot_doorway(-1)
        self.entrance   = self.doorways[-2]
        self.exit       = self.doorways[-1]
        print "ENT: ", self.entrance
        print "EXT: " , self.exit
        
        # Cleanup
        # Remove dead doorways
        print self.doorways
        print self.ghost_doorways
        for ghost_doorway in self.ghost_doorways:
            None
            self.map[ghost_doorway[1]][ghost_doorway[0]] = 0
            
        # Mark entrance/exit
        self.map[self.entrance[1]][self.entrance[0]]    = ENTRANCE
        self.map[self.exit[1]][self.exit[0]]            = EXIT
        
        # Lastly, center the dungeon
        #self.center_map()
        #print self.text_map()
        
    def plot_room(self):
        room = {}
        edges = {"top":[], "bottom":[], "left":[], "right":[]}
        
        size_x = random.randint(3,6)
        size_y = random.randint(3,6)
        
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
        print "\tTRYING ORIGIN:", room["origin"], "SIZE:", room["size"], "DOORWAY:", doorway
        
        # Check for running off the map
        if origin_x < 0 or origin_y < 0 or (origin_x+size_x > 23) or (origin_y+size_y > 23): # These 23s might need to be 24s?
            return False
        # Check for overlap
        for y in xrange(0,size_y):
            for x in xrange(0,size_x):
                pt_y = origin_y+y
                pt_x = origin_x+x
                if self.map[pt_y][pt_x] == 1:
                    #print "OVERLAP AT", pt_x, pt_y
                    return False
        
        print "ROOM ====================================="
        print "\tLSTDIR:", self.last_dir
        print "\tORIGIN:", room["origin"]
        print "\tSIZE  :", room["size"]
        
        # Write the room
        for y in xrange(0,size_y):
            for x in xrange(0,size_x):
                pt_y = origin_y+y
                pt_x = origin_x+x
                self.map[pt_y][pt_x] = 1
                
                if y == 0 and x > 0 and x < (size_x - 1):
                    #print "TOP EDGE:", (pt_x, pt_y)
                    edges["top"].append((pt_x,pt_y))
                if y == (size_y - 1) and x > 0 and x < (size_x - 1):
                    #print "BOTTOM EDGE:", (pt_x, pt_y)
                    edges["bottom"].append((pt_x,pt_y))
                if x == 0 and y > 0 and y < (size_y - 1):
                    #print "LEFT EDGE:", (pt_x, pt_y)
                    edges["left"].append((pt_x,pt_y))
                if x == (size_x - 1) and y > 0 and y < (size_y - 1):
                    #print "RIGHT EDGE:", (pt_x, pt_y)
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
        self.rooms.append(room)
        self.room_count += 1
        return True
        
    def plot_doorway(self, room_num="rnd"):
        #print self.rooms
        
        # Pick a room
        if room_num == "rnd":
            room_num = random.randint(0,len(self.rooms)-1)
        else:
            # Make sure specified room works
            while len(self.rooms[room_num]["edges"].keys()) == 0:
                room_num += 1
        #print "ROOM #", room_num
        
        # Pick a direction
        if self.rooms[room_num]["edges"].keys():
            dir = random.choice(self.rooms[room_num]["edges"].keys())
            print "\tDIR", dir
        else:
            print "ROOM DUMP"
            print self.rooms
            return False
        
        # Pick an edge
        edge = random.choice(self.rooms[room_num]["edges"][dir])
        #print "EDGE", edge
        
        # Plot a doorway
        y = edge[1]+(dir == "bottom")-(dir == "top")
        x = edge[0]+(dir == "right")-(dir == "left")
        self.map[y][x] = 1
        print "\tPlotted at", x, y
        
        # Remove it from the list
        del self.rooms[room_num]["edges"][dir]
        
        # Add doorway to the list
        self.doorways.append((x,y))
        self.last_dir = dir
        return True
        
    def text_map(self):
        text = ""
        for y in xrange(0,len(self.map)):
            row = ""
            for x in xrange(0,len(self.map[0])):
                if self.map[y][x] == -1:
                    row += "&nbsp;"
                elif self.map[y][x] == 0:
                    row += "#"
                elif self.map[y][x] == 1:
                    row += "."
                elif self.map[y][x] == 2:
                    row += "+"
                elif self.map[y][x] == 3:
                    row += "+"
            #print row
            text += row + "\n"
        print "\n"
        return text
        
    def center_map(self):
        # Vertically
        remove = []
        for x in xrange(0, len(self.map)):
            if self.map[x] == self.empty_row:
                remove.append(x)
        remove.reverse()
        for row in remove:
            del self.map[row]
            
        if len(self.map) % 2 == 0:
            self.map.append(self.empty_row)
            
        while len(self.map) < 24:
            self.map.insert(0, self.empty_row)
            self.map.append(self.empty_row)
            
        # Horizontally
        has_floors = []
        for x in xrange(0, len(self.map[0])):
            for y in xrange(0, len(self.map)):
                if self.map[y][x] != 0:
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
                    self.map[col].append(0)
        else:
            to_adjust = 0
            while blank_right > blank_left:
                blank_left += 1
                blank_right -= 1
                to_adjust += 1
            
            for x in xrange(0,to_adjust):
                for col in xrange(0, len(self.map)):
                    self.map[col].pop()
                    self.map[col].insert(0,0)
