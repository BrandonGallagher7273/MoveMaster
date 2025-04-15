import os
from sb3_contrib import MaskablePPO
from sb3_contrib.common.wrappers import ActionMasker

from jenga_env import JengaEnv

def mask_fn(env: JengaEnv):
    return env._compute_action_mask()

def main():
    model_file="jenga_maskable_model.zip"
    base_env=JengaEnv(silent_prob=True)
    env=ActionMasker(base_env, mask_fn)

    if os.path.isfile(model_file):
        choice=input(f"Found '{model_file}'. Load(l) or train(t)? [l/t]: ").strip().lower()
        if choice=="l":
            print("Loading existing model => continuing training or usage.")
            model=MaskablePPO.load(model_file, env=env)
        else:
            print("Training new model => 3M steps.")
            model=MaskablePPO("MlpPolicy", env, verbose=1)
            model.learn(total_timesteps=3_000_000)
            model.save(model_file)
            print(f"Saved => {model_file}")
    else:
        print("No model => train from scratch (3M).")
        model=MaskablePPO("MlpPolicy", env, verbose=1)
        model.learn(total_timesteps=3_000_000)
        model.save(model_file)
        print(f"Saved => {model_file}")

    print("Done with train_jenga.")

if __name__=="__main__":
    main()
