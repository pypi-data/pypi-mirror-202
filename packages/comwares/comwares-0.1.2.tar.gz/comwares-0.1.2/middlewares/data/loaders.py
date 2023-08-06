import json


def load_json_assets(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
