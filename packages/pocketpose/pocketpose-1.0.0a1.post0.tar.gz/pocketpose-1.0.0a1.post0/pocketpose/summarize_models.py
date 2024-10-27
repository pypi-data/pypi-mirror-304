import argparse
import json
import os

from .utils.io import write_to_table
from .utils.stats import get_stats_tflite, tabulate_stats


def parse_args():
    parser = argparse.ArgumentParser("Prints statistics about TFLite models")
    parser.add_argument(
        "--model_dir",
        type=str,
        required=True,
        help="Path to directory containing TFLite models",
    )
    parser.add_argument(
        "--save_file",
        type=str,
        required=False,
        default="./docs/model_statistics.json",
        help="Path to save results",
    )
    return parser.parse_args()


def list_models(models_dir: str):
    """List all TFLite models in a folder."""
    models = [m for m in os.listdir(models_dir) if m.endswith(".tflite")]
    models = sorted(models)
    return models


def main():
    args = parse_args()
    model_dir = args.model_dir
    models = list_models(model_dir)

    current_stats = {}
    for model in models:
        model_path = os.path.join(model_dir, model)
        model_key, model_stats = get_stats_tflite(model_path)

        if model_key in current_stats:
            current_stats[model_key].update(model_stats)
        else:
            current_stats[model_key] = model_stats

    # Update the JSON file with the stats
    json_path = args.save_file
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    existing_stats = {}
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            existing_stats = json.load(f)

    # Merge the existing stats with the new stats
    for model_key, model_stats in current_stats.items():
        if model_key in existing_stats:
            existing_stats[model_key].update(model_stats)
        else:
            existing_stats[model_key] = model_stats
        existing_stats[model_key] = dict(sorted(existing_stats[model_key].items()))

    # Sort the stats by model name
    existing_stats = dict(sorted(existing_stats.items()))

    # Write the stats to the JSON file
    with open(json_path, "w") as f:
        json.dump(existing_stats, f, indent=2)

    # Write the stats to a Markdown file
    stats = tabulate_stats(existing_stats)
    stats_path = os.path.splitext(json_path)[0] + ".md"
    write_to_table(stats, stats_path)


if __name__ == "__main__":
    main()
