## generator.py ##
import sys
import random
import math
print("running game sequence generator...\n")

#Probabilities
TURN_INCREASE = 0.0002 
LAYERS_ABOVE_START = 0.0002
SUBTRACT_PER_LAYER = 0.0003
SIDE_INCREASE = 0.0008
BLOCKS_AROUND = 0.0008
BLOCK_AROUND_LIST = [0.0000] * 54

PROB_UNDER_COUNT = 0

class Block:
   def __init__(self, ID, pos, prob=0):
      self.ID = int(ID)
      self.pos = pos
      self.prob = prob

   def __repr__(self):
      if self.ID == -1:
         return f"<   >"
      if self.ID < 10:
         return f"<B0{self.ID}>"
      return f"<B{self.ID}>"

   def print_prob(self):
      if self.ID == -1:
         return f"<      >"
      return "<{:.4f}>".format(self.prob)

   def __eq__(self, other):
      return (self.ID == other.ID)
   
   def __hash__(self):
      return hash(self.ID)

   def getID(self):
      return self.ID

   def getPos(self):
      return self.pos
   
   def getProb(self):
      return self.prob
   
   def setID(self, ID):
      self.ID = ID
   
   def setPos(self, pos):
      self.pos = pos

   def setProb(self, prob):
      self.prob = prob

   def addProb(self,prob):
      self.prob += prob

   def checkProb(self):
      return self.prob

   def isNull(self):
      return (self.ID == -1)

class Tower:
   def __init__(self, name, silent_prob=True):
      self.name = str(name)
      self.moves = 0
      self.tower = []
      self.silent_prob = silent_prob

      blockID = 1
      for layer in range(18):
         currLayer = []
         for _ in range(3):
            currLayer.append(Block(blockID, pos=0))
            blockID += 1
         self.tower.append(currLayer)
   
   def __repr__(self):
      reprStr = ""
      for l in range(len(self.tower)-1, -1, -1):
         reprStr += "\n" + str(self.tower[l])
      return f":{self.name}:{reprStr}"
   
   def print_prob(self):
      reprStr = ""
      for l in range(len(self.tower)-1, -1, -1):
         for i in range(3):
            reprStr += self.tower[l][i].print_prob()
         reprStr += "\n"
      return f":{self.name}:\n{reprStr}"

   def isTowerValid(self):
      #temp
      return True

   def _findBlock(self, ID):
      for l_idx, layer in enumerate(self.tower):
         for b_idx, blk in enumerate(layer):
            if blk.ID == ID:
               return (l_idx, b_idx)
      return (None, None)

   def resetprob(self):
      for layer in self.tower:
         for b in layer:
            b.setProb(0)

   def move(self, ID, newPos, flag):
      removeLevel, removeIdx = self._findBlock(ID)
      if removeLevel is None:
         return False

      # Probability check
      if flag and not self.silent_prob:
         rand_val = random.random()
         prob_val = self.tower[removeLevel][removeIdx].getProb()
         print(f"Comparing random number {rand_val:.3f} with block {ID}'s prob {prob_val:.3f}")
         if rand_val < prob_val:
            print(f"Move for block {ID} failed due to random probability!")
            return False

      self.tower[removeLevel][removeIdx].setID(-1)

      topLayer = self.tower[-1]
      hasNull = any(b.isNull() for b in topLayer)
      if hasNull:
         if not self.tower[-1][newPos-1].isNull():
            return False
         self.tower[-1][newPos-1] = Block(ID, pos=newPos)
      else:
         newL = [Block(-1,1), Block(-1,2), Block(-1,3)]
         if not newL[newPos-1].isNull():
            return False
         newL[newPos-1] = Block(ID, pos=newPos)
         self.tower.append(newL)

      self.moves += 1
      self.change_probabilities(ID, removeLevel, removeIdx)
      return True

   def generateSequence(self):
      sequence = ""
      posLst = [1,2,3]
      while True:
         if len(posLst) == 0:
            posLst = [1,2,3]
         randPos = random.choice(posLst)
         posLst.remove(randPos)

         randID = 0
         topIDs = set(b.ID for b in self.tower[-1])
         while randID in topIDs or randID==0:
            randID = random.randint(1,54)

         test = self.move(randID, randPos, True)
         if randID < 10:
            sequence += "0"
         sequence += f"{randID}.{randPos} "
         if not test:
            global PROB_UNDER_COUNT
            PROB_UNDER_COUNT += 1
            return sequence
         if self.moves > 150: # arbitrary
            return sequence

   def change_probabilities(self, ID, level, block):
      self.resetprob()
      layer_increase = TURN_INCREASE * pow(1.3,(self.moves // 2))

      layers_above = []
      prob_add = LAYERS_ABOVE_START
      for ly in self.tower:
         if len(ly) == 3:
            if prob_add < 0:
               prob_add = 0.0000
            layers_above.extend([prob_add, prob_add, prob_add])
         prob_add -= SUBTRACT_PER_LAYER

      side_prob = []
      for ly in self.tower:
         if len(ly) == 3:
            side_prob.extend([SIDE_INCREASE,0,SIDE_INCREASE])

      if level > 1:
         for i in range(3):
            if i == block:
               BLOCK_AROUND_LIST[self.tower[level-1][i].getID()-1]+=BLOCKS_AROUND
            else:
               BLOCK_AROUND_LIST[self.tower[level-1][i].getID()-1]+=BLOCKS_AROUND/2
      if level < len(self.tower)-1:
         for i in range(3):
            if i == block:
               BLOCK_AROUND_LIST[self.tower[level+1][i].getID()-1]+=BLOCKS_AROUND
            else:
               BLOCK_AROUND_LIST[self.tower[level+1][i].getID()-1]+=BLOCKS_AROUND/2

      if block == 0:
         BLOCK_AROUND_LIST[self.tower[level][1].getID()-1]+=BLOCKS_AROUND
         BLOCK_AROUND_LIST[self.tower[level][2].getID()-1]+=BLOCKS_AROUND/2
      elif block == 1:
         BLOCK_AROUND_LIST[self.tower[level][0].getID()-1]+=BLOCKS_AROUND
         BLOCK_AROUND_LIST[self.tower[level][2].getID()-1]+=BLOCKS_AROUND
      else:
         BLOCK_AROUND_LIST[self.tower[level][0].getID()-1]+=BLOCKS_AROUND/2
         BLOCK_AROUND_LIST[self.tower[level][1].getID()-1]+=BLOCKS_AROUND

      counter = 0
      for ly in self.tower:
         for blk in ly:
            if self.tower.index(ly) == len(self.tower)-1:
               blk.setProb(0.0000)
            else:
               blk.addProb(layer_increase + layers_above[counter] + side_prob[counter] + BLOCK_AROUND_LIST[blk.getID()-1])
               blk.setProb(min(blk.getProb(),1.0000))
            counter+=1

def isValidSequence(seq):
   return True  # stub

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
      BLOCK_AROUND_LIST = [0.0]*54
      if (i+1)%5000==0:
         print(f">> Generated {i+1} sequences...")
      startT = Tower("start", silent_prob=True)
      seq = startT.generateSequence()
      old_size = len(seqSet)
      seqSet.add(seq)
      if len(seqSet)>old_size:
         splitted = seq.split()
         seqLenLst.append(len(splitted))
      i+=1
   for s in seqSet:
      file.write(s+"\n")
   file.close()

   print("...done.\n")
   print("Min seq length:", min(seqLenLst))
   print("Max seq length:", max(seqLenLst))
   print("Len seqLenLst:", len(seqLenLst))
   print(f"Times Probability Fails: {PROB_UNDER_COUNT}")
