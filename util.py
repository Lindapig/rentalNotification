import json
import os


def load_config(config_path: str):
    with open(config_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
    return config
