###############################################
# train_jenga.py
###############################################
import os
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

from jenga_env import JengaEnv

def mask_fn(env: JengaEnv):
    return env._compute_action_mask()

def main():
    model_file="jenga_maskable_model.zip"
    base_env=JengaEnv(silent_prob=True, fail_ends_game=False)
    env=ActionMasker(base_env, mask_fn)

    if os.path.isfile(model_file):
        choice=input(f"Found '{model_file}'. Load(l) or train(t)? [l/t]: ").strip().lower()
        if choice=="l":
            print("Loading existing maskable model...")
            model=MaskablePPO.load(model_file, env=env)
        else:
            print("Training new maskable model => 1e6 steps.")
            model=MaskablePPO("MlpPolicy", env, verbose=1)
            model.learn(total_timesteps=1_000_000)
            model.save(model_file)
            print(f"Saved new model => {model_file}")
    else:
        print("No existing model => train from scratch (1e6 steps).")
        model=MaskablePPO("MlpPolicy", env, verbose=1)
        model.learn(total_timesteps=1_000_000)
        model.save(model_file)
        print(f"Saved model => {model_file}")

    print("Done with train_jenga.")


if __name__=="__main__":
    main()
