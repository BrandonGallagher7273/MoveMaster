import os
import numpy as np
import random

from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

from jenga_env import JengaEnv
from generator import Tower

def mask_fn(env: JengaEnv):
    return env._compute_action_mask()

def main():
    model_file="jenga_maskable_model.zip"
    model_exists=os.path.isfile(model_file)

    base_env=JengaEnv(silent_prob=True)
    env=ActionMasker(base_env, mask_fn)

    if model_exists:
        choice=input(f"Found '{model_file}'. Load(l) or train(t)? [l/t]: ").strip().lower()
        if choice=="l":
            print("Loading existing model.")
            model=MaskablePPO.load(model_file, env=env)
        else:
            print("Training new model for 3M steps.")
            model=MaskablePPO("MlpPolicy", env, verbose=1)
            model.learn(total_timesteps=3_000_000)
            model.save(model_file)
            print(f"Saved new model => {model_file}")
    else:
        print("No existing model => train from scratch (3M steps).")
        model=MaskablePPO("MlpPolicy", env, verbose=1)
        model.learn(total_timesteps=3_000_000)
        model.save(model_file)
        print(f"Saved => {model_file}")

    choice2=input("Choose:\n a) Provide a sequence => model suggests next move.\n b) Play a Jenga game.\n[a/b]: ").strip().lower()
    if choice2=='a':
        handle_sequence_option(env, model)
    elif choice2=='b':
        handle_play_option(model)
    else:
        print("Invalid => exit.")

def handle_sequence_option(env, model):
    seq_input=input("Enter sequence (e.g. '1.1 2.3 7.2'): ")
    seq=seq_input.strip().split()

    customT=Tower("custom", silent_prob=True)
    for mv in seq:
        try:
            b_str, p_str=mv.split(".")
            b_id=int(b_str)
            pos=int(p_str)
            success=customT.move(b_id, pos, flag=False)
            if not success:
                print(f"Move {mv} => fail => ignoring.")
        except:
            print(f"Invalid => {mv}")
            return

    base_env=env.env
    base_env.tower=customT
    base_env.current_step=0
    base_env.prev_top_count=base_env._count_top_blocks()

    obs=base_env._get_observation()
    action,_=model.predict(obs, deterministic=True)
    blockID=(action//3)+1
    topPos=(action%3)+1

    print(f"-- Next Best Move => remove block #{blockID}, place at {topPos}")

def handle_play_option(model):
    from sb3_contrib.common.wrappers import ActionMasker

    def mask_fn_play(env: JengaEnv):
        return env._compute_action_mask()

    base_play_env=JengaEnv(silent_prob=False)
    play_env=ActionMasker(base_play_env, mask_fn_play)

    obs, info=play_env.reset()
    done=False
    truncated=False
    user_turn=True

    while not(done or truncated):
        play_env.env.render()
        print("\n-- Probability Tower --")
        print(play_env.env.tower.print_prob())

        if user_turn:
            print("\n--- Your Turn ---")
            mv_in=input("Enter 'blockID.pos': ").strip()
            try:
                b_str,p_str=mv_in.split(".")
                b_id=int(b_str)
                pos=int(p_str)
            except:
                print("Invalid => skipping.")
                continue

            action=(b_id-1)*3 + (pos-1)
            obs,reward,done,truncated,info=play_env.step(action)
            if reward<0:
                print(f"Reward={reward:.2f} => fail or risky => continuing anyway.")
        else:
            print("\n--- Model's Turn ---")
            action,_=model.predict(obs, deterministic=True)
            obs,reward,done,truncated,info=play_env.step(action)
            block_id=(action//3)+1
            top_pos=(action%3)+1
            print(f"Model => block #{block_id}, pos {top_pos}, reward={reward:.2f}")
            if reward<0:
                print("Model fail => continuing since fail doesn't end episode.")

        if done:
            print("\nEpisode ended. Possibly tower invalid? Final tower =>")
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
