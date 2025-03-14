import gymnasium
import numpy as np
from stable_baselines3 import PPO  # or DQN, A2C, etc.
from jenga_env import JengaEnv  # Import your custom environment

def main():
    # Create the environment
    env = JengaEnv()

    # Initialize the RL model (PPO with an MLP policy, for instance)
    model = PPO('MlpPolicy', env, verbose=1)

    # Train the model
    model.learn(total_timesteps=100000)  # adjust as needed

    # Save the trained model
    model.save("jenga_ppo_model")

    # Test the trained model
    obs = env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        env.render()
        print("Reward:", reward)

if __name__ == "__main__":
    main()