# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


from .dungeon import *
from datetime import datetime

start = datetime.now()
dungeons = []
output = open("dungeons.txt", "w")
#def __init__(self, name="Test Dungeon", seed="TEST", floor=1, tileset="forest", variation="0001"):
for x in range(1,2001):
    dungeons.append(Dungeon("DEBUG", "1-"+str(x)+"-S1D01"))
    
#1-108-S1D01-0001-F1
    
for dungeon in dungeons:
    text = dungeon.text_map()
    #print dungeon.seed
    #print text
    #print "\n"
    output.write("==========================================================\n")
    output.write("SEED: " + dungeon.seed + "\n")
    output.write(text + "\n")
    
print("DONE.")
print(str(start))
print(str(datetime.now()))
#319
