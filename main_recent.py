import sys
import random
print("running game sequence generator...\n")
#if len(sys.argv) != 2:
#  print("ERROR: Please provide a Jenga game sequence, delimited by \"sequence\".")
#  sys.exit()

#seq = sys.argv[1]
#seq = seq.split(" ")

#for i in range(len(seq)):
#   seq[i] = seq[i].split(".")

#print("seqLst >>",seq)

"""
The following sequence is an example of how we will internally represent Jenga games:

3.2 14.1 17.3 42.1 7.3 51.2 27.3 11.2 38.1 32.1 8.0

- The first double represents Player 1's move.
- The second double represents Player 2's move.
- This alternating pattern continues until the end of the game sequence.
- If the number of entries in the sequence is even, Player 1 wins.
- If the number of entries in the sequence is odd, Player 2 wins.
- The number before the decimal denotes the ID of the block being moved.
- The number after the decimal denotes the position (1, 2, or 3) that the block is placed in on top 
of the tower, 0 indicating the end of the game sequence.
"""

# Defines a Block object. Each block has a unique ID, and posXY (does not have to be unique).
# Blocks can be compared using the == operator.
# Blocks can be printed as defined in __repr__.
class Block:
   def __init__(self, ID, pos):
      self.ID = int(ID)
      self.pos = pos

   def __repr__(self):
      if self.ID == -1:
         return f"<   >"
      if self.ID < 10:
         return f"<B0{self.ID}>"
      return f"<B{self.ID}>"
      #return f"<B{self.ID}, ({self.posXY[0]},{self.posXY[1]})>" # Prints posXY of each block

   def __eq__(self, other):
      isEqual = False
      if self.ID == other.ID:
         isEqual = True
      return isEqual
   
   def __hash__(self):
      return hash(self.ID)

   def getID(self):
      return self.ID

   def getPos(self):
      return self.pos
   
   def setID(self, ID):
      self.ID = ID
   
   def setPos(self, pos):
      self.pos = pos

   def isNull(self):
      if self.ID == -1:
         return True
      return False
      
   
class Tower:
   def __init__(self,name):
      self.name = str(name)
      self.tower = []
      blockID = 1
      for layer in range(18):
         currLayer = []
         for block in range(3):
            currLayer.append(Block(blockID,block+1))
            blockID += 1
         self.tower.append(currLayer)
   
   def __repr__(self):
      reprStr = ""
      for l in range(len(self.tower)-1, -1, -1):
         reprStr = reprStr + "\n" + str(self.tower[l])
      return f":{self.name}:{reprStr}"
   
   def getTopLayer(self):
      return self.tower[len(self.tower)-1]
   
   # For a tower to be considered valid, the following must be true:
   # [0] The number of nullBlocks in the tower must be equal to the number of moves made. (Trivial)
   # [1] Each block in the tower must have a unique ID number, 1 --> 54 (excluding nullBlocks).
   # [2] The tower must have at least 18 layers and at most 54 layers.
   # [3] There must not be 2 or more consecutive nullBlocks in any layer (excluding an unfinished top layer).
   # [4] There must always be 54 blocks in the tower.
   def isTowerValid(self):
      tower = self.tower
      # Checking [1] and [4]...
      blockSet = set()
      blockSet.add(-1)
      for layer in tower:
         for block in layer:
            blockSet.add(block.ID)
            if block.ID != -1 and (block.ID < 1 or block.ID > 54):
               return False
      # UNCOMMENT THIS CODE WHEN ADDING BLOCKS TO TOP OF TOWER IS IMPLEMENTED #
      if len(blockSet) != 55:
         print("#####\nINVALID BLOCKSSET:",blockSet)
         print("#####\n")
         print("# of blocks in blockset:",len(blockSet))
         return False
      
      # Checking [2]...
      if len(tower) < 18 or len(tower) > 54:
         return False
      # Checking [3]...
      for l,layer in enumerate(tower):
         for b,block in enumerate(layer):
            if(block.isNull() and l != len(tower)-1):
               if b == 1:
                  if layer[b-1].isNull() or layer[b+1].isNull():
                     return False
               elif b == 0:
                  if layer[b+1].isNull():
                     return False
               elif b == 2:
                  if layer[b-1].isNull():
                     return False
      # If all checks passed, return True               
      return True
   

   # Moves Block to a designated open spot (newPos) in the top layer.
   # newPos is either 1, 2, or 3.
   def move(self,ID, newPos):
      # If the top layer of the tower is not complete...
      topNotComplete = False
      # Disregards any moves in the top layer.
      for block in self.getTopLayer():
         if block.getID() == ID:
            return
         if block.isNull():
            topNotComplete = True
            break

      for l in range(len(self.tower)):
         for b in range(3):
            if self.tower[l][b].ID == ID:
               self.tower[l][b].setID(-1)

      if topNotComplete:
         self.tower[len(self.tower)-1][newPos-1] = Block(ID,newPos)
      else:
         newTop = [Block(-1,1), Block(-1,2), Block(-1,3)]
         newTop[newPos-1] = Block(ID,newPos)
         self.tower.append(newTop)

      #if not self.isTowerValid():
      #   print("### TOWER FELL...")

   def generateSequence(self):
      sequence = ""
      posLst = [1,2,3]
      while self.isTowerValid():
         if len(posLst) == 0:
            posLst = [1,2,3]
         randPos = random.choice(posLst)
         posLst.remove(randPos)
         randID = 0
         topLayer = self.getTopLayer()
         topLayerIDs = set()
         for block in topLayer:
            topLayerIDs.add(block.getID())
         while randID in topLayerIDs or randID == 0:
            randID = random.randint(1,54)
         
         self.move(randID,randPos)
         sequence = sequence + f"{randID}.{randPos} "
         if not self.isTowerValid():
            return sequence
      return sequence
   
def isValidSequence(seq):
   seq = seq.rstrip()
   result = False
   #print("seq:",seq)
   start = Tower("start")
   seq = seq.split(" ")
   for i in range(len(seq)):
      seq[i] = seq[i].split(".")
   
   for i in range(len(seq)-1):
      start.move(int(seq[i][0]),int(seq[i][1]))
      if not start.isTowerValid():
         return False
   
   #print(f"{int(seq[len(seq)-1][0])},{int(seq[len(seq)-1][1])}")
   start.move(int(seq[len(seq)-1][0]),int(seq[len(seq)-1][1]))
   if not start.isTowerValid():
      return True
   return result


      
###################################################################################################
###################################################################################################

startTower = Tower("start")
#print(startTower)


#for move in seq:
#   startTower.move(int(move[0]),int(move[1]))

#print(startTower)
seqSet = set()
for i in range(100):
   startTower = Tower("start")
   seq = startTower.generateSequence()
   print("Is seq valid? >>",isValidSequence(seq))
   seqSplit = seq.split()
   seqSet.add(len(seqSplit))

print("Min sequence length:",min(seqSet))
print("Max sequence length:",max(seqSet))
#print("isTowerValid? >>",startTower.isTowerValid())
# Owness is on user to ensure that they adhere to the following rules:
# 1. Taking pieces from the topmost layer is not allowed.
# 2. 
