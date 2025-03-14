import gymnasium
from gymnasium import spaces
import numpy as np
import random
import math

# Import or copy your Tower, Block classes here
from generator import Tower, Block  # or define them in this file

class JengaEnv(gymnasium.Env):
    def __init__(self):
        super(JengaEnv, self).__init__()

        # Jenga has up to 54 blocks, each can be placed in up to 3 positions => 54 * 3 = 162 possible moves
        self.action_space = spaces.Discrete(54 * 3)

        # Example: observation could be a 54-length array indicating where each block is (0=gone, 1=on tower)
        # or the layer index, or a more advanced representation. For now, keep it simple:
        self.observation_space = spaces.Box(low=0, high=1, shape=(54,), dtype=np.float32)

        self.tower = None
        self.reset()

    def reset(self, seed=None, return_info=False, options=None):
        # 1) Handle seeding if needed
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        # 2) Rebuild tower, etc.
        self.tower = Tower("start")
        observation = self._get_observation()

        # Return either (obs, {}) or just obs
        if return_info:
            return observation, {}
        else:
            return observation, {}

    def step(self, action):
        # Interpret 'action'
        blockID = (action // 3) + 1  # block IDs go from 1..54
        topPos  = (action % 3) + 1   # topPos is 1..3

        # Attempt move
        success = self.tower.move(blockID, topPos, flag=False)

        # If tower invalid after that move, we consider the tower toppled
        done = not self.tower.isTowerValid()
        
        # Reward shaping
        if not success:
            # E.g., you can penalize an invalid or prevented move
            reward = -0.01
        elif done:
            # The move caused the tower to topple
            reward = -1.0
        else:
            # Otherwise, small positive reward for a valid move
            reward = +0.01

        obs = self._get_observation()
        info = {}
        return obs, reward, done, info

    def render(self, mode='human'):
        # Optional: print the tower or show a custom GUI
        print(self.tower)

    def _get_observation(self):
        # Simple example: 1 if block is present, 0 if block is removed (-1)
        arr = np.zeros(54, dtype=np.float32)
        # Tower is a list of layers, each is [Block, Block, Block].
        # Each Block has an ID or -1 if removed.

        for layer in self.tower.tower:
            for block in layer:
                if not block.isNull():
                    # block.getID() is 1..54
                    arr[block.getID()-1] = 1.0
        return arr
