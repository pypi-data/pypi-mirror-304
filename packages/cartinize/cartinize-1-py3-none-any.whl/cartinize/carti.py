import json, os, random as r


def join(input_arr):
    separators = [r.choice([" ", "  ", "   ", "-"]) for _ in range(len(input_arr))]

    result = ""
    for i, item in enumerate(input_arr):
        result += item
        if i < len(separators):
            result += separators[i]

    return result


def leet(text):
    current_dir = os.path.dirname(__file__)

    leet_dict_path = os.path.join(current_dir, "assets", "leet_dict.json")

    with open(leet_dict_path, "r") as file:
        leet_dict = json.load(file)

    leet_text = "".join(leet_dict.get(char, char) for char in text)

    return leet_text


def carti(text, options={}):
    """
    Function that returns cartinized string value

    Parameters
    ----------
    text (string): string to convert
    options (dict): options to convert string
        - `leet` (bool): use leetcode to encode string. Defaults to True
        - `emoji` (bool): use emojis to encode string. Defaults to True
        - `case` (bool): use random case to encode string. Defaults to True

    Returns
    -------
    string
        Cartinized string
    """
    options["leet"] = options.get("leet", True)
    options["emoji"] = options.get("emoji", True)
    options["case"] = options.get("case", True)

    current_dir = os.path.dirname(__file__)

    carti_fillers_path = os.path.join(current_dir, "assets", "carti_fillers.json")

    with open(carti_fillers_path, "r") as file:
        carti_fillers = json.load(file)

    def randomize_symbol(char):
        random_options = []
        if options["leet"]:
            random_options.append(leet)
        if options["case"]:
            random_options.extend([str.upper, str.lower])

        if len(random_options) == 0:
            return char

        return r.choice(random_options)(char)

    input_list = text.split(" ")

    result = []
    for i in input_list:
        word = "".join(list(map(randomize_symbol, list(i))))
        result.append(word)
        if options["emoji"]:
            result.append(r.choice(carti_fillers["emoji"] + carti_fillers["text"]))
        else:
            result.append(r.choice(carti_fillers["text"]))

    return join(result)
