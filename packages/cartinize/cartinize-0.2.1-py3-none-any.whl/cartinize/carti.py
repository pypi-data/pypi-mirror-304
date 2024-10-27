import json, os, random as r

from cartinize.leet import leet
from cartinize.cartijoin import cartijoin


def carti(string):
    current_dir = os.path.dirname(__file__)

    carti_fillers_path = os.path.join(current_dir, "assets", "carti_fillers.json")

    with open(carti_fillers_path, "r") as file:
        carti_fillers = json.load(file)

    def randomize_symbol(char):
        return r.choice([str.upper, str.lower, leet])(char)

    input_list = string.split(" ")

    result = []
    for i in input_list:
        word = "".join(list(map(randomize_symbol, list(i))))
        result.append(word)
        result.append(r.choice(carti_fillers))

    return cartijoin(result)
