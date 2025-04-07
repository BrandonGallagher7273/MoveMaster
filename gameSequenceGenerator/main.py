###############################################
# main.py
###############################################
import os
import gymnasium
import numpy as np
import random
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

from jenga_env import JengaEnv
from generator import Tower

def mask_fn(env: JengaEnv) -> np.ndarray:
    return env._compute_action_mask()

def main():
    model_file = "jenga_maskable_model.zip"
    model_exists = os.path.isfile(model_file)

    base_env = JengaEnv(silent_prob=True, fail_ends_game=False)
    env = ActionMasker(base_env, mask_fn)

    if model_exists:
        choice = input(
            f"Found existing model '{model_file}'. Load(l) or train(t)? [l/t]: "
        ).strip().lower()
        if choice=="l":
            print("Loading existing maskable model...")
            model = MaskablePPO.load(model_file, env=env)
        else:
            print("Training new maskable model for 1e6 steps...")
            model = MaskablePPO("MlpPolicy", env, verbose=1)
            model.learn(total_timesteps=1_000_000)
            model.save(model_file)
            print(f"Saved new model as '{model_file}'.")
    else:
        print("No existing model => training from scratch (1e6 steps).")
        model = MaskablePPO("MlpPolicy", env, verbose=1)
        model.learn(total_timesteps=2_000_000)
        model.save(model_file)
        print(f"Model saved as '{model_file}'.")

    choice2 = input(
        "Choose:\n"
        " a) Provide a sequence => model suggests next move.\n"
        " b) Play a Jenga game.\n"
        "[a/b]: "
    ).strip().lower()

    if choice2=='a':
        handle_sequence_option(env, model)
    elif choice2=='b':
        handle_play_option(model)
    else:
        print("Invalid => exit.")

def handle_sequence_option(env, model):
    seq_str = input("Enter a Jenga sequence (e.g. '1.1 2.3 7.2'): ")
    seq = seq_str.split()

    customT = Tower("custom", silent_prob=True)
    for mv in seq:
        try:
            b_str, p_str = mv.split(".")
            b_id=int(b_str)
            pos=int(p_str)
            success=customT.move(b_id,pos,False)
            if not success:
                print(f"Move {mv} failed => ignoring.")
        except:
            print(f"Invalid format => {mv}.")
            return

    base_env = env.env  
    base_env.tower = customT
    base_env.current_step=0

    obs = base_env._get_observation()
    action, _ = model.predict(obs, deterministic=True)
    block_id=(action//3)+1
    topPos=(action%3)+1

    print(f"\n-- Next Best Move => remove block #{block_id}, place at {topPos}")

def handle_play_option(model):
    from sb3_contrib.common.wrappers import ActionMasker

    def mask_fn_play(env: JengaEnv)-> np.ndarray:
        return env._compute_action_mask()

    base_play_env=JengaEnv(silent_prob=False, fail_ends_game=True)
    play_env=ActionMasker(base_play_env, mask_fn_play)

    obs, info = play_env.reset()
    done=False
    truncated=False
    user_turn=True

    while not(done or truncated):
        play_env.env.render()
        print("\n-- Probability Tower --")
        print(play_env.env.tower.print_prob())

        if user_turn:
            print("\n--- Your Turn ---")
            mv=input("Enter 'blockID.pos': ").strip()
            try:
                b_str,p_str=mv.split(".")
                b_id=int(b_str)
                pos=int(p_str)
            except:
                print("Invalid => skip.")
                continue

            action=(b_id-1)*3 + (pos-1)
            obs,rew,done,truncated,info=play_env.step(action)
            if rew<0:
                print(f"Reward={rew} => might end game.")
        else:
            print("\n--- Model's Turn ---")
            action,_=model.predict(obs, deterministic=True)
            obs,rew,done,truncated,info=play_env.step(action)

            b_id=(action//3)+1
            p_val=(action%3)+1
            print(f"Model => block #{b_id} => top pos {p_val}, reward={rew:.2f}")
            if rew<0:
                print("Fail => game might end.")

        if done:
            print("\nGame Over => final tower =>")
            play_env.env.render()
            print("\n-- Final Probability Tower --")
            print(play_env.env.tower.print_prob())
            break
        elif truncated:
            print("\nMax steps => done.")
            break

        user_turn=not user_turn

    print("Game end.")


if __name__=="__main__":
    main()
