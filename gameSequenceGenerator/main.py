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

    choice = input(
        "Choose an option:\n"
        " a) Provide a sequence; model suggests next move.\n"
        " b) Play a Jenga game against the model.\n"
        "Enter 'a' or 'b': "
    ).strip().lower()

    if choice=='a':
        handle_sequence_option(env, model)
    elif choice=='b':
        play_env = JengaEnv(silent_prob=False, fail_ends_game=True)
        handle_play_option(play_env, model)
    else:
        print("Invalid choice. Exiting.")


def handle_sequence_option(env, model):
    seq_input = input("Enter your Jenga sequence (e.g., '1.1 2.3 7.2'): ")
    seq = seq_input.strip().split()
    customT = Tower("custom", silent_prob=True)
    for mv in seq:
        try:
            b_str, p_str = mv.split(".")
            b_id = int(b_str)
            p_val= int(p_str)
            success = customT.move(b_id, p_val, flag=False)
            if not success:
                print(f"Move {mv} failed, continuing.")
        except:
            print(f"Invalid format {mv}")
            return

    env.tower = customT
    env.current_step = 0

    obs = env._get_observation()
    action, _ = model.predict(obs, deterministic=True)
    blockID = (action//3)+1
    topPos = (action%3)+1

    print(f"\n--- Next Best Move ---\nRemove block #{blockID}, place at position #{topPos}")

def handle_play_option(env, model):
    obs, info = env.reset()
    done=False
    truncated=False
    user_turn=True

    while not (done or truncated):
        env.render()
        if user_turn:
            print("\n--- Your Turn ---")
            mv = input("Enter your move as 'blockID.pos': ")
            try:
                b_str,p_str = mv.split(".")
                b_id=int(b_str)
                p_val=int(p_str)
            except:
                print("Invalid format")
                continue
            action = (b_id-1)*3+(p_val-1)
            obs, reward, done, truncated, info = env.step(action)
            if reward<0:
                print(f"Reward={reward:.2f} => Possibly invalid or probability fail.")
        else:
            print("\n--- Model's Turn ---")
            action, _=model.predict(obs, deterministic=True)
            obs, reward, done, truncated, info=env.step(action)
            b_id=(action//3)+1
            p_val=(action%3)+1
            print(f"Model removed block #{b_id}, placed at {p_val}. (Reward={reward:.2f})")
            if reward<0:
                print("Model's move invalid or prob fail?")

        if done:
            print("\nTower toppled or move failed => game over!")
            env.render()
            break
        elif truncated:
            print("\nReached max steps => stop.")
            break

        user_turn= not user_turn

    print("Game Over.")

if __name__=="__main__":
    main()
