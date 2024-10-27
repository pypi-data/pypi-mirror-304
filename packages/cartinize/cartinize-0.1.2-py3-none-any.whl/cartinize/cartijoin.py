import random as r


def cartijoin(input_arr):
    separators = [r.choice([" ", "  ", "   ", "-"]) for _ in range(len(input_arr))]

    result = ""
    for i, item in enumerate(input_arr):
        result += item
        if i < len(separators):
            result += separators[i]

    return result
