import json


def leet(text):
    with open("./assets/leet_dict.json", "r") as file:
        leet_dict = json.load(file)

    leet_text = "".join(leet_dict.get(char, char) for char in text)

    return leet_text
