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

3.2 14.1 17.3 42.1 7.3 51.2 27.3 11.2 38.1 32.1 8.2

- The first double represents Player 1's move.
- The second double represents Player 2's move.
- This alternating pattern continues until the end of the game sequence.
- If the number of entries in the sequence is even, Player 1 wins.
- If the number of entries in the sequence is odd, Player 2 wins.
- The number before the decimal denotes the ID of the block being moved.
- The number after the decimal denotes the position (1, 2, or 3) that the block is placed in on top 
of the tower.
- The last number in the sequence denotes the last move before the tower fell (i.e., the final move in the sequence is what caused the tower to fall)
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
      # Checking [1]...
      blockSet = set()
      blockSet.add(-1)
      for layer in tower:
         for block in layer:
            blockSet.add(block.ID)
            if block.ID != -1 and (block.ID < 1 or block.ID > 54):
               return False
      # Checking [4]...
      if len(blockSet) != 55:
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
         ### COMMENT OUT THIS CODE TO REMOVE LEADING 0 FROM IDs < 10; ADDED FOR READABILITY
         if randID < 10:
            sequence = sequence + f"0"
         ###
         sequence = sequence + f"{randID}.{randPos} "
         if not self.isTowerValid():
            return sequence
      return sequence
   
def isValidSequence(seq):
   seq = seq.rstrip()
   result = False
   start = Tower("start")
   seq = seq.split(" ")
   for i in range(len(seq)):
      seq[i] = seq[i].split(".")
   
   for i in range(len(seq)-1):
      start.move(int(seq[i][0]),int(seq[i][1]))
      if not start.isTowerValid():
         return False
   
   start.move(int(seq[len(seq)-1][0]),int(seq[len(seq)-1][1]))
   if not start.isTowerValid():
      return True
   return result


      
###################################################################################################
###################################################################################################

seqSet = set()
seqLenLst = []
p1_wins = 0
p2_wins = 0
SEQ_GEN_NUM = 10000
runGenerator = True

if runGenerator:
   file = open(f"{SEQ_GEN_NUM}-sequences.txt", "w")

   print(f"Generating {SEQ_GEN_NUM} sequences...")

   i = 0
   while len(seqSet) < SEQ_GEN_NUM:
      if (i+1) % 5000 == 0:
         print(f">> Generated {i+1} sequences...")
      startTower = Tower("start")
      seq = startTower.generateSequence()
      seqSet.add(seq)
      seqSplit = seq.split()
      seqLenLst.append(len(seqSplit))
      i += 1
   for seq in seqSet:
      file.write(f"{seq}\n")
   print("...done.\n")
   print("Min sequence length:",min(seqLenLst))
   print("Max sequence length:",max(seqLenLst))
   for seqLen in seqLenLst:
      if seqLen % 2 == 0: # Even, P1 Wins
         p1_wins += 1
      else: # Odd, P2 Wins
         p2_wins += 1
   print(f"P1 Win %: {(p1_wins/SEQ_GEN_NUM)*100}%")
   print(f"P2 Win %: {(p2_wins/SEQ_GEN_NUM)*100}%")
   file.close()