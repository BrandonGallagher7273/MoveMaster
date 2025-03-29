import gymnasium
import numpy as np
import random
from stable_baselines3 import PPO

from jenga_env import JengaEnv
from generator import Tower

def main():
    env = JengaEnv(silent_prob=True, fail_ends_game=False)
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=100000)
    model.save("jenga_ppo_model")
    print("Training finished. Model saved as 'jenga_ppo_model'.")

if __name__=="__main__":
    main()
