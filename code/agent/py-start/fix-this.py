import json

def load_config():
    config = json.load(open("config.json"))
    # TODO: validate config structure
    return config
