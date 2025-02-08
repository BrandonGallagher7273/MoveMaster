print("running game sequence generator...\n\n")

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
class Block:
   def __init__(self, ID, posXY):
      self.ID = int(ID)
      self.posXY = posXY

   def __repr__(self):
      return f"<B{self.ID}>"
      #return f"<B{self.ID}, ({self.posXY[0]},{self.posXY[1]})>" # Prints posXY of each block



# For a tower to be considered valid, the following must be true:
# [1] Each layer cannot have two consecutive missing blocks
def isTowerValid(tower):
   return True


# nullBlock represents a 
nullBlock = Block(-1,[0,0])

tower = []
blockID = 1
for layer in range(18):
   currLayer = []
   for block in range(3):
      if layer % 2 == 0:   # If the layer is EVEN
         currLayer.append(Block(blockID,[1,block+1]))
      else:                # If the layer is ODD
         currLayer.append(Block(blockID,[block+1,1]))
      blockID += 1
   tower.append(currLayer)
   

for layer in tower:
   print(layer)