import json, random as r

from cartinize.leet import leet
from cartinize.cartijoin import cartijoin

def cartinize(string):
    with open("./assets/carti_fillers.json", "r") as file:
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
