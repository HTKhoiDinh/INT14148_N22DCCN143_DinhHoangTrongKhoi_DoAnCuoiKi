import json


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_fragment_config():
    return load_json("config/fragment_config.json")


def load_user_policy():
    return load_json("config/user_policy.json")


def load_security_policy():
    return load_json("config/security_policy.json")