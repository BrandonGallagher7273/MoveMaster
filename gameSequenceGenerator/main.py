print("running game sequence generator...\n")

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
   def __init__(self, ID, posXY):
      self.ID = int(ID)
      self.posXY = posXY

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

   def getPosXY(self):
      return self.posXY
      
   


class Tower:
   def __init__(self,name):
      self.name = str(name)
      self.tower = []
      blockID = 1
      for layer in range(18):
         currLayer = []
         for block in range(3):
            if layer % 2 == 0:   # If the layer is EVEN
               currLayer.append(Block(blockID,[1,block+1]))
            else:                # If the layer is ODD
               currLayer.append(Block(blockID,[block+1,1]))
            blockID += 1
         self.tower.append(currLayer)
   
   def __repr__(self):
      reprStr = ""
      for l in range(len(self.tower)-1, -1, -1):
         reprStr = reprStr + "\n" + str(self.tower[l])
      return f":{self.name}:{reprStr}"
      #return f"<B{self.ID}, ({self.posXY[0]},{self.posXY[1]})>" # Prints posXY of each block
   
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
      """
      if len(blockSet) != 55:
         return False
      """
      # Checking [2]...
      if len(tower) < 18 or len(tower) > 54:
         return False
      # Checking [3]...
      nullBlock = Block(-1,[0,0])
      for l,layer in enumerate(tower):
         for b,block in enumerate(layer):
            if(block == nullBlock and l != len(tower)-1):
               if b == 1:
                  if layer[b-1] == nullBlock or layer[b+1] == nullBlock:
                     return False
               elif b == 0:
                  if layer[b+1] == nullBlock:
                     return False
               elif b == 2:
                  if layer[b-1] == nullBlock:
                     return False
      # If all checks passed, return True               
      return True
   
   # Moves Block to an open spot in the top layer.
   def move(self,ID):
      nullBlock = Block(-1,[0,0])
      for l in range(len(self.tower)):
         for b in range(3):
            if self.tower[l][b].ID == ID:
               self.tower[l][b] = nullBlock
      
      # If the top layer of the tower is not complete...
      if len(set(self.getTopLayer())) != 3:
         for b in range(3):
            if self.tower[len(self.tower)-1][b] == nullBlock:
               if len(self.tower)-1 % 2 == 0: # If the current layer is EVEN
                  self.tower[len(self.tower)-1][b] = Block(ID,[1,b])
                  return
               else:
                  self.tower[len(self.tower)-1][b] = Block(ID,[b,1])
                  return
      else:
         newTop = []
         newTop.append(Block(ID,[1,1]))
         for i in range(2):
            newTop.append(nullBlock)
         self.tower.append(newTop)
###################################################################################################
###################################################################################################

# nullBlock represents an empty block (i.e., a space where a block was removed)
nullBlock = Block(-1,[0,0])

# Creates and initializes Jenga tower to standard start state
startTower = Tower("start")
print(startTower)

# Testing removing 1 block
print("\n\n# After removing 1 block...")
startTower.move(3)
print(startTower)
print("\nisTowerValid? >>",startTower.isTowerValid())


# Testing removing 2 blocks
print("\n\n# After removing a second block...")
startTower.move(2)
print(startTower)
print("\nisTowerValid? >>",startTower.isTowerValid())
"""
newTower = Tower("tower1")
print(newTower)

#while isTowerValid(tower):
#   print(yay)
"""