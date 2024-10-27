import json
import os

configs_dir = "pocketpose/models/configs/"

# Find all json files in configs_dir, open them, merge them into a single list,
# and save at save_path
save_path = "docs/website/_data/model_zoo.json"

configs = []
for filename in os.listdir(configs_dir):
    if filename.endswith(".json"):
        with open(os.path.join(configs_dir, filename)) as f:
            configs.append(json.load(f))

with open(save_path, "w") as f:
    json.dump(configs, f, indent=4)

print(f"Saved {len(configs)} models to {save_path}")
