import json, os


def leet(text):
    current_dir = os.path.dirname(__file__)

    leet_dict_path = os.path.join(current_dir, "assets", "leet_dict.json")

    with open(leet_dict_path, "r") as file:
        leet_dict = json.load(file)

    leet_text = "".join(leet_dict.get(char, char) for char in text)

    return leet_text
