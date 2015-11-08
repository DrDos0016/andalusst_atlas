#!/usr/bin/python
import random

X_MIN = 0
X_MAX = 24
Y_MIN = 0
Y_MAX = 24

MIN_SIZE = 5
MAX_SIZE = 7

random.seed("TEST")

class Dungeon(object):
    def __init__(self):
        self.tileset = "forest"
        self.rooms = 0
        self.map = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]
        
        self.room_origins = []
        
        self.scan_make()
        self.scan_make()
        self.scan_make()
        
        
        #self.plot_room()
        self.draw()
        #raw_input("")
        #self.
        
    def draw(self):
        print len(self.map)
        print len(self.map[0])
        for y in xrange(0,len(self.map)):
            row = ""
            for x in xrange(0,len(self.map[0])):
                if self.map[x][y] == 0:
                    row += "*"
                else:
                    row += str(self.map[x][y])
            print row
            
            
    def plot_room(self):
        # Pick an origin
        character = str(self.rooms+1)
        origin_x = random.randint(0+8,X_MAX-8)
        origin_y = random.randint(0+8,Y_MAX-8)
        
        size_x = random.randint(MIN_SIZE,MAX_SIZE)
        size_y = random.randint(MIN_SIZE,MAX_SIZE)
        
        
        for y in xrange(origin_y,origin_y+size_y):
            for x in xrange(origin_x,origin_x+size_x):
                if y == origin_y or y == origin_y+size_y - 1:
                    self.map[x][y] = "#"
                elif x == origin_x or x == origin_x+size_x - 1:
                    self.map[x][y] = "#"
                else:
                    self.map[x][y] = "."
        
        #self.map[origin_x][origin_y] = "*"
        self.rooms += 1
        
        
    def scan_make(self, origin_x=0, origin_y=0):
        #origin_x = 0
        #origin_y = 0
        
        size_x = random.randint(MIN_SIZE,MAX_SIZE)
        size_y = random.randint(MIN_SIZE,MAX_SIZE)
        
        for y in xrange(origin_y,origin_y+size_y):
            for x in xrange(origin_x,origin_x+size_x):
                if y == origin_y or y == origin_y+size_y - 1:
                    self.map[x][y] = "#"
                elif x == origin_x or x == origin_x+size_x - 1:
                    self.map[x][y] = "#"
                else:
                    self.map[x][y] = "."
        
dungeon = Dungeon()