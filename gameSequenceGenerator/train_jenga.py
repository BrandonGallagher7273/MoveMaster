import gymnasium
import numpy as np
import random
from stable_baselines3 import PPO

from jenga_env import JengaEnv
from generator import Tower, Block

###############################
# Hard-coded sequence (GLOBAL)
###############################
GLOBAL_SEQ = (
    "1.1 4.2 7.3 10.1 13.2 16.3 19.1 22.2 25.3 28.1 31.2 34.3 "
    "37.1 40.2 43.3 46.1 49.2 52.3 3.1 6.2 9.3 12.1 15.2 18.3 "
    "21.1 24.2 27.3 30.1 33.2 36.3 39.1 42.2 45.3 48.1 51.2 54.3"
)

def main():

    env = JengaEnv()
    policy_kwargs = dict(net_arch=[256, 256]) 
    model = PPO("MlpPolicy", env, policy_kwargs=policy_kwargs, verbose=1)
    model.learn(total_timesteps=100000)  
    model.save("jenga_ppo_model")

    customTower = Tower("custom")

    moves = GLOBAL_SEQ.split()
    for move_str in moves:
        block_str, pos_str = move_str.split(".")
        block_id = int(block_str)
        pos = int(pos_str)
        customTower.move(block_id, pos, flag=False)

    env.tower = customTower

    obs = env._get_observation()

    action, _states = model.predict(obs, deterministic=True)

    blockID = (action // 3) + 1
    topPos  = (action % 3) + 1

    print(f"\n--- Next Best Move ---")
    print(f"Remove block #{blockID}, place at position #{topPos}")

if __name__ == "__main__":
    main()
