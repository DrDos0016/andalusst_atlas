from dungeon import *
from datetime import datetime

start = datetime.now()
dungeons = []
output = open("dungeons.txt", "w")
#def __init__(self, name="Test Dungeon", seed="TEST", floor=1, tileset="forest", variation="0001"):
for x in xrange(1,2001):
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
    
print "DONE."
print str(start)
print str(datetime.now())
#319