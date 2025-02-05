import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(BASE_DIR, "config", "email_config.json")

def load_email_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)
