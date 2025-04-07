###############################################
# jenga_env.py
###############################################
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
        blockID = (action // 3) + 1
        topPos  = (action % 3) + 1

        success = self.tower.move(blockID, topPos, True)
        if not success:
            reward = -2.0
            terminated = self.fail_ends_game
        else:
            reward = 0.02
            terminated = False

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
        for layer in self.tower.tower:
            for blk in layer:
                if not blk.isNull():
                    arr[blk.getID() - 1] = 1.0
        return arr

    def _compute_action_mask(self) -> np.ndarray:
        mask = np.ones((54*3,), dtype=bool)
        top_index = len(self.tower.tower) - 1
        top_minus_1 = top_index - 1

        top_ids = {b.getID() for b in self.tower.tower[top_index]}
        minus1_ids = set()
        if top_minus_1 >= 0:
            minus1_ids = {b.getID() for b in self.tower.tower[top_minus_1]}

        for block_id in range(1, 55):
            offset = (block_id - 1)*3
            if (block_id in top_ids) or (block_id in minus1_ids):
                mask[offset:offset+3] = False

        return mask
