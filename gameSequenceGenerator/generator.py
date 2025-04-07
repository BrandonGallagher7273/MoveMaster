###############################################
# generator.py
###############################################
import sys
import random
import math

print("running game sequence generator...\n")

# Probability constants
TURN_INCREASE = 0.002
LAYERS_ABOVE_START = 0.08
SUBTRACT_PER_LAYER = 0.003
SIDE_INCREASE = 0.008
BLOCKS_AROUND = 0.008
BLOCK_AROUND_LIST = [0.0]*54

PROB_UNDER_COUNT = 0

class Block:
    def __init__(self, ID, pos, prob=0):
        self.ID = int(ID)
        self.pos = pos
        self.prob = prob

    def __repr__(self):
        if self.ID == -1:
            return "<   >"
        if self.ID < 10:
            return f"<B0{self.ID}>"
        return f"<B{self.ID}>"

    def print_prob(self):
        if self.ID == -1:
            return "<      >"
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

    def addProb(self, prob):
        self.prob += prob

    def isNull(self):
        return (self.ID == -1)

class Tower:
    def __init__(self, name, silent_prob=False):
        self.name = str(name)
        self.silent_prob = silent_prob
        self.moves = 0
        self.tower = []

        blockID = 1
        for layer in range(18):
            currLayer = []
            for b in range(3):
                currLayer.append(Block(blockID, b+1))
                blockID += 1
            self.tower.append(currLayer)

    def __repr__(self):
        out = ""
        for i in range(len(self.tower)-1, -1, -1):
            out += "\n" + str(self.tower[i])
        return f":{self.name}:{out}"

    def print_prob(self):
        reprStr = ""
        for l in range(len(self.tower)-1, -1, -1):
            for i in range(3):
                reprStr += self.tower[l][i].print_prob()
            reprStr += "\n"
        return f":{self.name}:\n{reprStr}"

    def _findBlock(self, ID):
        for l_idx, layer in enumerate(self.tower):
            for b_idx, blk in enumerate(layer):
                if blk.getID() == ID:
                    return (l_idx, b_idx)
        return (None, None)

    def isTowerValid(self):
        if len(self.tower) < 18 or len(self.tower) > 54:
            return False
        blockSet = set([-1])
        for layer in self.tower:
            for blk in layer:
                if blk.getID() != -1 and (blk.getID() < 1 or blk.getID() > 54):
                    return False
                blockSet.add(blk.getID())
        if len(blockSet) != 55:
            return False
        return True

    def move(self, ID, newPos, flag):
        lvl, idx = self._findBlock(ID)
        if lvl is None:
            return False

        topIndex = len(self.tower)-1
        if lvl >= topIndex-1:
            return False

        if flag:
            rand_val = random.random()
            prob_val = self.tower[lvl][idx].getProb()
            if not self.silent_prob:
                print(f"Comparing random {rand_val:.3f} vs block {ID}'s prob {prob_val:.3f}")
            if rand_val < prob_val:
                if not self.silent_prob:
                    print(f"Move for block {ID} failed by probability!")
                return False
        self.tower[lvl][idx].setID(-1)
        topLayer = self.tower[-1]
        hasNull = any(b.isNull() for b in topLayer)
        if hasNull:
            if not topLayer[newPos-1].isNull():
                return False
            topLayer[newPos-1] = Block(ID, newPos)
        else:
            newLayer = [Block(-1,1), Block(-1,2), Block(-1,3)]
            if not newLayer[newPos-1].isNull():
                return False
            newLayer[newPos-1] = Block(ID, newPos)
            self.tower.append(newLayer)

        self.moves += 1
        self.change_probabilities(ID, lvl, idx)
        return True

    def generateSequence(self):
        seq = ""
        posLst = [1,2,3]

        while self.isTowerValid():
            if len(posLst) == 0:
                posLst = [1,2,3]

            randPos = random.choice(posLst)
            posLst.remove(randPos)

            topIDs = set(b.getID() for b in self.tower[-1])
            randID=0
            while randID==0 or randID in topIDs:
                randID = random.randint(1,54)

            test = self.move(randID, randPos, True)
            if randID<10:
                seq+="0"
            seq+=f"{randID}.{randPos} "

            if not test:
                global PROB_UNDER_COUNT
                PROB_UNDER_COUNT+=1
                return seq
            if not self.isTowerValid():
                return seq

        return seq

    def resetprob(self):
        for layer in self.tower:
            for b in layer:
                b.setProb(0)

    def change_probabilities(self, ID, level, block_index):
        layer_increase = TURN_INCREASE * pow(1.3, (self.moves // 2))
        layers_above = []
        prob_add = LAYERS_ABOVE_START
        for ly in self.tower:
            if len(ly) == 3:
                if prob_add < 0:
                    prob_add = 0.0
                layers_above.extend([prob_add, prob_add, prob_add])
            prob_add -= SUBTRACT_PER_LAYER
        side_prob = []
        for ly in self.tower:
            if len(ly) == 3:
                side_prob.extend([SIDE_INCREASE, 0, SIDE_INCREASE])
        if level > 1:
            for i in range(3):
                if i == block_index:
                    BLOCK_AROUND_LIST[self.tower[level-1][i].getID()-1] += BLOCKS_AROUND
                else:
                    BLOCK_AROUND_LIST[self.tower[level-1][i].getID()-1] += (BLOCKS_AROUND / 2)

        if level < (len(self.tower) - 1):
            for i in range(3):
                if i == block_index:
                    BLOCK_AROUND_LIST[self.tower[level+1][i].getID()-1] += BLOCKS_AROUND
                else:
                    BLOCK_AROUND_LIST[self.tower[level+1][i].getID()-1] += (BLOCKS_AROUND / 2)

        if block_index == 0:
            BLOCK_AROUND_LIST[self.tower[level][1].getID()-1] += BLOCKS_AROUND
            BLOCK_AROUND_LIST[self.tower[level][2].getID()-1] += (BLOCKS_AROUND / 2)
        elif block_index == 1:
            BLOCK_AROUND_LIST[self.tower[level][0].getID()-1] += BLOCKS_AROUND
            BLOCK_AROUND_LIST[self.tower[level][2].getID()-1] += BLOCKS_AROUND
        else:
            BLOCK_AROUND_LIST[self.tower[level][0].getID()-1] += (BLOCKS_AROUND / 2)
            BLOCK_AROUND_LIST[self.tower[level][1].getID()-1] += BLOCKS_AROUND

        old_prob_factor = 0.70  
        new_factor = 0.30       

        idx_count = 0
        for ly_i, layer in enumerate(self.tower):
            for blk_i, blk_obj in enumerate(layer):
                old_prob = blk_obj.getProb()

                if ly_i == len(self.tower) - 1:
                    blk_obj.setProb(0.0)
                else:
                    increments_val = layer_increase + layers_above[idx_count] + side_prob[idx_count] + BLOCK_AROUND_LIST[blk_obj.getID()-1]
                    new_prob = (old_prob * old_prob_factor) + (increments_val * new_factor)
                    new_prob = min(new_prob, 1.0)
                    blk_obj.setProb(new_prob)

                idx_count += 1
        for i in range(len(BLOCK_AROUND_LIST)):
            BLOCK_AROUND_LIST[i] = 0.0

def isValidSequence(seq):
    return True

#################################################
# MAIN GENERATION
#################################################
seqSet=set()
seqLenLst=[]
p1_wins=0
p2_wins=0

SEQ_GEN_NUM=10000
runGenerator=True

if runGenerator:
    outFileName = f"{SEQ_GEN_NUM}-sequences.txt"
    file = open(outFileName, "w")

    print(f"Generating {SEQ_GEN_NUM} sequences...")

    i=0
    while i<SEQ_GEN_NUM:
        for z in range(54):
            BLOCK_AROUND_LIST[z] = 0.0 
        tower = Tower("start", silent_prob=True)
        seq = tower.generateSequence()
        seqSplit = seq.split()
        seqLenLst.append(len(seqSplit))
        seqSet.add(seq)
        i+=1

    for s in seqSet:
        file.write(s + "\n")
    file.close()

    print("...done.\n")
    print("Min seq length:", min(seqLenLst))
    print("Max seq length:", max(seqLenLst))

    for sLen in seqLenLst:
        if sLen%2==0:
            p1_wins+=1
        else:
            p2_wins+=1
    print(f"P1 Win %: {(p1_wins/SEQ_GEN_NUM)*100}%")
    print(f"P2 Win %: {(p2_wins/SEQ_GEN_NUM)*100}%")
    print(f"Times Failed Due to Probability: {PROB_UNDER_COUNT}")
    print(f"Unique sequences in final file: {len(seqSet)}")
    print(f"Output file => {outFileName}")
