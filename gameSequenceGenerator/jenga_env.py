import gymnasium
from gymnasium import spaces
import numpy as np
import random
import math
from collections import defaultdict

from generator import Tower

class JengaEnv(gymnasium.Env):
    def __init__(self, silent_prob=True):
        super().__init__()
        self.action_space = spaces.Discrete(54*3)
        self.observation_space = spaces.Box(low=0, high=1, shape=(54,), dtype=np.float32)

        self.silent_prob = silent_prob
        self.tower = Tower("start", silent_prob=self.silent_prob)
        self.current_step = 0
        self.max_steps = 2500
        self.block_fail_count = defaultdict(int)

        self.prev_top_count = self._count_top_blocks()

    def reset(self, seed=None, options=None):
        if seed is not None:
            self.np_random, seed = gymnasium.utils.seeding.np_random(seed)
            np.random.seed(seed)
            random.seed(seed)

        self.current_step = 0
        self.tower = Tower("start", silent_prob=self.silent_prob)
        self.block_fail_count = defaultdict(int)
        self.prev_top_count = self._count_top_blocks()

        obs = self._get_observation()
        info={}
        return obs, info

    def step(self, action):
        blockID = (action // 3) + 1
        topPos  = (action % 3) + 1

        old_height = len(self.tower.tower)
        success = self.tower.move(blockID, topPos, flag=True)

        if not success:
            self.block_fail_count[blockID]+=1
            fail_times = self.block_fail_count[blockID]
            reward = -10.0 * fail_times
        else:
            reward = 2
            new_height = len(self.tower.tower)
            if new_height>old_height:
                reward += 40.0
            else:
                top_now = self._count_top_blocks()
                if self.prev_top_count==2 and top_now==3:
                    reward += 20.0
            self.prev_top_count = self._count_top_blocks()

        self.current_step += 1
        truncated = (self.current_step>=self.max_steps)
        terminated = False

        obs = self._get_observation()
        info={}
        return obs, reward, terminated, truncated, info

    def render(self):
        if self.tower:
            print(self.tower)

    def _get_observation(self):
        arr=np.zeros(54,dtype=np.float32)
        for layer in self.tower.tower:
            for blk in layer:
                if not blk.isNull():
                    arr[blk.getID()-1]=1.0
        return arr

    def _compute_action_mask(self) -> np.ndarray:
        mask = np.ones((54*3,), dtype=bool)

        top_idx = len(self.tower.tower)-1
        minus_1 = top_idx-1

        top_ids = {b.getID() for b in self.tower.tower[top_idx]}
        minus_ids = set()
        if minus_1>=0:
            minus_ids={b.getID() for b in self.tower.tower[minus_1]}

        for block_id in range(1,55):
            off=(block_id-1)*3
            if (block_id in top_ids) or (block_id in minus_ids):
                mask[off:off+3]=False

        return mask

    def _count_top_blocks(self):
        topL=self.tower.tower[-1]
        return sum(1 for b in topL if not b.isNull())
