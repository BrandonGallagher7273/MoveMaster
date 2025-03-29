import gymnasium
from gymnasium import spaces
import numpy as np
import random
import math

from generator import Tower

class JengaEnv(gymnasium.Env):
    def __init__(self, silent_prob=True, fail_ends_game=False):
        super().__init__()
        self.action_space = spaces.Discrete(54*3)
        self.observation_space = spaces.Box(low=0, high=1, shape=(54,), dtype=np.float32)
        self.silent_prob = silent_prob
        self.fail_ends_game = fail_ends_game
        self.tower = Tower("start", silent_prob=self.silent_prob)
        self.current_step = 0
        self.max_steps = 1000

    def reset(self, seed=None, options=None):
        if seed is not None:
            self.np_random, seed = gymnasium.utils.seeding.np_random(seed)
            np.random.seed(seed)
            random.seed(seed)
        self.current_step = 0
        self.tower = Tower("start", silent_prob=self.silent_prob)
        obs = self._get_observation()
        info = {}
        return obs, info

    def step(self, action):
        blockID = (action//3)+1
        topPos = (action%3)+1

        success = self.tower.move(blockID, topPos, flag=True)
        if not success:
            if self.fail_ends_game:
                reward = -1.0
                terminated = True
            else:
                reward = -0.1
                terminated = False
        else:
            reward = 0.02
            terminated = False
        tower_valid = self.tower.isTowerValid()
        if not tower_valid:
            reward -= 1.0
            terminated = True

        obs = self._get_observation()
        self.current_step += 1
        truncated = (self.current_step>=self.max_steps)

        info={}
        return obs, reward, terminated, truncated, info

    def render(self):
        if self.tower:
            print(self.tower)

    def _get_observation(self):
        arr = np.zeros(54, dtype=np.float32)
        for ly in self.tower.tower:
            for blk in ly:
                if not blk.isNull():
                    arr[blk.getID()-1] = 1.0
        return arr


    def _is_move_invalid(self, blockID):
        #temp
        return False
