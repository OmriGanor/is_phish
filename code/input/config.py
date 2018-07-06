"""
Author: Omri Ganor
Purpose: loads the project configuration
"""
import json


def load_config(config_path):
    with open(config_path, "rb") as f:
        return json.load(f)
