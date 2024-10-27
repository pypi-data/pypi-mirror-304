import json, sys, random as r
from modules.leetcode import leet
from modules.join_string import carti_join


def cartinize():
    with open("assets/carti_fillers.json", "r") as file:
        carti_fillers = json.load(file)

    def randomize_symbol(char):
        return r.choice([str.upper, str.lower, leet])(char)

    input_list = sys.argv[1].split(" ")

    result = []
    for i in input_list:
        word = "".join(list(map(randomize_symbol, list(i))))
        result.append(word)
        result.append(r.choice(carti_fillers))

    return carti_join(result)
