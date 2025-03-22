import gymnasium
from gymnasium import spaces
import numpy as np
import random
import math

from generator import Tower, Block 

class JengaEnv(gymnasium.Env):
    
    def __init__(self):
        super(JengaEnv, self).__init__()
        self.action_space = spaces.Discrete(54 * 3)
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(54,), dtype=np.float32
        )

        self.tower = None
        self.current_step = 0
        self.max_steps = 1000 


    def reset(self, seed=None, options=None):
        if seed is not None:
            self.np_random, seed = gymnasium.utils.seeding.np_random(seed)
            np.random.seed(seed)
            random.seed(seed)

        self.tower = Tower("start")
        self.current_step = 0

        obs = self._get_observation()
        info = {}  
        return obs, info
    
    def _is_in_top_layer(self, blockID):
        if self.tower is None or len(self.tower.tower) == 0:
            return False
        top_layer = self.tower.tower[-1] 
        return any(b.getID() == blockID for b in top_layer if not b.isNull())


    def step(self, action):
        blockID = (action // 3) + 1 
        topPos  = (action % 3) + 1  

        if self._is_in_top_layer(blockID):
            reward = -1.0
            obs = self._get_observation()
            terminated = False
            truncated = False
            info = {}
            return obs, reward, terminated, truncated, info

        success = self.tower.move(blockID, topPos, flag=False)
        tower_fell = not self.tower.isTowerValid()

        if not success:
            reward = -0.01 
        else:
            reward = 0.02   

        if tower_fell:
            reward -= 1.0

        terminated = tower_fell
        self.current_step += 1
        truncated = (self.current_step >= self.max_steps)

        obs = self._get_observation()
        info = {}

        return obs, reward, terminated, truncated, info

    def render(self):
        if self.tower:
            print(self.tower)

    def _get_observation(self):
        arr = np.zeros(54, dtype=np.float32)
        if self.tower is not None:
            for layer in self.tower.tower:
                for block in layer:
                    if not block.isNull():
                        arr[block.getID() - 1] = 1.0
        return arr
